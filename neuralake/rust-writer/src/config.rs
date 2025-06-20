use serde::{Deserialize, Serialize};
use std::time::Duration;

/// Configuration for the Writer process
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WriterConfig {
    /// Maximum batch size before forcing a write
    pub max_batch_size: usize,
    /// Maximum time to wait before forcing a write
    pub max_batch_time_ms: u64,
    /// Maximum latency target in milliseconds  
    pub max_latency_ms: u64,
    /// Number of retries on write failure
    pub max_retries: u32,
    /// Backoff delay between retries in milliseconds
    pub retry_delay_ms: u64,
}

impl Default for WriterConfig {
    fn default() -> Self {
        Self {
            max_batch_size: 1000,
            max_batch_time_ms: 1000, // 1 second
            max_latency_ms: 250,     // 250ms SLA
            max_retries: 3,
            retry_delay_ms: 100,
        }
    }
}

/// Configuration for the Compaction process
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CompactionConfig {
    /// Target file size in bytes for compacted files
    pub target_file_size_bytes: u64,
    /// Minimum number of files to trigger compaction
    pub min_files_to_compact: usize,
    /// Compaction interval in seconds
    pub compaction_interval_secs: u64,
    /// Maximum concurrent compaction tasks
    pub max_concurrent_compactions: usize,
}

impl Default for CompactionConfig {
    fn default() -> Self {
        Self {
            target_file_size_bytes: 128 * 1024 * 1024, // 128 MB
            min_files_to_compact: 5,
            compaction_interval_secs: 300, // 5 minutes
            max_concurrent_compactions: 2,
        }
    }
}

/// Configuration for the Vacuum process
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VacuumConfig {
    /// Retention period in hours
    pub retention_hours: u64,
    /// Vacuum interval in seconds
    pub vacuum_interval_secs: u64,
    /// Whether to perform dry runs first
    pub dry_run: bool,
}

impl Default for VacuumConfig {
    fn default() -> Self {
        Self {
            retention_hours: 72, // 3 days
            vacuum_interval_secs: 3600, // 1 hour
            dry_run: false,
        }
    }
}

impl WriterConfig {
    pub fn max_batch_time(&self) -> Duration {
        Duration::from_millis(self.max_batch_time_ms)
    }
    
    pub fn max_latency(&self) -> Duration {
        Duration::from_millis(self.max_latency_ms)
    }
    
    pub fn retry_delay(&self) -> Duration {
        Duration::from_millis(self.retry_delay_ms)
    }
}

impl CompactionConfig {
    pub fn compaction_interval(&self) -> Duration {
        Duration::from_secs(self.compaction_interval_secs)
    }
}

impl VacuumConfig {
    pub fn vacuum_interval(&self) -> Duration {
        Duration::from_secs(self.vacuum_interval_secs)
    }
} 