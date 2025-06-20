# Neuralake: A Code-First Data Platform Blueprint

This directory contains a working blueprint for a modern data platform, inspired by the principles behind Neuralink's Neuralake architecture. It's designed to bridge the high-level theory discussed in `docs/explanation/neuralake.md` with tangible, executable code.

This is not just a demo; it's a starter kit for building data systems where the entire data landscape is defined, versioned, and queried as code, powered by high-performance, Rust-based tools like Polars and DataFusion.

## 📚 **New to This? Start With Educational Resources**

If you're new to our catalog architecture, start with the comprehensive learning materials in the main repository:

### **🎓 3-Week Learning Path**
1. **Week 1: Architecture Concepts** - [`../docs/explanation/concepts/catalog-architecture-fundamentals.md`](../docs/explanation/concepts/catalog-architecture-fundamentals.md)
   - **START HERE** for complete architectural understanding
   - Hybrid architecture philosophy and design decisions
   - When to use function vs Delta vs Parquet tables
   - Production scaling patterns

2. **Week 2: Hands-On Tutorial** - [`../docs/tutorials/02-catalog-system-walkthrough.md`](../docs/tutorials/02-catalog-system-walkthrough.md)
   - **Build your first tables** with step-by-step guidance
   - Function tables, Delta tables, cross-type joins
   - Documentation generation workflow

3. **Week 3: Production & Context** - [`../docs/explanation/case-studies/01-debugging-neuralake-v0.0.5.md`](../docs/explanation/case-studies/01-debugging-neuralake-v0.0.5.md)
   - Real-world architectural decisions
   - Production deployment strategies

**Quick Outcomes:** After the learning path, you'll understand our hybrid architecture, table type decisions, unified query interface, and production considerations.

## AI-Native Development Philosophy

This project follows a sophisticated, AI-native development methodology designed for clarity, context, and effective collaboration between human and AI developers. The full philosophy, including our core workflow, documentation standards, and recommended tooling, is detailed in the root of the repository.

