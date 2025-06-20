from pathlib import Path
import sys


def setup_path():
    """Setup the Python path for local imports."""
    proj_root = Path(__file__).parent.parent
    if str(proj_root) not in sys.path:
        sys.path.append(str(proj_root))


def main():
    """
    Demonstrates how to use the neuralake catalog to query a table.
    The underlying data source (local S3, production S3) is determined
    by the configuration loaded via the NEURALAKE_ENV environment variable.

    By default, the config will load the 'local' environment, which is
    pre-configured to connect to the local MinIO S3 instance.
    You can switch to a different environment (e.g., production) by setting
    the 'NEURALAKE_ENV' environment variable before running this script.
    For example:
    NEURALAKE_ENV=production python -m neuralake.query_data
    """
    setup_path()

    from config import get_config, is_production
    from my_catalog import DemoCatalog

    config = get_config()
    env = "Production" if is_production() else "Local"
    print(f"--- Querying 'part' table from S3 ({env} Environment) ---")
    print(f"--- S3 Endpoint: {config.s3.endpoint_url} ---")

    # Get a reference to the 'part' table from the catalog
    part_table = DemoCatalog.db("demo_db").table("part")

    # Execute a simple query to get the first 5 rows.
    # The .collect() call triggers the actual data read from S3.
    part_data = part_table.limit(5).collect()

    print("\\nQuery successful! Fetched data from S3:")
    print(part_data)


if __name__ == "__main__":
    main()
