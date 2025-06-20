//! Shared helpers for all tests.
use anyhow::Result;
use deltalake::DeltaTable;
use std::sync::Once;
use testcontainers::{clients, images::generic::GenericImage, Container, Docker};

static INIT: Once = Once::new();

/// Spins up MinIO + DynamoDB in Docker exactly once for the entire test run.
pub(crate) fn setup_docker() -> (Container<'static, GenericImage>, Container<'static, GenericImage>) {
    INIT.call_once(|| {
        // nothing – Once just ensures the log statement below prints once
        env_logger::try_init().ok();
        log::info!("🚀  Starting test containers…");
    });

    let docker = clients::Cli::default();

    // MinIO image (latest tag, stable API)
    let minio = docker.run(
        GenericImage::new("minio/minio", "latest")
            .with_env_var("MINIO_ROOT_USER", "minioadmin")
            .with_env_var("MINIO_ROOT_PASSWORD", "minioadmin")
            .with_wait_for(testcontainers::core::WaitFor::message_on_stdout(
                "API: http://",
            ))
            .with_entrypoint(["server", "/data", "--console-address", ":9001"]),
    );

    // DynamoDB local image
    let dynamo = docker.run(
        GenericImage::new("amazon/dynamodb-local", "latest").with_wait_for(
            testcontainers::core::WaitFor::message_on_stdout("Initializing DynamoDB Local"),
        ),
    );

    (minio, dynamo)
}

/// Convenience – returns a configured DeltaTable pointing at the test MinIO bucket.
///
/// IMPLEMENTATION:
/// 1. Build S3 URI: s3://test-bucket/{table_name}
/// 2. Pre-create bucket via MinIO client if not exists.
/// 3. Return DeltaTable::new(table_uri).
pub(crate) async fn create_delta_table(table_name: &str) -> Result<DeltaTable> {
    // TODO: implement real delta table creation
    todo!("Implement delta table creation with MinIO backend")
} 