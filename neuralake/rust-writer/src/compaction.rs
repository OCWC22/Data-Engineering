use anyhow::{Context, Result};
use deltalake::DeltaTable;
use std::sync::Arc;
use tokio::sync::Mutex;
use tokio::time::{interval, Instant};
use crate::config::CompactionConfig;

/// The Compaction process - merges small files into larger, optimized ones
#[derive(Debug, Clone)]
pub struct CompactionProcess {
    config: CompactionConfig,
}

impl CompactionProcess {
    /// Create a new compaction process
    pub fn new(config: CompactionConfig) -> Self {
        Self { config }
    }

    /// Main run loop for the compaction process
    pub async fn run(&self, table: Arc<Mutex<DeltaTable>>) -> Result<()> {
        log::info!("Starting Compaction process");
        
        let mut interval_timer = interval(self.config.compaction_interval());
        
        loop {
            tokio::select! {
                _ = interval_timer.tick() => {
                    if let Err(e) = self.run_compaction_cycle(&table).await {
                        log::error!("Compaction cycle failed: {}", e);
                    }
                }
                _ = tokio::signal::ctrl_c() => {
                    log::info!("Compaction process received shutdown signal");
                    break;
                }
            }
        }
        
        Ok(())
    }

    /// Run a single compaction cycle
    async fn run_compaction_cycle(&self, table: &Arc<Mutex<DeltaTable>>) -> Result<()> {
        let start_time = Instant::now();
        
        // Lock the table for compaction
        let mut locked_table = table.lock().await;
        
        // Check if compaction is needed
        let file_count = locked_table.get_files_iter()?.count();
        
        if file_count < self.config.min_files_to_compact {
            log::debug!(
                "Skipping compaction: {} files < {} minimum",
                file_count,
                self.config.min_files_to_compact
            );
            return Ok(());
        }
        
        log::info!("Starting compaction: {} files to process", file_count);
        
        // Run the actual compaction
        self.run_once(&mut locked_table).await?;
        
        let elapsed = start_time.elapsed();
        let new_file_count = locked_table.get_files_iter()?.count();
        
        log::info!(
            "Compaction completed in {:?}: {} files -> {} files",
            elapsed,
            file_count,
            new_file_count
        );
        
        Ok(())
    }

    /// Run compaction once on the given table
    pub async fn run_once(&self, table: &mut DeltaTable) -> Result<()> {
        // Refresh the table to get latest state
        table.update().await
            .with_context("Failed to refresh table before compaction")?;
            
        // Run the optimize operation
        // Note: In delta-rs, optimize() handles the compaction logic
        table.optimize(None).await
            .with_context("Failed to run optimize operation")?;
            
        Ok(())
    }

    /// Get metrics about the compaction performance
    pub fn get_metrics(&self) -> CompactionMetrics {
        CompactionMetrics {
            config: self.config.clone(),
            // In a real implementation, these would be tracked
            total_compactions_run: 0,
            total_files_compacted: 0,
            total_bytes_compacted: 0,
            average_compaction_time_ms: 0.0,
        }
    }
}

/// Metrics for the compaction process
#[derive(Debug, Clone)]
pub struct CompactionMetrics {
    pub config: CompactionConfig,
    pub total_compactions_run: u64,
    pub total_files_compacted: u64,
    pub total_bytes_compacted: u64,
    pub average_compaction_time_ms: f64,
} 