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

# Get the absolute path for the parquet file
# This makes sure the file can be found regardless of where the script is run
parquet_file_path = os.path.abspath("data/parts.parquet")

# A table backed by a Parquet file
part = ParquetTable(
    name="part",
    uri=f"file://{parquet_file_path}",
    partitioning=[],
    description="Information about parts.",
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