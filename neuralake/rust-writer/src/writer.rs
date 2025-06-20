use anyhow::{Context, Result};
use deltalake::writer::RecordBatchWriter;
use deltalake::{DeltaTable, StorageOptions};
use polars::prelude::DataFrame;
use std::sync::Arc;
use tokio::sync::Mutex;
use tokio::time::{Duration, Instant, interval};
use crate::config::WriterConfig;

/// The Writer process - continuously appends small files to Delta tables with minimal latency
#[derive(Debug, Clone)]
pub struct WriterProcess {
    config: WriterConfig,
}

impl WriterProcess {
    /// Create a new writer process
    pub fn new(config: WriterConfig) -> Self {
        Self { config }
    }

    /// Main run loop for the writer process
    pub async fn run(
        &self,
        table: Arc<Mutex<DeltaTable>>,
        storage_options: StorageOptions,
    ) -> Result<()> {
        log::info!("Starting Writer process");
        
        let mut interval = interval(self.config.max_batch_time());
        
        loop {
            tokio::select! {
                _ = interval.tick() => {
                    // Periodic flush - in a real implementation, this would flush
                    // accumulated batches from a queue
                    log::debug!("Writer process tick - would flush accumulated batches");
                }
                _ = tokio::signal::ctrl_c() => {
                    log::info!("Writer process received shutdown signal");
                    break;
                }
            }
        }
        
        Ok(())
    }

    /// Write a single batch to the Delta table
    pub async fn write_batch(
        &self,
        df: DataFrame,
        storage_options: &StorageOptions,
        table_uri: &str,
    ) -> Result<()> {
        let start_time = Instant::now();
        
        let mut retry_count = 0;
        
        while retry_count <= self.config.max_retries {
            match self.try_write_batch(&df, storage_options, table_uri).await {
                Ok(()) => {
                    let elapsed = start_time.elapsed();
                    log::debug!("Write completed in {:?}", elapsed);
                    
                    // Check if we exceeded our latency SLA
                    if elapsed > self.config.max_latency() {
                        log::warn!(
                            "Write exceeded latency SLA: {:?} > {:?}",
                            elapsed,
                            self.config.max_latency()
                        );
                    }
                    
                    return Ok(());
                }
                Err(e) => {
                    retry_count += 1;
                    if retry_count > self.config.max_retries {
                        return Err(e).with_context("All write retries exhausted");
                    }
                    
                    log::warn!(
                        "Write attempt {} failed, retrying: {}",
                        retry_count,
                        e
                    );
                    
                    tokio::time::sleep(self.config.retry_delay()).await;
                }
            }
        }
        
        unreachable!()
    }

    /// Internal method to attempt writing a batch
    async fn try_write_batch(
        &self,
        df: &DataFrame,
        storage_options: &StorageOptions,
        table_uri: &str,
    ) -> Result<()> {
        // Convert Polars DataFrame to Arrow RecordBatch
        let batch = df.to_arrow(None)
            .with_context("Failed to convert DataFrame to Arrow")?;
            
        // Create a new writer with storage options
        let mut writer = RecordBatchWriter::for_table_path(table_uri)
            .with_context("Failed to create RecordBatchWriter")?
            .with_storage_options(storage_options.clone());
            
        // Write the batch
        writer.write(batch)
            .await
            .with_context("Failed to write batch")?;
            
        // Close the writer to commit the transaction
        writer.close()
            .await
            .with_context("Failed to close writer")?;
            
        Ok(())
    }

    /// Get metrics about the writer performance
    pub fn get_metrics(&self) -> WriterMetrics {
        WriterMetrics {
            config: self.config.clone(),
            // In a real implementation, these would be tracked
            total_batches_written: 0,
            total_rows_written: 0,
            average_latency_ms: 0.0,
            p99_latency_ms: 0.0,
        }
    }
}

/// Metrics for the writer process
#[derive(Debug, Clone)]
pub struct WriterMetrics {
    pub config: WriterConfig,
    pub total_batches_written: u64,
    pub total_rows_written: u64,
    pub average_latency_ms: f64,
    pub p99_latency_ms: f64,
} 