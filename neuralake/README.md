# Neuralake: A Code-First Data Platform Blueprint

This repository contains a working blueprint for a modern data platform, inspired by the principles behind Neuralink's Neuralake architecture. It's designed to bridge the high-level theory discussed in the `ONBOARDING.md` with tangible, executable code.

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
    Instead of GUIs or wikis, the entire data landscape is defined in Python. `my_tables.py` declares the available data sources, and `my_catalog.py` unifies them into a single, queryable catalog. This is the "code as a catalog" principle, made real.

2.  **High-Performance, In-Process ELT**
    The project follows a modern ELT (Extract, Load, Transform) pattern. We load raw data sources (a Parquet file and an in-memory function) and then use the `neuralake` query engine to perform joins and transformations *on the fly* when a query is executed.

3.  **Federated Querying Across Diverse Sources**
    The `query_data.py` script seamlessly joins data from a static Parquet file with a table generated dynamically from a Python function. The query engine handles this federation, allowing you to treat disparate sources as if they were in the same database.

4.  **The Power of a Rust-Based Stack**
    Under the hood, this entire system runs on Polars and Apache DataFusion. There is no JVM, no heavy Spark cluster required—just the raw performance of Rust for interactive-speed analytics, right on your laptop.

## Repository Structure

*   `ONBOARDING.md`: 🧠 The deep-dive document. **Start here for the 'why'.**
*   `query_data.py`: 🚀 The main entry point. **Run this to see it work.**
*   `pyproject.toml`: 🔧 The core project configuration file for Poetry.
*   `my_tables.py`: 宣言 Where data sources are declared (from files, functions, etc.).
*   `my_catalog.py`: 📚 Unifies all declared tables into a single, queryable catalog.
*   `create_sample_data.py`: 🏗️ A simple utility to generate the sample Parquet data.

## Getting Started

Follow these steps to set up and run the project using the modern toolchain.

1.  **Install Poetry**
    If you don't have it, install it globally. The recommended method is via `pipx`.
    ```bash
    # Install pipx if you don't have it
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath

    # Install poetry
    pipx install poetry
    ```

2.  **Navigate to this Project and Install Dependencies**
    From the root of the repository, navigate into this project's directory and let Poetry work its magic.
    ```bash
    cd neuralake
    poetry install
    ```

3.  **Run the Query Script**
    Execute the main script using `poetry run`, which ensures it runs inside the project's managed environment.
    ```bash
    poetry run python query_data.py
    ```

### Expected Output
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

## Beyond the Demo

This blueprint is your starting point. Fork it. Experiment with it.
*   **Add a new data source:** Define a new table in `my_tables.py` that reads from a CSV file or pulls data from a live REST API.
*   **Write complex queries:** Create new queries in `query_data.py` that perform aggregations, window functions, or more complex joins.
*   **Add dependencies:** Use `poetry add <package-name>` to add new libraries and see UV install them in record time. 

## Setting up the Local S3 Environment (MinIO)

To work with cloud-scale features like Delta Lake, you first need to start the local S3-compatible storage service, MinIO.

1.  **Prerequisites:** Ensure you have `docker` and the `aws-cli` installed on your system.

2.  **Run the Setup Script:**
    Execute the provided script to start the MinIO container and create the necessary storage bucket.
    ```bash
    ./setup_minio.sh
    ```

3.  **Verify Setup:**
    After the script completes, you can access the MinIO web console at `http://localhost:9001` and log in with the credentials `minioadmin` / `minioadmin`. You should see the `neuralake-bucket` already created. 

4.  **Upload Sample Data:**
    Run the following command to upload the sample `parts.parquet` file to your new MinIO bucket.
    ```bash
    poetry run python upload_sample_data_to_minio.py
    ```

5.  **Query the S3 Data:**
    With the local S3 server running and data uploaded, you can now run the main query script.
    ```bash
    poetry run python query_data.py
    ```
