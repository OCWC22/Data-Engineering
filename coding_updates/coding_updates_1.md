# 06-19-25 - Initial Project Setup & Debugging (`neuralake` Demo)

### Files Updated:
- `neuralake/neuralake_demo/create_sample_data.py`: Created script to generate sample Parquet data.
- `neuralake/neuralake_demo/my_tables.py`: Defined `neuralake` tables from Parquet and a Python function.
- `neuralake/neuralake_demo/my_catalog.py`: Established the `neuralake` data catalog.
- `neuralake/neuralake_demo/query_data.py`: Implemented the main query and join logic.
- `neuralake/neuralake_demo/ONBOARDING.md`: Created educational documentation.
- `neuralake/neuralake_demo/README.md`: Created the project README.
- `.gitignore`: Added a standard Python gitignore file.
- `coding_updates/coding_updates_1.md`: Initial documentation of the setup process.

### Description:
This initial update sets up a demonstration project for the `neuralake` library. It includes creating sample data, defining a data catalog in code, and executing a query that joins data from two different sources. This serves as a foundational example of a modern ELT pipeline using `neuralake`.

### Reasoning:
The goal was to provide a hands-on, working example to accompany the educational documentation. The process involved several debugging steps, which are documented here to provide a realistic view of the development process.

### Trade-offs:
- **Initial Complexity**: The debugging process revealed that the `neuralake` library has some undocumented or unexpected API requirements (e.g., the `partitioning` argument). This added some initial friction to the setup.
- **Simplified Data**: The sample data is very small and simple. A real-world example would involve more complex data and schemas.

### Considerations:
The debugging process highlighted the importance of reading the source code when documentation is sparse. The errors encountered were primarily `TypeError` exceptions due to incorrect arguments passed to the `ParquetTable` constructor. The final file path issue was a simple oversight in the initial script.

### Future Work:
- Explore more advanced features of `neuralake`, such as `DeltalakeTable`.
- Expand the demo to include a more complex, multi-stage data pipeline.
- Add automated tests to verify the pipeline's correctness.

---
# 06-19-25 - Migrated to Poetry for Dependency Management

### Files Updated:
- `pyproject.toml`: Created to manage project dependencies with Poetry.
- `poetry.lock`: Generated to ensure reproducible builds.
- `README.md`: Updated installation and execution instructions to use Poetry commands.
- `requirements.txt`: Deleted as it is now obsolete.
- `.gitignore`: Updated to include `.DS_Store` and other common Python artifacts.

### Description:
This update transitions the project from a `pip` and `requirements.txt` based setup to a more modern and robust dependency management system using **Poetry**. This improves the reliability and reproducibility of the development environment.

### Reasoning:
Using `pip` with a `requirements.txt` file is functional but has drawbacks. It doesn't inherently handle dependency conflicts well, and it doesn't provide a true lockfile mechanism to guarantee that the exact same versions of all dependencies (including sub-dependencies) are used across different environments. **Poetry** solves these problems by:
1.  Providing a `pyproject.toml` for clear dependency declaration.
2.  Generating a `poetry.lock` file for deterministic, reproducible builds.
3.  Offering a much better developer experience for managing dependencies and virtual environments.

We also explored using **`uv`**, a high-speed installer, as a backend for Poetry. However, this feature appears to require a newer version of Poetry than is currently installed, so we have deferred this optimization to keep the setup instructions simple and reliable. The core benefits of Poetry's dependency management are fully realized.

### Trade-offs:
- **Learning Curve**: For developers unfamiliar with Poetry, there is a small learning curve compared to `pip`. However, the benefits in project stability and maintainability far outweigh this.
- **Tooling Overhead**: Poetry introduces a new tool into the workflow, but it replaces the need to manage `virtualenv` and `pip` separately.

### Considerations:
The migration involved resolving dependency conflicts, as `neuralake` has strict version requirements for its own dependencies (`polars` and `pyarrow`). Poetry's dependency resolver helped identify and fix these issues explicitly in the `pyproject.toml` file.

### Future Work:
- Re-evaluate using `uv` as an installer for Poetry in the future, as newer versions of Poetry are released.
- Add linters and formatters (like `ruff`) to the `dev` dependencies in `pyproject.toml` to enforce code quality.

