Below is a tightened-up Task 6 specification with exact crate versions, library choices, starter code snippets, and changelog-friendly structure.  Everything is expressed in Markdown so you can drop it straight into .taskmaster/tasks/task_006.txt (or paste the subtask sections into their own files) without post-editing.

⸻

🚀 Updated Task 6 – Low-Latency “Surgical Strike” Writer

<details>
<summary>**Quick-glance summary**</summary>


	•	Language / edition: Rust 1.77+, edition 2021
	•	Async runtime: Tokio 1.37.0 (full features)  ￼
	•	Delta Lake layer: deltalake 0.27.0 (with json,s3,aws,optimize,datafusion features)  ￼
	•	DataFrame engine: polars 0.49.1 (with lazy,parquet,json,ipc,dtype-struct,arrow)  ￼ ￼
	•	Columnar IO: arrow 55.1.0  ￼ ￼
	•	AWS clients: aws-sdk-s3 1.95.0, aws-sdk-dynamodb 1.93.0  ￼ ￼
	•	Config loader: config 0.14.0  ￼
	•	CLI: clap 4.5.4 (derive)  ￼
	•	Observability: metrics 0.23 + metrics-exporter-prometheus 0.15.0  ￼
	•	Local dockerised infra for tests: testcontainers 0.15.7 (with minio,localstack modules)  ￼
	•	Benchmarks: criterion 0.5.1   ￼

</details>


1  High-level deliverables

Phase	Deliverable	Notes
6.1	writer.rs – async ingest loop (JSON → Polars → Delta commit)	Target p99 ≤ 250 ms for 1 k rows/batch
6.2	compactor.rs – smart OPTIMIZE wrapper	Size- & time-based triggers (300 s default)
6.3	vacuum.rs – retention vacuum	Default 168 h retention; honour minVersions
6.4	locking.rs – DynamoDB coarse lock	Conditional-write pattern (PutItem … ConditionExpression attribute_not_exists)
6.5	daemon sub-command	Spawns the three processes; Prometheus metrics on :9090

2  Starter repository layout

rust-writer/
├── Cargo.toml
├── config.toml          # opinionated defaults for LOCAL env
└── src/
    ├── main.rs          # CLI & daemon supervisor
    ├── config.rs        # strongly-typed Config using `config` & `serde`
    ├── writer.rs
    ├── compactor.rs
    ├── vacuum.rs
    ├── locking.rs
    └── lib.rs           # re-exports for benches/tests

3  Cargo.toml template (💯 compile-ready)

[package]
name            = "neuralake-writer"
version         = "0.1.0"
edition         = "2021"
publish         = false

