# Data Engineering Playground: A Blueprint for Modern Data Platforms

This repository is a hands-on playground for exploring the next generation of data engineering. It provides a tangible, runnable blueprint based on the architectural principles of high-performance data platforms like Neuralink's Neuralake.

The core philosophy is building **Simple Systems for Complex Data**, centered on two key ideas:
1.  **Code-as-Catalog:** The entire data landscape is defined, versioned, and queried as code. No GUIs, no separate services, no stale documentation. The code is the single source of truth.
2.  **Lightweight, Performant Tooling:** The stack is built on a foundation of Rust-based libraries (`polars`, `datafusion`) for maximum performance and a modern Python toolchain (`poetry`, `uv`) for a superior developer experience.

## The Demo: A Neuralake Blueprint

The `neuralake/` directory contains a working demonstration that brings these principles to life.

### Key Architectural Patterns Demonstrated:

*   **Declarative Data Catalog:** See how `my_tables.py` and `my_catalog.py` define a complete, queryable data catalog without a single line of configuration or a running server.
*   **High-Performance ELT:** The `query_data.py` script executes an ELT (Extract, Load, Transform) job, performing joins and transformations on raw data sources *on the fly*.
*   **Federated Querying:** The demo seamlessly joins data from a static Parquet file with a table generated dynamically from a Python function, showcasing the power of a unified query engine.
*   **Modern, Rust-Powered Stack:** The entire pipeline runs without a JVM or a heavy distributed cluster, highlighting the speed and efficiency of Polars and DataFusion for local development and production services.

## Quick Start

Follow these steps to get the demo running in minutes.

### 1. Prerequisites: Poetry & UV

This project uses a modern Python toolchain for robust dependency management and blazing-fast installation speed.

*   **Poetry:** A powerful dependency and packaging manager.
*   **UV:** An extremely fast package installer, written in Rust, used by Poetry to accelerate setup.

If you don't have them, install them with `pipx` (recommended):
```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install the tools
pipx install poetry
pipx install uv
```

### 2. Configure Poetry to use UV

Tell Poetry to use the UV installer. You only need to do this once.
```bash
poetry config virtualenvs.installer uv
```

### 3. Install & Run

Clone the repository and let Poetry handle the rest.

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-directory>

# Navigate to the neuralake project directory
cd neuralake

# Install dependencies into a new virtual environment
poetry install

# Run the query script to see it query data from the local S3 (MinIO) server
poetry run python query_data.py
```

### Expected Output

You will see a Polars DataFrame printed to the console, showing the result of querying the `parts.parquet` file stored in the local MinIO S3 bucket.

```
--- Querying 'part' table from S3 ---

Query successful! Fetched data from S3:
shape: (5, 4)
┌───────────┬──────────┬─────────┬───────────────┐
│ p_partkey ┆ p_name   ┆ p_brand ┆ p_retailprice │
│ ---       ┆ ---      ┆ ---     ┆ ---           │
│ i64       ┆ str      ┆ str     ┆ f64           │
╞═══════════╪══════════╪═════════╪═══════════════╡
│ 1         ┆ Part#1   ┆ Brand#1 ┆ 10.0          │
│ 2         ┆ Part#2   ┆ Brand#2 ┆ 20.0          │
│ 3         ┆ Part#3   ┆ Brand#3 ┆ 30.0          │
│ 4         ┆ Part#4   ┆ Brand#1 ┆ 40.0          │
│ 5         ┆ Part#5   ┆ Brand#2 ┆ 50.0          │
└───────────┴──────────┴─────────┴───────────────┘
```

## Explore Further

This playground is your starting point.
*   **Dive Deeper:** Read the detailed architectural breakdown in **[ONBOARDING.md](./neuralake/ONBOARDING.md)**.
*   **Experiment:** Add a new data source in `my_tables.py` (e.g., from a CSV or a live API).
*   **Build:** Write a new query in `query_data.py` to perform more complex aggregations or transformations.