### Issues Encountered & Resolutions:

1.  **NumPy Version Conflict**:
    -   **Issue**: The initial execution failed with an error indicating that a module compiled with NumPy 1.x could not run with the installed NumPy 2.x. This is a common issue when new major versions of core libraries are released.
    -   **Resolution**: I downgraded the `numpy` package to a version less than 2.0 (`pip install "numpy<2.0"`) to ensure compatibility with the `neuralake` dependency tree.

2.  **`ParquetTable` `TypeError`s**:
    -   **Issue**: The script failed with a series of `TypeError` exceptions because invalid arguments (`schema`, `unique_columns`) were passed to the `ParquetTable` constructor. The documentation provided in the PyPI description was slightly out of sync with the actual class implementation.
    -   **Resolution**: I inspected the library's source code to find the correct constructor signature. This revealed the `partitioning` argument was required. I updated the code to provide the correct arguments (`name`, `uri`, `partitioning`).

3.  **`PartitioningScheme` `ValueError`**:
    -   **Issue**: I initially tried to pass an empty list to `PartitioningScheme`, which caused a `ValueError` because it's an `Enum`, not a class that can be instantiated with a list.
    -   **Resolution**: By reading the source code in `neuralake/core/tables/util.py`, I identified that `PartitioningScheme` was an `Enum` and that the `ParquetTable`'s `partitioning` argument expected a list of `Partition` objects. For our unpartitioned data, passing an empty list (`[]`) to `partitioning` was the correct approach.

4.  **`FileNotFoundError`**:
    -   **Issue**: The query script failed because it couldn't find the `parts.parquet` file. The `create_sample_data.py` script was run from the project root, creating the `data` directory there, but the query script expected it inside the `neuralake/neuralake_demo` directory.
    -   **Resolution**: I moved the `data` directory into the `neuralake/neuralake_demo` directory (`mv data neuralake/neuralake_demo/`), which aligned the actual file path with the path expected by the script.

---
# 06-19-25 - Refactored to a Multi-Project Monorepo Structure

### Files Updated:
- `neuralake/`: The entire directory was restructured to be a self-contained project.
- `pyproject.toml`: Moved into `neuralake/`.
- `poetry.lock`: Moved into `neuralake/`.
- `README.md`: A new root-level README was created to act as a table of contents.
- `neuralake/README.md`: The previous root README was moved here and updated with project-specific instructions.
- `neuralake/*.py`: All python scripts were updated to remove unnecessary path manipulation.

### Description:
This update refactors the repository from a single-project setup to a multi-project "monorepo" structure. The `neuralake` demo is now a fully self-contained project within the larger `Data-Engineering` repository.

### Reasoning:
The original structure, with a single `pyproject.toml` at the root, was not scalable. It would have led to dependency conflicts as soon as a second project was added. The new structure isolates each project's dependencies, making the repository much more robust and easier to manage long-term. This aligns with the user's goal of having a collection of separate mini-projects.

### Trade-offs:
- **Slightly More Complex Navigation**: Developers now need to `cd` into the specific project directory (`neuralake/`) before running commands. This is a very minor trade-off for the significant benefit of dependency isolation.

### Considerations:
This refactoring is a critical step in establishing a clean, scalable foundation for a data engineering portfolio. Each new project can now be added in its own directory with its own `poetry` environment, without interfering with any existing projects.

### Future Work:
- Add a new data engineering project to the repository to validate the multi-project structure.
- Create a template or cookiecutter for bootstrapping new projects within this monorepo.

---
# 06-19-25 - Implement Local S3 Environment with MinIO

### Files Updated:
- `neuralake/docker-compose.yml`: Created to define the local MinIO service.
- `neuralake/setup_minio.sh`: Created to automate starting MinIO and creating the necessary bucket.
- `neuralake/README.md`: Updated with instructions for running the MinIO setup script.
- `.taskmaster/tasks/tasks.json`: Updated all tasks with detailed local-first implementation strategies.
- `.taskmaster/docs/prd.txt`: Updated the master plan to reflect the zero-cost, local-first strategy.

### Description:
This update establishes the foundation for our local-first development strategy by setting up a local, S3-compatible object store using MinIO. It includes a Docker Compose file for easy service startup and a shell script to automate the configuration, including the creation of the `neuralake-bucket`. All project tasks in Taskmaster have been updated to reflect this cost-effective approach.

