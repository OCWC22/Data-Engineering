import os

# --- S3 Configuration ---
# Set environment variables for S3-compatible storage (MinIO).
# The neuralake library's underlying engine (delta-rs/pyarrow) will
# automatically use these variables for authentication and connection.
# IMPORTANT: This must be done *before* importing the catalog.
os.environ["AWS_ACCESS_KEY_ID"] = "minioadmin"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minioadmin"
os.environ["AWS_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["AWS_ALLOW_HTTP"] = "true"
os.environ["AWS_S3_ALLOW_UNSAFE_RENAME"] = "true"

from my_catalog import DemoCatalog

def main():
    """
    This script demonstrates how to use the neuralake catalog to query a table
    backed by S3-compatible storage (MinIO).
    """
    print("--- Querying 'part' table from S3 ---")

    # Get a reference to the 'part' table from the catalog
    part_table = DemoCatalog.db("demo_db").table("part")

    # Execute a simple query to get the first 5 rows.
    # The .collect() call triggers the actual data read from S3.
    part_data = part_table.limit(5).collect()

    print("\\nQuery successful! Fetched data from S3:")
    print(part_data)


if __name__ == "__main__":
    main() 