# Production Data Engineering Simulation

[![CI Pipeline](https://github.com/OCWC22/Data-Engineering/workflows/CI%20Pipeline/badge.svg)](https://github.com/OCWC22/Data-Engineering/actions)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)

This repository is for learning how to build production grade enterprise level data engineering. It provides a tangible, runnable blueprint based on the architectural principles of high-performance data platforms like Neuralink's Neuralake.

https://www.youtube.com/watch?v=rVSb0u9OTtM&t=763s

## 🎯 **What We're Building: See TaskMaster for Complete Roadmap**

**Want to see EVERYTHING we're building?** 

👉 **Go to `.taskmaster/tasks/tasks.json`** - This is our comprehensive project roadmap with detailed tasks

👉 **Or use TaskMaster via MCP tools** if you have the MCP server set up in your IDE (Cursor/Windsurf):
```bash
# See all tasks (via MCP tools in IDE)
# get_tasks tool with withSubtasks=true

# See next task to work on  
# next_task tool

# Get specific task details
# get_task tool with id parameter
```

### Current Project Status (17+ Tasks Total):
- ✅ **Task 1**: S3/MinIO Foundation (COMPLETE - 4/4 subtasks)
- ✅ **Task 2**: Code Quality Tooling (COMPLETE - 4/4 subtasks) 
- ✅ **Task 3**: CI/CD Pipeline (COMPLETE - 6/6 subtasks)
- ✅ **Task 4**: Delta Lake Implementation (COMPLETE - 4/4 subtasks)
- ✅ **Task 5**: Code-as-Catalog System (COMPLETE - 5/5 subtasks)
- 🚧 **Task 6**: "Surgical Strike" Writer (**Foundation Complete, Real Implementation Needed**)
- ⏳ **Tasks 7-17**: Testing framework, Kafka streams, ROAPI, Spark integration, etc. (pending Task 6)

**⚠️ IMPORTANT:** This isn't just a demo - we're building a **complete production data engineering platform** following Neuralink's exact architectural patterns. 

**Current Progress: 5/17 Tasks Complete (29.4%)**
- **Tasks 1-5**: Fully implemented with comprehensive subtasks, tests, and production-ready code
- **Task 6**: Infrastructure foundation complete (compatible dependencies, TDD test framework, project structure) but **core implementation still needed**
- **Tasks 7-17**: Ready to start once Task 6 real implementation is complete

## 📚 **Learning & Onboarding: Start Here for Education**

### **🎓 New Engineer Learning Path (3 Weeks)**

**Week 1: Understanding the Architecture**
1. **Read Core Concepts**: [`docs/explanation/concepts/catalog-architecture-fundamentals.md`](./docs/explanation/concepts/catalog-architecture-fundamentals.md) - **START HERE**
   - Hybrid architecture philosophy 
   - When to use function vs Delta vs Parquet tables
   - Unified query interface with Polars LazyFrames
   - Production scaling patterns
2. **High-Level Philosophy**: [`docs/explanation/neuralake.md`](./docs/explanation/neuralake.md)
3. **Environment Setup**: [`docs/tutorials/01-foundations-lakehouse-ingestion.md`](./docs/tutorials/01-foundations-lakehouse-ingestion.md)

**Week 2: Hands-On Implementation**
1. **Hands-On Tutorial**: [`docs/tutorials/02-catalog-system-walkthrough.md`](./docs/tutorials/02-catalog-system-walkthrough.md) - **Build Your First Tables**
   - Create function tables with `@table` decorator
   - Set up Delta tables for ACID transactions
   - Join data across different table types
   - Generate automatic documentation
2. **SSG Deep Dive**: [`docs/explanation/concepts/code-as-catalog-ssg.md`](./docs/explanation/concepts/code-as-catalog-ssg.md)

**Week 3: Production & Real-World Context**
1. **Real-World Decisions**: [`docs/explanation/case-studies/01-debugging-neuralake-v0.0.5.md`](./docs/explanation/case-studies/01-debugging-neuralake-v0.0.5.md)
2. **Production Deployment**: [`docs/how-to/upgrade_dev_to_prod.md`](./docs/how-to/upgrade_dev_to_prod.md)
3. **Implement Real Tables**: Apply learnings to your team's actual data

### **🎯 Quick Learning Outcomes**

After completing the learning path, you'll understand:
- **Why we built a hybrid catalog architecture** instead of pure external dependency
- **How the `@table` decorator and static table registration work together**  
- **When to use function tables vs Delta tables vs Parquet tables**
- **How configuration enables local development → production deployment**
- **The relationship between catalog metadata and static site generation**

### **📖 Documentation Architecture**

Our documentation follows the [Diátaxis framework](https://diataxis.fr/) for maximum learning effectiveness:

```
docs/
├── explanation/          # WHY we built it this way
│   ├── concepts/         # Core architectural concepts
│   ├── case-studies/     # Real-world experiences  
│   └── neuralake.md      # High-level philosophy
├── tutorials/            # HOW to build it yourself  
│   ├── 01-foundations-lakehouse-ingestion.md
│   └── 02-catalog-system-walkthrough.md
├── how-to/              # PRACTICAL guides for specific tasks
│   ├── setup-taskmaster.md
│   └── upgrade_dev_to_prod.md
└── reference/           # TECHNICAL specifications
    ├── api/             # API documentation
    └── changelogs/      # Complete change history
```

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
    -   `src/`: Python source code for the data platform (`demo_catalog.py`, `my_catalog.py`, `query_data.py`, `config.py`).
    -   `scripts/`: Utility and verification scripts (`production_verification.py`, `create_sample_data.py`).
    -   `pyproject.toml` & `poetry.lock`: Poetry configuration for managing dependencies.
-   `README.md`: This file, providing an overview of the entire playground.

## The Core Philosophy

The core philosophy is building **Simple Systems for Complex Data**, centered on two key ideas:
1.  **Code-as-Catalog:** The entire data landscape is defined, versioned, and queried as code. No GUIs, no separate services, no stale documentation. The code is the single source of truth.
2.  **Lightweight, Performant Tooling:** The stack is built on a foundation of Rust-based libraries (`polars`, `datafusion`) for maximum performance and a modern Python toolchain (`poetry`, `uv`) for a superior developer experience.

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

## 🚀 **Working Demo: "Code as a Catalog" System**

Our catalog system demonstrates the complete philosophy in action. See it working:

### **Browse the Live Demo Catalog**

The Static Site Generator (SSG) creates beautiful, interactive documentation from your table definitions:

```bash
cd neuralake
python scripts/generate_demo_catalog_site.py

# Open demo-catalog-site/index.html in your browser
# Or serve it locally:
cd demo-catalog-site && python3 -m http.server 8080
# Then visit: http://localhost:8080
```

**What you'll see:**
- 📊 **Interactive Table Browser**: Search, filter, and explore all tables
- 🔍 **Rich Table Details**: Schemas, examples, metadata, owner information
- 📋 **Copy-Paste Code**: Working Python examples for every table
- 🛠️ **API Reference**: Complete documentation with live examples
- 🏷️ **Tag-Based Organization**: Tables organized by functionality

### **Example Tables Available**

**Function Tables** (Dynamic, code-generated):
- `users` - Enterprise user data with comprehensive profiles
- `user_events` - Real-time event stream with user interactions  
- `neural_signals` - Neural signal recordings from research experiments
- `data_quality_metrics` - Data quality monitoring and validation results

**Static Tables** (Delta Lake with ACID guarantees):
- `transactions` - Financial transaction records with audit trails
- `inventory` - Real-time inventory tracking with warehouse locations

### **Unified Query Interface**

Despite different storage types, everything uses the same Polars LazyFrame interface:

```python
from catalog_core import Catalog
catalog = Catalog()

# All return Polars LazyFrames - same interface regardless of source
users = catalog.table("users")                    # Function table
events = catalog.table("user_events")             # Function table  
transactions = catalog.table("transactions")      # Delta table
inventory = catalog.table("inventory")            # Delta table

# Same query patterns work across all types
analysis = (
    users
    .join(events, on="user_id")
    .join(transactions, on="user_id")
    .filter(pl.col("is_active") == True)
    .group_by("user_type")
    .agg([
        pl.count().alias("user_count"),
        pl.col("amount").sum().alias("total_spent")
    ])
    .collect()  # Only executes when you call .collect()
)
```

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
2.  **[Context7](https://github.com/upstash/context7):** (HIGHLY RECOMMENDED) Provides always-up-to-date documentation for any library, directly in your IDE. It's more reliable than any web search.
3.  **Sequential Thinking:** Turns any base model into a powerful reasoning engine, perfect for planning and problem-solving.
4.  **Others:** Explore other MCPs like **Supabase** (for database work), or find ones that suit your workflow on **[Smithery](https://smithery.ai/)**, **Glama**, or **Composio**. You can build your own if you don't find the one you want. 

I recommend using Smithery because it's the easiest way to setup external MCPs to your IDE. Cursor, Windsurf, Trae have started offering toggle MCP servers, explore those first.

For setup instructions, see the **[How to Set Up Taskmaster Guide](./docs/how-to/setup-taskmaster.md)**.

## The Neuralake Demo: A Code-First Data Platform

The `neuralake/` directory contains a working demonstration that brings the "Code-as-Catalog" and "Lightweight Tooling" principles to life.

### 📁 **Source Architecture Breakdown (`neuralake/src/`)**

Our `src/` directory implements a **layered architecture** following the "Code as a Catalog" philosophy:

```
┌─────────────────────────────────────────────────┐
│             📊 Application Layer                │
├─────────────────────────────────────────────────┤
│   demo_catalog.py   │   my_catalog.py           │
│   my_tables.py      │   query_data.py           │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│             🌐 Documentation Layer              │
├─────────────────────────────────────────────────┤
│              ssg.py (32KB)                      │
│        Static Site Generator                    │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│              📚 Catalog Layer                   │
├─────────────────────────────────────────────────┤
│            catalog_core.py (11KB)               │
│         @table decorator + Registry             │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│              🗄️ Data Layer                      │
├─────────────────────────────────────────────────┤
│  delta_tables.py  │  delta_config.py            │
│     (13KB)        │     (6KB)                   │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│           ⚙️ Infrastructure Layer               │
├─────────────────────────────────────────────────┤
│             config.py (21KB)                    │
│     Environment + S3 + Security                │
└─────────────────────────────────────────────────┘
```

#### **Key Files Explained:**

**🏗️ Infrastructure Foundation:**
- **`config.py` (21KB)**: Production-ready configuration management
  - Environment-aware: `LOCAL`, `DEVELOPMENT`, `STAGING`, `PRODUCTION`
  - Security: Credential management, encryption settings
  - Performance: Connection pools, caching, parallelism controls
  - Data Quality: Validation thresholds, schema enforcement

**🗄️ Data Management:**
- **`delta_tables.py` (13KB)**: Delta Lake wrapper with ACID guarantees
  - Transactional operations: `create_table()`, `insert()`, `query()`
  - Time travel queries and audit trails
  - Schema evolution and optimization
- **`delta_config.py` (6KB)**: Delta Lake-specific configurations

**📚 Catalog Engine:**
- **`catalog_core.py` (11KB)**: Heart of "Code as a Catalog" system
  - `@table` decorator for auto-discovery
  - `CatalogRegistry` for metadata management
  - Unified `pl.LazyFrame` interface for all table types

**🌐 Documentation Generation:**
- **`ssg.py` (32KB)**: Static Site Generator (largest file)
  - Interactive HTML catalog with search/filtering
  - Auto-generated API documentation
  - Copy-paste code examples
  - Modern responsive design

**📊 Application Examples:**
- **`demo_catalog.py` (11KB)**: Comprehensive demo with 6 tables
  - Function tables: `users`, `events`, `neural_signals`, `quality_metrics`
  - Static tables: `transactions`, `inventory`
  - Rich metadata with schemas, partitions, ownership
- **`my_tables.py` (5.5KB)**: Production patterns example
- **`my_catalog.py` (1.6KB)**: Simple catalog setup
- **`query_data.py` (5.4KB)**: Usage examples and patterns

#### **🔄 Data Flow Through Architecture:**

```
1. 📝 Define Tables
   └── @table decorator or register_static_table()

2. 📚 Auto-Registration  
   └── CatalogRegistry stores metadata + functions

3. 🔍 Query Interface
   └── catalog.table("name") → pl.LazyFrame

4. 📊 Unified API
   └── All tables return Polars LazyFrames

5. 🌐 Documentation
   └── SSG generates browsable HTML docs

6. 🔧 Configuration
   └── Environment-aware settings drive behavior
```

### Key Architectural Patterns Demonstrated:

*   **Declarative Data Catalog:** See how `neuralake/src/my_tables.py` and `neuralake/src/my_catalog.py` define a complete, queryable data catalog without a single line of configuration or a running server.
*   **Environment-Aware Configuration:** The `neuralake/src/config.py` module manages environment-specific settings (e.g., S3 endpoints, credentials) using the `NEURALAKE_ENV` environment variable (`local` or `production`).
*   **High-Performance ELT:** The `neuralake/src/query_data.py` script executes an ELT (Extract, Load, Transform) job, performing joins and transformations on raw data sources *on the fly*.
*   **Federated Querying:** The demo seamlessly joins data from a static Parquet file with a table generated dynamically from a Python function, showcasing the power of a unified query engine.
*   **Comprehensive Verification:** The `neuralake/scripts/production_verification.py` script provides a suite of tests to ensure the platform functions correctly in both local and production-simulated environments.
*   **Modern, Rust-Powered Stack:** The entire pipeline runs without a JVM or a heavy distributed cluster, highlighting the speed and efficiency of Polars and DataFusion for local development and production services.

## Quick Start

Follow these steps to get the **working components** running. Note that Docker is **required** for the S3 simulation (MinIO).

### 1. Prerequisites: Poetry, UV & Docker Desktop

This project uses a modern Python toolchain and requires Docker for local S3 simulation.

**Required:**
- **Docker Desktop**: Must be running for MinIO (S3 simulation)
- **Poetry**: Dependency and packaging manager
- **UV**: Fast package installer (used by Poetry)

If you don't have them, install with `pipx` (recommended):
```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install the tools
pipx install poetry
pipx install uv

# Ensure Docker Desktop is installed and running
# Download from: https://www.docker.com/products/docker-desktop/
```

### 2. Configure Poetry to use UV

Tell Poetry to use the UV installer (one-time setup):
```bash
poetry config virtualenvs.installer uv
```

### 3. Start MinIO (Required for S3 Simulation)

**IMPORTANT**: Start Docker Desktop first, then:
```bash
# Clone and navigate to repository
git clone <your-repo-url>
cd <your-repo-directory>

# Start MinIO S3 server and create bucket
cd neuralake
bash setup_minio.sh
```

### 4. Install Dependencies & Test

```bash
# Install Python dependencies
poetry install

# Generate sample data
poetry run python scripts/create_sample_data.py

# Upload data to MinIO
poetry run python scripts/upload_sample_data_to_minio.py

# Test the query system (requires MinIO running)
poetry run python src/query_data.py

# Run comprehensive verification tests
poetry run python scripts/production_verification.py
```

### 5. Generate and Browse the Catalog Site

```bash
# Generate the interactive catalog documentation
poetry run python scripts/generate_demo_catalog_site.py

# Open in browser - two options:

# Option 1: Direct file access
open demo-catalog-site/index.html

# Option 2: Local web server (recommended)
cd demo-catalog-site && python3 -m http.server 8080
# Then visit: http://localhost:8080
```

### Expected Output

If everything is working, `poetry run python src/query_data.py` will show:

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
🔍 Running Demo Queries...

1️⃣  Querying 'users' table (Function Table):
✅ Successfully fetched user data: (5, 7)
┌─────────┬─────────────┬──────────────────────┬─────────────────────┬─────────────────────┬───────────┬───────────┐
│ user_id ┆ username    ┆ email                ┆ created_at          ┆ last_login          ┆ is_active ┆ user_type │
...
🎉 Demo catalog queries completed!
💡 To generate a browsable catalog site, run:
   python -c "from src.my_catalog import generate_catalog_site; generate_catalog_site()"
   Then open the generated HTML file in your browser
```

### Troubleshooting

**S3 Connection Errors**: Ensure Docker Desktop is running and MinIO was started successfully:
```bash
# Check if Docker is running
docker ps

# Check if MinIO container is running
docker ps | grep minio

# Restart MinIO if needed
bash setup_minio.sh
```

**"Cannot connect to Docker daemon"**: Start Docker Desktop application first.

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

## 🚀 What's Next: Current Development Priorities

### **Immediate Priority: Complete Task 6 - Rust "Surgical Strike" Writer**

**Status**: 🚧 Foundation Complete, **Core Implementation Gap**

**✅ FOUNDATION COMPLETE**:
- **Dependencies Resolved**: All Cargo.toml dependencies compatible and locked (deltalake 0.26.2, AWS SDK, tokio 1.45.1)
- **Project Structure**: Complete `rust-writer/` directory with proper organization
- **TDD Framework**: Comprehensive test suite ready (`tests/surgical_strike.rs` with all test cases)
- **Configuration System**: Complete config structures for all three processes

**❌ IMPLEMENTATION GAP - What We Need**:
1. **Real Writer Process** - Replace placeholder `Writer` struct with actual:
   - DynamoDB locking integration for concurrent safety
   - Delta Lake write operations via MinIO
   - 250ms latency SLA monitoring and retry logic
   
2. **Real Compaction Process** - Replace placeholder `Compactor` with:
   - Delta Lake OPTIMIZE operations to merge small files
   - Intelligent scheduling (time-based, size-based triggers)
   - File size distribution monitoring
   
3. **Real Vacuum Process** - Replace placeholder `Vacuum` with:
   - Retention policy enforcement
   - Unreferenced file cleanup
   - Safe deletion with dependency checks

**Current Blocker**: Task 6.1 says "Set up Rust project" but that's done. We need **actual Rust implementation** of the three-process architecture.

**Next Immediate Steps**:
1. **Update Task 6** to reflect foundation complete, add implementation subtasks
2. **Start with Writer Process** - Most critical for the pipeline
3. **Enable TDD Tests** - Remove `#[ignore]` as real code replaces placeholders
4. **Integration Testing** - Connect to existing MinIO Delta Lake tables

### **Subsequent Priorities (Tasks 7+)**:
- **Task 7**: Testing Framework Integration
- **Task 8**: Kafka Streaming Integration  
- **Task 9**: ROAPI Auto-Generated APIs
- **Task 10**: Performance Benchmarking (Rust vs Spark)

**🔧 To Contribute**: The most impactful work right now is completing the Rust writer implementation in `neuralake/rust-writer/`. All tests and infrastructure are ready for TDD development.

## Explore Further

**Current Working Components:**
*   **🎯 MOST IMPORTANT: Check `.taskmaster/tasks/tasks.json`** to see our complete roadmap with detailed status
*   **📋 Use TaskMaster via MCP:** If you have the MCP server set up in your IDE, you can interact with tasks via natural language
*   **🏗️ Working Foundation (Tasks 1-5):** Complete S3/MinIO integration, Delta Lake, Code-as-Catalog system, CI/CD pipeline
*   **📚 Educational Resources:** Complete learning path for engineers from concepts to production
*   **🌐 Interactive Catalog:** Browse the generated catalog site to see "Code as a Catalog" in action
*   **🔍 View Changelogs:** Check **[docs/reference/changelogs/](./docs/reference/changelogs/)** to see exactly what's been built

**Development Opportunities:**
*   **🦀 HIGHEST PRIORITY: Complete Rust Writer Implementation**
    - Replace placeholder structs in `neuralake/rust-writer/src/` with real functionality
    - Start with `writer.rs` (most critical for pipeline)
    - Enable TDD tests incrementally as implementations are added
    - **Immediate Impact**: Unlocks all remaining 11 tasks in the roadmap
*   **🧪 Experiment with Working System:** Add new data sources in `neuralake/src/my_tables.py` (e.g., CSV, live API)
*   **📊 Build on Foundation:** Write complex queries in `neuralake/src/query_data.py` for advanced aggregations
*   **⚙️ Understand Architecture:** Examine `neuralake/src/config.py` for environment-specific configuration patterns
*   **🐳 Production Deployment:** Follow **[docs/how-to/upgrade_dev_to_prod.md](./docs/how-to/upgrade_dev_to_prod.md)** to deploy to real AWS

**Quick Tests to Verify Setup:**
```bash
# Basic functionality test - Demo catalog queries
cd neuralake && poetry run python src/query_data.py

# Generate browsable catalog site
poetry run python scripts/generate_demo_catalog_site.py

# Full verification suite  
poetry run python scripts/production_verification.py

# Check Rust writer compilation
cd rust-writer && cargo check
```

**Browse the Catalog:**
After running the demo catalog site generator, open `neuralake/demo-catalog-site/index.html` in your browser to explore the interactive catalog with all table definitions, schemas, and sample queries.

**Complete Demo Workflow:**
```bash
# Run the comprehensive demo that shows everything
cd neuralake && poetry run python scripts/demo_complete_workflow.py

# This will:
# 1. Query all demo tables with analytics
# 2. Generate the browsable catalog site  
# 3. Show you exactly how to explore the results
# 4. Provide copy-paste code examples
```