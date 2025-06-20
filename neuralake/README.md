# Neuralake: A Code-First Data Platform Blueprint

This directory contains a working blueprint for a modern data platform, inspired by the principles behind Neuralink's Neuralake architecture. It's designed to bridge the high-level theory discussed in `docs/explanation/ONBOARDING.md` with tangible, executable code.

This is not just a demo; it's a starter kit for building data systems where the entire data landscape is defined, versioned, and queried as code, powered by high-performance, Rust-based tools like Polars and DataFusion.

## Why Poetry & UV? A Modern Python Stack

The tooling for a project should reflect its philosophy. A high-performance, Rust-based data stack deserves a high-performance, modern Python development environment. That's why this project uses **Poetry** for dependency management and **UV** for installation.

*   **For Dependency Management: Poetry**
    Poetry replaces the traditional `requirements.txt` file with `pyproject.toml`, the modern standard for configuring Python projects. It creates a `poetry.lock` file to guarantee deterministic, reproducible builds across all developer machines and CI/CD environments. This eliminates "it works on my machine" issues.

*   **For Blazing-Fast Installation: UV**
    UV is a next-generation package installer and resolver, written in Rust. It serves as a drop-in replacement for `pip` and is orders of magnitude faster. By configuring Poetry to use UV, we dramatically accelerate the initial setup and any subsequent dependency updates, significantly improving the developer experience.

Using them together gives us the best of both worlds: robust, modern dependency management and unparalleled installation speed.

## Architectural Principles in Action

This blueprint demonstrates the core tenets of the Neuralake philosophy in a way you can run on your own machine.

1.  **A Declarative, Code-First Catalog**
    Instead of GUIs or wikis, the entire data landscape is defined in Python. `src/my_tables.py` declares the available data sources, and `src/my_catalog.py` unifies them into a single, queryable catalog. This is the "code as a catalog" principle, made real.

2.  **Environment-Aware Configuration**
    The `src/config.py` module manages environment-specific settings (e.g., S3 endpoints, credentials) using the `NEURALAKE_ENV` environment variable. This allows seamless switching between `local` development (e.g., MinIO) and `production` (e.g., AWS S3) environments.

3.  **High-Performance, In-Process ELT**
    The project follows a modern ELT (Extract, Load, Transform) pattern. We load raw data sources (a Parquet file and an in-memory function) and then use the `neuralake` query engine to perform joins and transformations *on the fly* when a query is executed via `src/query_data.py`.

4.  **Federated Querying Across Diverse Sources**
    The `src/query_data.py` script seamlessly joins data from a static Parquet file with a table generated dynamically from a Python function. The query engine handles this federation, allowing you to treat disparate sources as if they were in the same database.

5.  **Comprehensive Verification**
    The `scripts/production_verification.py` script provides a suite of tests to ensure the platform functions correctly in both local and production-simulated environments. It tests configuration loading, table instantiation, catalog creation, and query execution.

6.  **The Power of a Rust-Based Stack**
    Under the hood, this entire system runs on Polars and Apache DataFusion. There is no JVM, no heavy Spark cluster required—just the raw performance of Rust for interactive-speed analytics, right on your laptop.

## Repository Structure

*   `docs/`: Contains all documentation.
    *   `explanation/ONBOARDING.md`: 🧠 The deep-dive document. **Start here for the 'why'.**
    *   `reference/changelogs/`: Detailed changelogs for development iterations.
*   `src/`: Core Python source code.
    *   `query_data.py`: 🚀 The main entry point for data querying. **Run this to see it work.**
    *   `my_tables.py`: 宣言 Where data sources are declared (from files, functions, etc.).
    *   `my_catalog.py`: 📚 Unifies all declared tables into a single, queryable catalog.
    *   `config.py`: ⚙️ Manages environment-specific configurations.
*   `scripts/`: Utility and operational scripts.
    *   `production_verification.py`: ✅ Script to verify the platform in different environments.
    *   `create_sample_data.py`: 🏗️ Utility to generate sample Parquet data for local testing.
    *   `setup_minio.sh`: 🐳 Script to set up a local MinIO S3-compatible server using Docker.
    *   `upload_sample_data_to_minio.py`: 📤 Script to upload sample data to the local MinIO server.
*   `pyproject.toml`: 🔧 The core project configuration file for Poetry.
*   `poetry.lock`: 🔒 Lockfile for deterministic, reproducible builds.
*   `docker-compose.yml`: 🐳 Defines the local MinIO service for S3 emulation.
*   `README.md`: This file.

## Getting Started

Follow these steps to set up and run the project using the modern toolchain.

1.  **Install Poetry & UV**
    If you don't have them, install them globally. The recommended method is via `pipx`.
    ```bash
    # Install pipx if you don't have it
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath

    # Install poetry and uv
    pipx install poetry
    pipx install uv
    ```
    Then, configure Poetry to use UV (one-time setup):
    ```bash
    poetry config virtualenvs.installer uv
    ```

2.  **Set up Local S3 Environment (MinIO)**
    This project uses a local MinIO server to simulate S3.
    ```bash
    # Start MinIO and create the bucket
    bash scripts/setup_minio.sh

    # Upload sample data
    poetry run python scripts/upload_sample_data_to_minio.py
    ```
    Ensure Docker is running before executing `setup_minio.sh`.

3.  **Install Dependencies**
    From this `neuralake` directory, let Poetry work its magic.
    ```bash
    poetry install
    ```

4.  **Configure Environment (Optional)**
    The system defaults to the `local` environment. To explicitly set it:
    ```bash
    export NEURALAKE_ENV=local
    # or for production-like settings (ensure relevant AWS env vars are set for real S3)
    # export NEURALAKE_ENV=production
    ```
    Refer to `src/config.py` for details on environment variables used.

5.  **Run the Query Script**
    Execute the main script using `poetry run`, which ensures it runs inside the project's managed environment.
    ```bash
    poetry run python src/query_data.py
    ```

6.  **Run Verification Tests**
    To ensure everything is configured and working correctly:
    ```bash
    poetry run python scripts/production_verification.py
    ```

### Expected Output (from `src/query_data.py`)
You will see a Polars DataFrame printed to the console, showing the result of querying the `parts.parquet` file from your local MinIO S3 bucket.

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
The `production_verification.py` script will output detailed test results.

## Beyond the Demo

This blueprint is your starting point. Fork it. Experiment with it.
*   **Add a new data source:** Define a new table in `src/my_tables.py` that reads from a CSV file or pulls data from a live REST API.
*   **Write complex queries:** Create new queries in `src/query_data.py` that perform aggregations, window functions, or more complex joins.
*   **Add dependencies:** Use `poetry add <package-name>` to add new libraries and see UV install them in record time.
*   **Explore Configuration:** Modify `src/config.py` to add new configuration options or environments.
    ```bash
    poetry run python query_data.py
    ```
