from neuralake.core import (
    ParquetTable,
    Filter,
    table,
    NlkDataFrame,
    Partition,
    PartitioningScheme
)
import pyarrow as pa
import polars as pl
import os
from pathlib import Path
from neuralake.core import Catalog

# Define the connection details for our local MinIO S3 instance.
# The neuralake library will pass these to the underlying query engine (delta-rs).
S3_STORAGE_OPTIONS = {
    "AWS_ACCESS_KEY_ID": "minioadmin",
    "AWS_SECRET_ACCESS_KEY": "minioadmin",
    "AWS_ENDPOINT_URL": "http://localhost:9000",
    "AWS_ALLOW_HTTP": "true",
    "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
}

# Get the absolute path to the project's root directory
# Note: This is a simple approach for the local demo. In a real application,
# this might come from a config file or environment variables.
# BASE_DIR = Path(__file__).parent.parent
# parquet_file_path = os.path.join(BASE_DIR, "data", "parts.parquet")

# A table backed by a Parquet file stored in S3.
# The connection details are configured via environment variables
# in the script that runs the query (see query_data.py).
# The schema is inferred from the Parquet file at query time.
part = ParquetTable(
    name="part",
    uri="s3://neuralake-bucket/parts.parquet",
    partitioning=[],
    description="Information about parts, stored in S3.",
)

# A table defined as a Python function
@table(
    data_input="Supplier master data from a dictionary.",
    latency_info="Data is generated in-memory when the function is called.",
)
def supplier() -> NlkDataFrame:
    """Supplier information."""
    data = {
        "s_suppkey": [1, 2, 3, 4, 5],
        "s_name": [
            "Supplier#1",
            "Supplier#2",
            "Supplier#3",
            "Supplier#4",
            "Supplier#5",
        ],
        "s_address": [
            "123 Main St",
            "456 Oak Ave",
            "789 Pine Ln",
            "101 Maple Dr",
            "212 Birch Rd",
        ],
    }
    return NlkDataFrame(frame=pl.LazyFrame(data)) 