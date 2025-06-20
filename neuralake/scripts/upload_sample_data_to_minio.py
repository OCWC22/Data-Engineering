from pathlib import Path

import polars as pl
from pyarrow.fs import S3FileSystem
import pyarrow.parquet as pq


def main():
    """
    This script uploads the local sample Parquet file to the MinIO S3 bucket.
    """
    print("--- Starting data upload to MinIO ---")

    # Explicitly create an S3 FileSystem object for PyArrow
    s3 = S3FileSystem(
        access_key="minioadmin",
        secret_key="minioadmin",
        endpoint_override="http://localhost:9000",
    )

    local_parquet_path = Path("data/parts.parquet")
    bucket = "neuralake-bucket"
    s3_path = f"{bucket}/parts.parquet"

    # Check if the local file exists
    if not local_parquet_path.exists():
        print(f"Error: Local data file not found at '{local_parquet_path}'.")
        print("Please run 'create_sample_data.py' first.")
        return

    print(f"Reading local data from '{local_parquet_path}'...")
    df = pl.read_parquet(local_parquet_path)

    # Convert Polars DataFrame to a PyArrow Table
    arrow_table = df.to_arrow()

    print(f"Uploading data to 's3://{s3_path}'...")

    # Use PyArrow's Parquet writer with the explicit S3 filesystem
    pq.write_table(table=arrow_table, where=s3_path, filesystem=s3)

    print("\\n--- Upload complete! ---")
    print(f"The file 'parts.parquet' has been uploaded to the '{bucket}' in MinIO.")
    print("You can verify this by checking the MinIO console at http://localhost:9001.")


if __name__ == "__main__":
    main()
