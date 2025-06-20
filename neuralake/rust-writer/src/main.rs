use anyhow::Result;
use clap::{Parser, Subcommand};
use polars::prelude::*;
use surgical_strike_writer::*;
use std::collections::HashMap;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Start the full orchestrator with all three processes
    Start {
        #[arg(short, long, default_value = "config.toml")]
        config: String,
    },
    /// Write a single test batch
    WriteBatch {
        #[arg(short, long)]
        table_uri: String,
        #[arg(short, long, default_value = "10")]
        rows: usize,
    },
    /// Run compaction once
    Compact {
        #[arg(short, long)]
        table_uri: String,
    },
    /// Run vacuum once
    Vacuum {
        #[arg(short, long)]
        table_uri: String,
        #[arg(short, long, default_value = "72")]
        retention_hours: u64,
    },
}

#[tokio::main]
async fn main() -> Result<()> {
    env_logger::init();
    
    let cli = Cli::parse();

    match &cli.command {
        Commands::Start { config } => {
            println!("Starting Surgical Strike Writer with config: {}", config);
            
            // For now, use default config
            let config = create_default_config();
            let orchestrator = SurgicalStrikeOrchestrator::new(config).await?;
            
            orchestrator.start().await?;
        }
        Commands::WriteBatch { table_uri, rows } => {
            println!("Writing test batch with {} rows to {}", rows, table_uri);
            
            let config = create_config_for_table(table_uri);
            let orchestrator = SurgicalStrikeOrchestrator::new(config).await?;
            
            let test_df = create_test_dataframe(*rows)?;
            orchestrator.write_batch(test_df).await?;
            
            println!("Successfully wrote {} rows", rows);
        }
        Commands::Compact { table_uri } => {
            println!("Running compaction on {}", table_uri);
            
            let config = create_config_for_table(table_uri);
            let orchestrator = SurgicalStrikeOrchestrator::new(config).await?;
            
            orchestrator.compact().await?;
            
            println!("Compaction completed");
        }
        Commands::Vacuum { table_uri, retention_hours } => {
            println!("Running vacuum on {} with retention {} hours", table_uri, retention_hours);
            
            let mut config = create_config_for_table(table_uri);
            config.vacuum.retention_hours = *retention_hours;
            
            let orchestrator = SurgicalStrikeOrchestrator::new(config).await?;
            
            orchestrator.vacuum().await?;
            
            println!("Vacuum completed");
        }
    }

    Ok(())
}

fn create_default_config() -> SurgicalStrikeConfig {
    SurgicalStrikeConfig {
        table_uri: "s3://neuralake-bucket/test-table".to_string(),
        storage_options: deltalake::StorageOptions(
            HashMap::from([
                ("AWS_ENDPOINT_URL".to_string(), "http://localhost:9000".to_string()),
                ("AWS_ACCESS_KEY_ID".to_string(), "minioadmin".to_string()),
                ("AWS_SECRET_ACCESS_KEY".to_string(), "minioadmin".to_string()),
                ("AWS_REGION".to_string(), "us-east-1".to_string()),
            ])
            .into(),
        ),
        ..Default::default()
    }
}

fn create_config_for_table(table_uri: &str) -> SurgicalStrikeConfig {
    SurgicalStrikeConfig {
        table_uri: table_uri.to_string(),
        storage_options: deltalake::StorageOptions(
            HashMap::from([
                ("AWS_ENDPOINT_URL".to_string(), "http://localhost:9000".to_string()),
                ("AWS_ACCESS_KEY_ID".to_string(), "minioadmin".to_string()),
                ("AWS_SECRET_ACCESS_KEY".to_string(), "minioadmin".to_string()),
                ("AWS_REGION".to_string(), "us-east-1".to_string()),
            ])
            .into(),
        ),
        ..Default::default()
    }
}

fn create_test_dataframe(rows: usize) -> Result<DataFrame> {
    let ids: Vec<i32> = (1..=rows as i32).collect();
    let values: Vec<String> = (1..=rows).map(|i| format!("value_{}", i)).collect();
    let timestamps = vec![chrono::Utc::now().timestamp(); rows];
    
    let df = df! {
        "id" => ids,
        "value" => values,
        "timestamp" => timestamps,
    }?;
    
    Ok(df)
} 