**Please read the [AI-Native Development Philosophy](../README.md#ai-native-development-philosophy) in the main `README.md` to understand our way of working.**

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
    Instead of GUIs or wikis, the entire data landscape is defined in Python. `src/demo_catalog.py` declares the available data sources, and `src/my_catalog.py` unifies them into a single, queryable catalog. This is the "code as a catalog" principle, made real.

2.  **Environment-Aware Configuration**
    The `src/config.py` module manages environment-specific settings (e.g., S3 endpoints, credentials) using the `NEURALAKE_ENV` environment variable. This allows seamless switching between `local` development (e.g., MinIO) and `production` (e.g., AWS S3) environments.

3.  **High-Performance, In-Process ELT**
    The project follows a modern ELT (Extract, Load, Transform) pattern. We load raw data sources (a Parquet file and in-memory functions) and then use the `neuralake` query engine to perform joins and transformations *on the fly* when a query is executed via `src/query_data.py`.

4.  **Federated Querying Across Diverse Sources**
    The `src/query_data.py` script seamlessly joins data from static Parquet files with tables generated dynamically from Python functions and Delta Lake tables with ACID guarantees. The query engine handles this federation, allowing you to treat disparate sources as if they were in the same database.

5.  **Comprehensive Verification**
    The `scripts/production_verification.py` script provides a suite of tests to ensure the platform functions correctly in both local and production-simulated environments. It tests configuration loading, table instantiation, catalog creation, and query execution.

6.  **The Power of a Rust-Based Stack**
    Under the hood, this entire system runs on Polars and Apache DataFusion. There is no JVM, no heavy Spark cluster required—just the raw performance of Rust for interactive-speed analytics, right on your laptop.

## 🚀 **"Code as a Catalog" System in Action**

### **Interactive Catalog Documentation**

The Static Site Generator (SSG) creates beautiful, browsable documentation automatically from your table definitions:

```bash
# Generate the interactive catalog site
python scripts/generate_demo_catalog_site.py

# Serve it locally for the best experience
cd demo-catalog-site && python3 -m http.server 8080
# Visit: http://localhost:8080
```

**What You'll See:**
- 📊 **Table Browser**: Search, filter, and explore all tables by name, tags, or description
- 🔍 **Rich Details**: Complete schemas, metadata, ownership information
- 📋 **Copy-Paste Code**: Working Python examples for every table
- 🛠️ **API Reference**: Complete documentation with live examples
- 🏷️ **Smart Organization**: Tables organized by tags and functionality

### **Demo Tables Showcase Different Patterns**

**Function Tables** (Dynamic, code-generated data):
```python
@table(description="User data with profiles", tags=["users", "core"])
def users():
    return pl.LazyFrame({
        "user_id": [1, 2, 3],
        "email": ["alice@neuralake.com", "bob@neuralake.com", "charlie@neuralake.com"]
    })
```

**Delta Tables** (ACID transactions, time travel):
```python
delta_table = NeuralakeDeltaTable("transactions")
register_static_table(
    delta_table, "transactions",
    description="Financial records with ACID guarantees",
    tags=["finance", "acid", "audit"]
)
```

### **Unified Query Interface**

All table types use the same Polars LazyFrame interface:

```python
from catalog_core import Catalog
catalog = Catalog()

# Same query patterns work across all table types
users = catalog.table("users")           # Function table
events = catalog.table("user_events")    # Function table
transactions = catalog.table("transactions")  # Delta table

# Complex analysis across different storage types
analysis = (
    users
    .join(events, on="user_id")
    .join(transactions, on="user_id") 
    .group_by("user_type")
    .agg([
        pl.count().alias("user_count"),
        pl.col("amount").sum().alias("total_revenue")
    ])
    .collect()
)
```

## Repository Structure

This `neuralake` project contains the core source code and scripts. All documentation has been centralized in the root `docs/` directory to provide a unified knowledge base for the entire repository.

*   `src/`: Core Python source code.
    *   `query_data.py`: 🚀 The main entry point for data querying. **Run this to see it work.**
    *   `demo_catalog.py`: 📚 Complete demo catalog with multiple table types and rich examples
    *   `my_tables.py`: 📋 Simple examples for learning (legacy, see demo_catalog.py for comprehensive examples)
    *   `my_catalog.py`: 🔧 Catalog configuration and site generation utilities
    *   `catalog_core.py`: ⚙️ Core catalog system with @table decorator and registration
    *   `config.py`: 🛠️ Environment-specific configuration management
    *   `delta_tables.py`: 🏗️ Delta Lake integration for ACID transactions
    *   `ssg.py`: 📖 Static Site Generator for automatic documentation
*   `scripts/`: Utility and operational scripts.
    *   `generate_demo_catalog_site.py`: 📚 **Generate the browsable catalog site**
    *   `demo_complete_workflow.py`: 🚀 **Complete end-to-end demo**
    *   `production_verification.py`: ✅ Comprehensive verification suite
    *   `create_sample_data.py`: 🏗️ Generate sample Parquet data
    *   `upload_sample_data_to_minio.py`: 📤 Upload data to local MinIO
*   `setup_minio.sh`: 🐳 Local MinIO S3-compatible server setup
*   `pyproject.toml`: 🔧 Core project configuration for Poetry
*   `poetry.lock`: 🔒 Lockfile for deterministic builds
*   `docker-compose.yml`: 🐳 MinIO service definition
*   `README.md`: This file

For the architectural deep-dive, please see **[The Neuralake Data Architecture](../docs/explanation/neuralake.md)** in the main documentation section.

## Code Quality

This project uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting to ensure consistent, high-quality code. Ruff is a fast Python linter and formatter written in Rust, providing the same speed philosophy as our data stack.

### Quick Commands

```bash
# Run all quality checks
python3 scripts/lint.py

# Auto-fix issues and format code
python3 scripts/lint.py --fix

# Only format code (no linting)
python3 scripts/lint.py --format-only

# Only check (no formatting)
python3 scripts/lint.py --check-only

# Or use Make targets for convenience
make help     # Show all available targets
make check    # Check code quality without fixing
make lint     # Run linting and formatting
make format   # Format code only
```

### Manual Commands

```bash
# Check for issues
poetry run ruff check .

# Auto-fix safe issues
poetry run ruff check . --fix

# Format all Python files
poetry run ruff format .

# Check formatting without changing files
poetry run ruff format --check .
```

### Configuration

Ruff configuration is in `pyproject.toml` under `[tool.ruff]`. Key settings:

- **Line length:** 88 characters (Black default)
- **Target Python:** 3.11+
- **Enabled rules:** pycodestyle, pyflakes, isort, flake8-bugbear, and more
- **Import sorting:** Groups imports with neuralake as first-party

### Pre-commit Workflow

Before committing code:

1. Run `python3 scripts/lint.py --fix` to auto-fix issues
2. Review and commit the changes
3. Ensure `python3 scripts/lint.py` passes with no errors

### Troubleshooting

**Import errors:**
```bash
# Ensure all dependencies are installed
poetry install
```

**Syntax errors:**
- Fix Python syntax issues first before running ruff

**Persistent formatting issues:**
```bash
# Check specific file
poetry run ruff check src/my_tables.py --verbose

# Get help on specific rule
poetry run ruff rule F401
```

### IDE Integration

**VS Code:**
Install the "Ruff" extension for real-time linting and formatting.

**PyCharm:**
Configure ruff as external tool or use the ruff plugin.

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
    This project uses a local MinIO server to simulate S3. **Ensure Docker Desktop is running first**, then start the server and create the necessary bucket:
    ```bash
    # Start MinIO and create the bucket
    bash setup_minio.sh
    ```
    **Requirements:**
    - Docker Desktop must be running
    - If you get "Cannot connect to the Docker daemon" error, start Docker Desktop first
    
    **Troubleshooting:**
    - If the script fails, ensure Docker is running: `docker ps` should work
    - The MinIO web interface will be available at http://localhost:9001 (admin/password)

3.  **Install Dependencies**
    From this `neuralake` directory, let Poetry work its magic.
    ```bash
    poetry install
    ```

4.  **Generate Sample Data**
    Next, generate the sample `parts.parquet` file. This creates a simple 5-row dataset for testing.
    ```bash
    # Generate the data (creates a simple 5-row sample)
    poetry run python scripts/create_sample_data.py
    ```

5.  **Upload the Data**
    Load the newly created Parquet file into your local MinIO server.
    ```bash
    # Upload the generated 'parts.parquet' file
    poetry run python scripts/upload_sample_data_to_minio.py
    ```

6.  **Configure Environment (Optional)**
    The system defaults to the `local` environment. To explicitly set it:
    ```bash
    export NEURALAKE_ENV=local
    # or for production-like settings (ensure relevant AWS env vars are set for real S3)
    # export NEURALAKE_ENV=production
    ```
    Refer to `src/config.py` for details on environment variables used.

7.  **Run the Complete Demo Workflow**
    Execute the comprehensive demo that showcases everything:
    ```bash
    poetry run python scripts/demo_complete_workflow.py
    ```
    This will:
    - Query all demo tables with analytics
    - Generate the browsable catalog site
    - Show you exactly how to explore the results
    - Provide copy-paste code examples

8.  **Browse the Interactive Catalog**
    Generate and explore the catalog documentation:
    ```bash
    # Generate the catalog site
    poetry run python scripts/generate_demo_catalog_site.py
    
    # Serve it locally (recommended)
    cd demo-catalog-site && python3 -m http.server 8080
    # Visit: http://localhost:8080
    ```

9.  **Run Individual Components**
    Test specific parts of the system:
    ```bash
    # Main query script (requires MinIO running)
    poetry run python src/query_data.py
    
    # Comprehensive verification tests
    poetry run python scripts/production_verification.py
    ```

### Expected Output (from `demo_complete_workflow.py`)

You will see comprehensive output showing:

```
🌐 Neuralake Demo Catalog Query (Local Environment)
📊 S3 Endpoint: http://localhost:9000
============================================================

📚 Available Tables in Catalog (6 total):
  • users               (function) - Enterprise user data with comprehensive user...
  • user_events         (function) - Real-time event stream data with user inter...
  • neural_signals      (function) - Neural signal data from research experiments...
  • data_quality_metrics(function) - Data quality metrics and validation results...
  • transactions       (delta   ) - Financial transaction records with ACID guar...
  • inventory           (delta   ) - Real-time inventory tracking with warehouse ...

============================================================
🔍 Running Demo Queries and Analytics...

[Detailed analytics and query results for each table type]

📚 Generating Interactive Catalog Site...
✅ Demo catalog site generated at: /path/to/demo-catalog-site
   Open: file:///path/to/demo-catalog-site/index.html

🎉 Complete workflow demonstration finished!
💡 Next steps:
   1. Browse the catalog site in your browser
   2. Explore table details and copy-paste code examples  
   3. Try the tutorial: ../docs/tutorials/02-catalog-system-walkthrough.md
   4. Read architecture concepts: ../docs/explanation/concepts/catalog-architecture-fundamentals.md
```

The `production_verification.py` script will output detailed test results.

## Beyond the Demo

This blueprint is your starting point. Fork it. Experiment with it.

### **Extend the Catalog System**

*   **Add Function Tables:** Define new tables in `src/demo_catalog.py` using the `@table` decorator:
    ```python
    @table(description="My team's data", tags=["team", "custom"])
    def my_team_data():
        return pl.LazyFrame({"metric": [1, 2, 3], "value": [10, 20, 30]})
    ```

*   **Register Delta Tables:** Add ACID-compliant tables for production data:
    ```python
    delta_table = NeuralakeDeltaTable("my_production_table")
    register_static_table(delta_table, "my_table", description="Production data with ACID")
    ```

*   **Add External Data Sources:** Read from CSV files, APIs, or databases:
    ```python
    @table(description="Live API data", tags=["external", "real-time"])
    def api_data():
        # In real implementation, call your API
        return pl.LazyFrame(fetch_from_api())
    ```

### **Advanced Query Patterns**

*   **Write complex queries:** Create new queries in `src/query_data.py` that perform aggregations, window functions, or more complex joins across different table types.

*   **Cross-source analytics:** Join function tables, Delta tables, and Parquet files in the same query using the unified Polars interface.

### **Configuration and Deployment**

*   **Add dependencies:** Use `poetry add <package-name>` to add new libraries and see UV install them in record time.

*   **Explore Configuration:** Modify `src/config.py` to add new configuration options or environments.

*   **Production deployment:** Follow the production guide at [`../docs/how-to/upgrade_dev_to_prod.md`](../docs/how-to/upgrade_dev_to_prod.md).

### **Learning and Development**

*   **Follow the tutorial:** Complete [`../docs/tutorials/02-catalog-system-walkthrough.md`](../docs/tutorials/02-catalog-system-walkthrough.md) to build your own tables step-by-step.

*   **Study real decisions:** Read [`../docs/explanation/case-studies/01-debugging-neuralake-v0.0.5.md`](../docs/explanation/case-studies/01-debugging-neuralake-v0.0.5.md) to understand how debugging experiences shaped our architecture.

*   **Contribute to the roadmap:** Check `.taskmaster/tasks/tasks.json` in the main repository to see what's being built next and how you can help.

**Quick test to verify everything is working:**
```bash
poetry run python scripts/demo_complete_workflow.py
```

This will run the complete demonstration, generate the catalog site, and show you exactly how to explore the results!
