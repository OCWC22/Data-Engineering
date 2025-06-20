# Production Data Engineering Simulation

[![CI Pipeline](https://github.com/OCWC22/Data-Engineering/workflows/CI%20Pipeline/badge.svg)](https://github.com/OCWC22/Data-Engineering/actions)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)

This repository is for learning how to build production grade enterprise level data engineering. It provides a tangible, runnable blueprint based on the architectural principles of high-performance data platforms like Neuralink's Neuralake.

https://www.youtube.com/watch?v=rVSb0u9OTtM&t=763s

## 🎯 **What We're Building: See TaskMaster for Complete Roadmap**

**Want to see EVERYTHING we're building?** 

👉 **Go to `.taskmaster/tasks/tasks.json`** - This is our comprehensive project roadmap with 17 detailed tasks

👉 **Or use TaskMaster CLI** to explore tasks interactively:
```bash
# See all tasks
poetry run taskmaster get-tasks --with-subtasks

# See next task to work on  
poetry run taskmaster next-task

# Get specific task details
poetry run taskmaster get-task --id 2
```

### Current Project Status (17 Tasks Total):
- ✅ **Task 1**: S3/MinIO Foundation (COMPLETE)
- 🚧 **Tasks 2-7**: Foundational improvements (Code quality, CI/CD, Delta Lake, Code-as-Catalog, Low-latency writer, Testing)
- 📋 **Tasks 8-17**: Blueprint expansion (Kafka, ROAPI, Performance benchmarking, Spark, Real-time pipelines, etc.)

**⚠️ IMPORTANT:** This isn't just a demo - we're building a **complete production data engineering platform** following Neuralink's exact architectural patterns. Each task has comprehensive subtasks with specific code, configurations, and implementation details.

## The Core Philosophy

The core philosophy is building **Simple Systems for Complex Data**, centered on two key ideas:
1.  **Code-as-Catalog:** The entire data landscape is defined, versioned, and queried as code. No GUIs, no separate services, no stale documentation. The code is the single source of truth.
2.  **Lightweight, Performant Tooling:** The stack is built on a foundation of Rust-based libraries (`polars`, `datafusion`) for maximum performance and a modern Python toolchain (`poetry`, `uv`) for a superior developer experience.

## Project Structure & Documentation

This repository follows a structured layout to separate concerns and make the project, especially its documentation, easy to navigate for both humans and AI agents.

-   **`.taskmaster/`**: **🎯 START HERE** - Complete project planning system
    -   `tasks/tasks.json`: **Master roadmap** with all 17 tasks and detailed subtasks
    -   `docs/prd.txt`: Product Requirements Document explaining the full vision
-   `docs/`: The central hub for all documentation. It follows a framework inspired by [Diátaxis](https://diataxis.fr/), organized into:
    -   `explanation/`: High-level concepts, architectural deep-dives, and case studies (e.g., `neuralake.md`).
    -   `how-to/`: Practical, step-by-step guides for specific tasks (e.g., `upgrade_dev_to_prod.md`).
    -   `tutorials/`: Learning-oriented, hands-on walkthroughs.
    -   `reference/`: Technical descriptions, API documentation, and changelogs.
-   `neuralake/`: Contains the core Neuralake demonstration project.
    -   `src/`: Python source code for the data platform (`my_tables.py`, `my_catalog.py`, `query_data.py`, `config.py`).
    -   `scripts/`: Utility and verification scripts (`production_verification.py`, `create_sample_data.py`).
    -   `pyproject.toml` & `poetry.lock`: Poetry configuration for managing dependencies.
-   `README.md`: This file, providing an overview of the entire playground.

## What Makes This Project Special: Neuralink's Architecture

We're implementing the **exact** data engineering patterns described by Neuralink's engineering team:

### 🏗️ **Dual-Engine Architecture:**
- **"Surgical Strike" (Rust Stack):** Polars + DataFusion + ROAPI for low-latency, high-performance operations
- **"Workhorse" (Spark Stack):** Apache Spark for large-scale, distributed ELT operations
- Both engines operate on the same Delta Lake storage

### 🔧 **Technology Stack:**
- **Rust** for performance-critical components (writer, query engine, API layer)
- **Polars** as the standard DataFrame library for all non-Spark operations  
- **Delta Lake** for all transactional storage with ACID guarantees
- **Apache DataFusion** for embeddable query processing
- **ROAPI** for auto-generated, high-performance SQL APIs

### 🚀 **Key Components We're Building:**
1. **Low-Latency "Surgical Strike" Writer** (Rust-based, 3-process architecture)
2. **Code-as-Catalog System** (Define tables in code, generate APIs automatically)
3. **Auto-Generated SQL APIs** (ROAPI + DataFusion, no custom API code)
4. **Real-time Streaming Pipeline** (Kafka → Writer → Delta → ROAPI)
5. **Performance Benchmarking** (Comparing "surgical strike" vs "workhorse" engines)

**📖 For the complete technical deep-dive, see [docs/explanation/neuralake.md](./docs/explanation/neuralake.md)**

## An AI-Native Development Philosophy

This project is more than just code; it's a living blueprint for a new way of building software. It's an **AI-native workflow** designed from the ground up to be understood, maintained, and enhanced by both human developers and AI coding agents.

Our methodology is built on four pillars: **Communication, Documentation, Organization, and Architecture.** The goal is to eliminate ambiguity and provide deep context, treating our AI counterparts like brilliant but inexperienced interns who thrive on clarity.

### The Heart of the Project: The `docs/` Folder

The `docs/` directory is the soul of this repository. It's where the "why" behind every decision lives. Before a single line of code is written for a new feature, its purpose, design, trade-offs, and implementation strategy are documented here. This ensures that any developer—human or AI—can onboard quickly and contribute meaningfully without getting lost.

### The Core Workflow: A Cycle of Deliberate Action

We follow a structured, iterative process designed to ensure that every change is well-planned, researched, and documented.

1.  **Plan with Taskmaster:** Every new feature begins in **[Taskmaster](https://github.com/eyaltoledano/claude-task-master)**. We create a Product Requirements Document (`.taskmaster/docs/prd.txt`) and use Taskmaster to generate a detailed, structured plan. This is our single source of truth for what needs to be built.

2.  **Deep Research & Refinement:** With a plan in hand, we turn to external, specialized AI tools for deep research. We use reasoning models (like Claude 4 Sonnet Thinking or Gemini 2.5 Pro with Extended Thinking in Google AI Studio, o3) paired with research tools that have full web and social access (like Perplexity) to validate our approach against the latest best practices, library documentation, and security advisories. The findings from this research are used to refine the plan. 

3.  **Implement:** With a research-backed plan, we begin coding.

4.  **Test:** We rigorously verify that the implementation works as expected.

5.  **Document with Changelogs:** Upon completion, we create a new, permanent record in the `docs/reference/changelogs/` directory. This is not just a list of changes; it's a narrative that explains the "why," the trade-offs, and the reasoning behind the implementation, providing invaluable context for future work.

### Changelog as Catalog: The Project's Memory

Our changelog is our institutional memory. Each entry is a standalone file, making it version-controlled, auditable, and easily discoverable.

-   **Naming Convention:** We follow a strict format: `XX-YYYY-MM-DD-brief-description.md`, where `XX` is a zero-padded sequential number. This provides chronological order and versioning at a glance.
-   **Content Structure:** Each changelog provides deep context, including the Taskmaster task ID, a summary of changes, the reasoning behind key decisions, and any trade-offs made. This is critical for preventing confusion and enabling effective collaboration with AI agents.
-   **Example in Practice:** The `neuralake` library has no public API documentation. We had to reverse-engineer it. Our findings and the script used to generate the docs are recorded in changelog `05-2025-06-19-api-docs-generation.md`, preserving that knowledge forever.

### Recommended Toolchain: The MCP-Powered IDE

To fully embrace this AI-native workflow, we strongly recommend an IDE integrated with **MCP (Model Control Protocol)** servers. This turns your editor into a powerful, context-aware development environment.

Our recommended stack of MCPs includes:

1.  **[Task Master](https://github.com/eyaltoledano/claude-task-master):** (ESSENTIAL) The core of our project management system - see tasks, update status, get next steps
2.  **[Context7](https://context.ai/):** (HIGHLY RECOMMENDED) Provides always-up-to-date documentation for any library, directly in your IDE. It's more reliable than any web search.
3.  **Sequential Thinking:** Turns any base model into a powerful reasoning engine, perfect for planning and problem-solving.
4.  **Others:** Explore other MCPs like **Supabase** (for database work), or find ones that suit your workflow on **[Smithery](https://smithery.ai/)**, **Glama**, or **Composio**. You can build your own if you don't find the one you want. 

I recommend using Smithery because it's the easiest way to setup external MCPs to your IDE. Cursor, Windsurf, Trae have started offering toggle MCP servers, explore those first.

For setup instructions, see the **[How to Set Up Taskmaster Guide](./docs/how-to/setup-taskmaster.md)**.

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

## Code Quality

This project uses `ruff` for code linting and formatting. The configuration can be found in `neuralake/ruff.toml`.

To check for issues and apply automatic fixes, run the following command from the `neuralake` directory:
```bash
poetry run ruff check --fix .
```

To simply check for issues without applying fixes, run:
```bash
poetry run ruff check .
```

## Explore Further

This playground is your starting point.
*   **🎯 MOST IMPORTANT: Check `.taskmaster/tasks/tasks.json`** to see our complete 17-task roadmap
*   **📋 Use TaskMaster:** Install the MCP and interact with tasks via natural language
*   **Dive Deeper:** Read the detailed architectural breakdown in **[docs/explanation/neuralake.md](./docs/explanation/neuralake.md)**.
*   **Experiment:** Add a new data source in `neuralake/src/my_tables.py` (e.g., from a CSV or a live API).
*   **Build:** Write a new query in `neuralake/src/query_data.py` to perform more complex aggregations or transformations.
*   **Understand Configuration:** Examine `neuralake/src/config.py` to see how environment-specific settings are managed.