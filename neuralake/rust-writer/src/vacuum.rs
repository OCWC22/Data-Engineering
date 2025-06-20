use anyhow::{Context, Result};
use deltalake::DeltaTable;
use std::sync::Arc;
use tokio::sync::Mutex;
use tokio::time::{interval, Instant};
use crate::config::VacuumConfig;

/// The Vacuum process - cleans up stale files beyond retention period
#[derive(Debug, Clone)]
pub struct VacuumProcess {
    config: VacuumConfig,
}

impl VacuumProcess {
    /// Create a new vacuum process
    pub fn new(config: VacuumConfig) -> Self {
        Self { config }
    }

    /// Main run loop for the vacuum process
    pub async fn run(&self, table: Arc<Mutex<DeltaTable>>) -> Result<()> {
        log::info!("Starting Vacuum process");
        
        let mut interval_timer = interval(self.config.vacuum_interval());
        
        loop {
            tokio::select! {
                _ = interval_timer.tick() => {
                    if let Err(e) = self.run_vacuum_cycle(&table).await {
                        log::error!("Vacuum cycle failed: {}", e);
                    }
                }
                _ = tokio::signal::ctrl_c() => {
                    log::info!("Vacuum process received shutdown signal");
                    break;
                }
            }
        }
        
        Ok(())
    }

    /// Run a single vacuum cycle
    async fn run_vacuum_cycle(&self, table: &Arc<Mutex<DeltaTable>>) -> Result<()> {
        let start_time = Instant::now();
        
        // Lock the table for vacuum
        let mut locked_table = table.lock().await;
        
        log::info!(
            "Starting vacuum cycle: retention_hours={}, dry_run={}",
            self.config.retention_hours,
            self.config.dry_run
        );
        
        // Get file count before vacuum
        let files_before = locked_table.get_files_iter()?.count();
        
        // Run the actual vacuum
        self.run_once(&mut locked_table).await?;
        
        // Get file count after vacuum
        locked_table.update().await
            .with_context("Failed to refresh table after vacuum")?;
        let files_after = locked_table.get_files_iter()?.count();
        
        let elapsed = start_time.elapsed();
        let files_removed = files_before.saturating_sub(files_after);
        
        log::info!(
            "Vacuum completed in {:?}: {} files removed ({} -> {})",
            elapsed,
            files_removed,
            files_before,
            files_after
        );
        
        Ok(())
    }

    /// Run vacuum once on the given table
    pub async fn run_once(&self, table: &mut DeltaTable) -> Result<()> {
        // Refresh the table to get latest state
        table.update().await
            .with_context("Failed to refresh table before vacuum")?;
            
        // Run the vacuum operation
        // Note: In delta-rs, vacuum() handles the cleanup logic
        table.vacuum(
            Some(self.config.retention_hours),
            self.config.dry_run,
            None, // enforce_retention_duration
        ).await
        .with_context("Failed to run vacuum operation")?;
            
        Ok(())
    }

    /// Get metrics about the vacuum performance
    pub fn get_metrics(&self) -> VacuumMetrics {
        VacuumMetrics {
            config: self.config.clone(),
            // In a real implementation, these would be tracked
            total_vacuum_runs: 0,
            total_files_removed: 0,
            total_bytes_freed: 0,
            average_vacuum_time_ms: 0.0,
        }
    }
}

/// Metrics for the vacuum process
#[derive(Debug, Clone)]
pub struct VacuumMetrics {
    pub config: VacuumConfig,
    pub total_vacuum_runs: u64,
    pub total_files_removed: u64,
    pub total_bytes_freed: u64,
    pub average_vacuum_time_ms: f64,
} 