[dependencies]
tokio           = { version = "1.37.0", features = ["full"] }          # async runtime  [oai_citation:13‡crates.io](https://crates.io/crates/tokio?utm_source=chatgpt.com)
polars          = { version = "0.49.1", features = ["lazy","parquet","json","ipc","dtype-struct","arrow"] }  [oai_citation:14‡docs.rs](https://docs.rs/polars/latest/polars/frame/struct.DataFrame.html?utm_source=chatgpt.com)
arrow           = "55.1.0"                                             # columnar memory  [oai_citation:15‡docs.rs](https://docs.rs/arrow/latest/arrow/ffi_stream/index.html)
deltalake       = { version = "0.27.0", features = ["json","s3","aws","optimize","datafusion"] }  [oai_citation:16‡crates.io](https://crates.io/crates/deltalake)
object_store    = { version = "0.12.0", features = ["aws"] }
aws-config      = "1.8.0"
aws-sdk-s3      = "1.95.0"  [oai_citation:17‡docs.rs](https://docs.rs/crate/aws-sdk-s3/latest/source/Cargo.toml.orig?utm_source=chatgpt.com)
aws-sdk-dynamodb= "1.93.0"  [oai_citation:18‡crates.io](https://crates.io/crates/aws-sdk-dynamodb?utm_source=chatgpt.com)
serde           = { version = "1.0", features = ["derive"] }
serde_json      = "1.0"
toml            = "0.8"
config          = "0.14.0"  [oai_citation:19‡crates.io](https://crates.io/crates/deltalake/range/%5E0.17?utm_source=chatgpt.com)
clap            = { version = "4.5.4", features = ["derive"] }  [oai_citation:20‡crates.io](https://crates.io/crates/aws-sdk-s3/dependencies?utm_source=chatgpt.com)
tracing         = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
metrics         = "0.23"
metrics-exporter-prometheus = "0.15"  [oai_citation:21‡crates.io](https://crates.io/crates/polars-io?utm_source=chatgpt.com)
uuid            = { version = "1.7", features = ["v4"] }
thiserror       = "1.0"
anyhow          = "1.0"

[dev-dependencies]
testcontainers  = { version = "0.15.7", features=["minio","localstack"] }  [oai_citation:22‡crates.io](https://crates.io/crates/testcontainers?utm_source=chatgpt.com)
criterion       = { version = "0.5.1", features = ["html_reports"] }  [oai_citation:23‡crates.io](https://crates.io/crates/criterion?utm_source=chatgpt.com)
tokio           = { version = "1.37.0", features = ["macros","rt-multi-thread","test-util"] }
tempfile        = "3.8"

4  Minimal main.rs

//! Bin-entry: spawn individual commands or a long-running daemon.

mod config;
mod writer;
mod compactor;
mod vacuum;
mod locking;

use clap::{Parser, Subcommand};
use config::Config;

#[derive(Parser)]
#[command(name = "neuralake-writer")]
struct Cli {
    /// Path to configuration TOML
    #[arg(short, long, default_value = "config.toml")]
    config: String,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Run the low-latency writer once (for integration tests)
    Writer { table: String, input: String },
    /// Run a compaction pass (can be cron-ed)
    Compact { table: String, #[arg(long, default_value_t = false)] force: bool },
    /// Run a vacuum pass
    Vacuum  { table: String, #[arg(long, default_value_t = 168)] retain_hours: u64 },
    /// Spawn writer + compactor + vacuum as long-running daemon
    Daemon  { table: String, input: String },
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();
    let cfg = Config::from_file(&cli.config)?;
    match cli.command {
        Commands::Writer{table,input} => writer::run(&cfg,&table,&input).await?,
        Commands::Compact{table,force} => compactor::run(&cfg,&table,force).await?,
        Commands::Vacuum{table,retain_hours} => vacuum::run(&cfg,&table,retain_hours).await?,
        Commands::Daemon{table,input} => {
            //           ┌── writer     (tokio task 1)
            //           │
            // supervisor│── compactor (task 2, interval cfg.compaction.interval)
            //           │
            //           └── vacuum     (task 3, interval cfg.vacuum.interval)
            daemon::run(&cfg,&table,&input).await?;
        }
    }
    Ok(())
}

Tip: keep the file short; put real logic in writer.rs, compactor.rs, vacuum.rs, and daemon.rs for testability.

5  Sub-task breakdown (with changelog hooks)

ID	File(s) to touch	Acceptance criteria	Changelog tag
6.1	writer.rs, unit tests tests/writer_tests.rs	p99 latency < 250 ms on localhost MinIO; passes cargo test -p neuralake-writer writer	# Changelog: Task 6.1-Writer
6.2	compactor.rs	Merges ≥ 5 small files to single ≥ 128 MiB file; delta-rs OPTIMIZE succeeds	Task 6.2-Compaction
6.3	vacuum.rs	Removes obsolete files older than retention; table version increments	Task 6.3-Vacuum
6.4	locking.rs	Concurrent writer + compactor on CI docker-compose (LocalStack Dynamo) completes 500 commits without conflict	Task 6.4-Locking
6.5	daemon.rs, Prometheus exporter	/metrics endpoint exposes ingest_rows_total counter & compaction_duration_seconds histogram	Task 6.5-Daemon

💡 Changelog discipline: each PR must include /docs/reference/changelogs/YYYY-MM-DD-task-6.x-*.md summarising what changed, why, and perf numbers.

6  Test & CI matrix

Layer	Tooling	Command
Unit	cargo nextest	cargo nextest run -p neuralake-writer
Integration	testcontainers + MinIO + LocalStack	cargo test --test integration_minio
Bench	Criterion	cargo bench --bench writer_bench
Lint	cargo clippy --all-targets -- -D warnings	
Format	cargo fmt -- --check	

CI must run the full matrix on every PR branch.

⸻

📜 How this fits into the existing changelog cascade
	1.	Create docs/reference/changelogs/18-<date>-task-6-bootstrap.md on this commit summarising:
	•	crate versions logged above
	•	initial folder scaffold + unfinished compile status
	2.	Subsequent PRs (6.1 → 6.5) append 19-…, 20-…, etc.
	3.	Always include measured latency / throughput numbers in the changelog for transparency (mirrors Tasks 14 & 11 KPI work).

With these pinned versions, a clean starter scaffold, and explicit changelog hooks, the team can jump straight into TDD on each process while guaranteeing deterministic builds and crystal-clear historical context.