### Reasoning:
To accelerate development, improve the developer feedback loop, and eliminate cloud costs during the initial build-out phase, we are emulating the AWS S3 environment locally. MinIO is a lightweight, fully S3-compatible server that allows us to develop and test all Delta Lake and cloud storage features without needing an active AWS account. This aligns perfectly with the project's "scale-down" philosophy.

### Trade-offs:
- This local setup does not test for cloud-specific configurations like IAM roles or network policies. These aspects will need to be addressed in a later stage when we prepare for a true cloud deployment. However, for developing core functionality, this is a significant net positive.

### Considerations:
The implementation uses Docker Compose for a declarative and reproducible service definition. The `setup_minio.sh` script orchestrates the setup, making the environment easy for any developer to spin up. Using the standard `aws-cli` to interact with the local MinIO endpoint confirms that our tooling and the S3 API calls will be portable to a real AWS environment with minimal changes.

### Future Work:
- Modify the `neuralake` library's `ParquetTable` to read from the MinIO S3 endpoint instead of the local filesystem.
- Create a script to upload the sample `parts.parquet` data to the `neuralake-bucket` in MinIO to prepare for the next development stage.

---
# 06-19-25 - End-to-End S3 Integration & Debugging

### Files Updated:
- `neuralake/pyproject.toml`: Updated to install `polars` with the `[aws]` extra to include necessary S3 support libraries.
- `neuralake/poetry.lock`: Regenerated after updating dependencies.
- `neuralake/upload_sample_data_to_minio.py`: Rewritten to use `pyarrow.fs.S3FileSystem` for robust, direct-to-S3 writing.
- `neuralake/my_tables.py`: Modified the `ParquetTable` definition to match the actual, more simplistic API of the installed `neuralake` version.
- `neuralake/query_data.py`: Refactored to set S3 environment variables and query the `part` table directly from the MinIO S3 bucket.

### Description:
This update marks the successful completion of Task 1: "Configure AWS S3 Integration." It establishes a fully functional, end-to-end data pipeline running on the local machine. Data is uploaded to a local MinIO S3 server and then successfully queried using the `neuralake` library. This validates the core components of our local development environment.

### Reasoning:
The primary goal was to create a local, cost-free equivalent of a cloud data pipeline. The process involved a significant debugging effort, which was critical for uncovering the true API and dependency requirements of the `neuralake` library. By solving these issues, we have de-risked future development and now have a stable, validated local stack.

### Trade-offs:
- The `neuralake` library version (`0.0.5`) proved to be far more minimalistic than its documentation suggested. We had to abandon passing credentials via `storage_options` and discovered several arguments were not implemented. The trade-off is that we are now working with the library's actual capabilities, not its documented ones.

### Issues Encountered & Resolutions:
This was a multi-stage debugging process that peeled back layers of the library stack:

1.  **`TypeError` on `pl.write_parquet`**: The initial attempt to upload data using `polars`' `storage_options` failed. This feature was not supported as expected for S3 in the installed version.
2.  **`FileNotFoundError` with Environment Variables**: Switching to environment variables for authentication failed because the underlying engine couldn't find the correct S3 library.
3.  **Dependency Conflict**: Attempting to add `s3fs` manually caused dependency conflicts with `neuralake`'s existing tree.
4.  **Correct Dependency (`polars[aws]`)**: The correct solution was to install `polars` with its `[aws]` extra in `pyproject.toml`. This provided the necessary Rust-based S3/AWS support without conflicts.
5.  **Robust Upload (`pyarrow.fs.S3FileSystem`)**: Even with the right dependencies, direct writing was unreliable. The final, robust solution was to rewrite the upload script to use `pyarrow`'s `S3FileSystem` explicitly, giving us direct control over the connection.
6.  **`neuralake` `ParquetTable` `TypeError`**: The final and most critical issue was that the `neuralake` library's `ParquetTable` constructor did not match its documentation. Through trial and error, we determined its actual signature is much simpler, requiring only `name`, `uri`, and `partitioning`. After modifying `my_tables.py` to use this correct signature, the end-to-end query from S3 finally succeeded. 