# Data Engineering Playground: A Blueprint for Modern Data Platforms

This repository is a hands-on playground for exploring the next generation of data engineering. It provides a tangible, runnable blueprint based on the architectural principles of high-performance data platforms like Neuralink's Neuralake.

The core philosophy is building **Simple Systems for Complex Data**, centered on two key ideas:
1.  **Code-as-Catalog:** The entire data landscape is defined, versioned, and queried as code. No GUIs, no separate services, no stale documentation. The code is the single source of truth.
2.  **Lightweight, Performant Tooling:** The stack is built on a foundation of Rust-based libraries (`polars`, `datafusion`) for maximum performance and a modern Python toolchain (`poetry`, `uv`) for a superior developer experience.

## Project Structure Overview

This repository is organized as follows:

-   `neuralake/`: Contains the core Neuralake demonstration project.
    -   `src/`: Python source code for the data platform (e.g., `my_tables.py`, `my_catalog.py`, `query_data.py`, `config.py`).
    -   `scripts/`: Utility and verification scripts (e.g., `production_verification.py`, `create_sample_data.py`).
    -   `docs/`: Documentation specific to the Neuralake component, including explanations, how-to guides, and API references.
    -   `pyproject.toml` & `poetry.lock`: Poetry configuration for managing dependencies.
-   `docs/`: (Currently, primary documentation is within `neuralake/docs/`)
-   `README.md`: This file, providing an overview of the entire playground.

## The Neuralake Demo: A Code-First Data Platform

The `neuralake/` directory contains a working demonstration that brings the "Code-as-Catalog" and "Lightweight Tooling" principles to life.

### Key Architectural Patterns Demonstrated:

*   **Declarative Data Catalog:** See how `neuralake/src/my_tables.py` and `neuralake/src/my_catalog.py` define a complete, queryable data catalog without a single line of configuration or a running server.
*   **Environment-Aware Configuration:** The `neuralake/src/config.py` module manages environment-specific settings (e.g., S3 endpoints, credentials) using the `NEURALAKE_ENV` environment variable (`local` or `production`).
*   **High-Performance ELT:** The `neuralake/src/query_data.py` script executes an ELT (Extract, Load, Transform) job, performing joins and transformations on raw data sources *on the fly*.
*   **Federated Querying:** The demo seamlessly joins data from a static Parquet file with a table generated dynamically from a Python function, showcasing the power of a unified query engine.
*   **Comprehensive Verification:** The `neuralake/scripts/production_verification.py` script provides a suite of tests to ensure the platform functions correctly in both local and production-simulated environments.
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
git clone <your-repo-url> # Replace with your repository URL
cd <your-repo-directory>  # Replace with your repository directory

# Navigate to the neuralake project directory
cd neuralake

# Install dependencies into a new virtual environment
poetry install

# Set the environment (optional, defaults to 'local')
# export NEURALAKE_ENV=local # or 'production' for production settings

# Run the query script to see it query data from the local S3 (MinIO) server
poetry run python src/query_data.py

# Run the verification tests
poetry run python scripts/production_verification.py
```

### Expected Output (from `query_data.py`)

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
The `production_verification.py` script will output test results.

## Explore Further

This playground is your starting point.
*   **Dive Deeper:** Read the detailed architectural breakdown in **[neuralake/docs/explanation/ONBOARDING.md](./neuralake/docs/explanation/ONBOARDING.md)**.
*   **Experiment:** Add a new data source in `neuralake/src/my_tables.py` (e.g., from a CSV or a live API).
*   **Build:** Write a new query in `neuralake/src/query_data.py` to perform more complex aggregations or transformations.
*   **Understand Configuration:** Examine `neuralake/src/config.py` to see how environment-specific settings are managed.