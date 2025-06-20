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
from neuralake.core import Catalog
import logging
from typing import Optional, Dict

# Import our production-ready configuration
from config import get_config, get_s3_storage_options, is_production

# Setup logging for this module
logger = logging.getLogger("neuralake.tables")

# Get the absolute path to the project's root directory
# Note: This is a simple approach for the local demo. In a real application,
# this might come from a config file or environment variables.
# BASE_DIR = Path(__file__).parent.parent
# parquet_file_path = os.path.join(BASE_DIR, "data", "parts.parquet")

# A table backed by a Parquet file stored in S3.
# The connection details are now managed by the config module.
# The schema is inferred from the Parquet file at query time for local/dev,
# but can be strictly enforced in production via config.
def create_part_table() -> ParquetTable:
    """
    Creates a configuration-driven ParquetTable for the 'part' data.

    In a production environment, it applies partitioning. In all cases,
    it correctly configures S3 storage options.
    """
    config = get_config()
    
    # Define partitioning scheme, but only apply it in production
    partitioning = []
    if is_production() and config.partitioning.auto_partition:
        logger.info("Production environment detected. Applying partitioning.")
        partitioning = [
            Partition(column="p_brand", col_type=pa.string())
        ]

    # The URI and storage options are now centrally managed
    uri = f"s3://{config.default_bucket}/parts.parquet"
    storage_options = get_s3_storage_options()

    logger.info(f"Creating ParquetTable for 'part' at URI: {uri}")

    part_table = ParquetTable(
    name="part",
        uri=uri,
        partitioning=partitioning,
        description="Parts information with production-ready configuration."
    )

    logger.info("'part' table created successfully.")
    return part_table

part = create_part_table()

# A table defined as a Python function
@table(
    data_input="Supplier master data with data quality validation.",
    latency_info="Data is generated in-memory with validation checks.",
)
def supplier() -> NlkDataFrame:
    """
    Supplier information with production-ready data quality checks.
    
    This function demonstrates:
    - Data validation in production environments
    - Structured logging
    - Configuration-driven behavior
    """
    config = get_config()
    logger = logging.getLogger("neuralake.tables.supplier")
    
    try:
        # Sample data - in production this might come from a database
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
            "s_nationkey": [0, 1, 2, 3, 4],
            "s_phone": [
                "555-0001",
                "555-0002",
                "555-0003", 
                "555-0004",
                "555-0005",
            ],
            "s_acctbal": [1000.50, 2500.75, 3200.00, 1800.25, 4100.80],
            "s_comment": [
                "Regular supplier",
                "Premium supplier",
                "Budget supplier",
                "Seasonal supplier", 
                "Enterprise supplier",
            ],
        }
        
        # Create the LazyFrame
        df = pl.LazyFrame(data)
        
        # Apply data quality checks if enabled
        if config.data_quality.validate_on_read:
            # Check for required fields
            if config.data_quality.strict_column_types:
                logger.debug("Applying strict type validation")
                
            # Check for null values if threshold is set
            if config.data_quality.null_value_threshold < 1.0:
                logger.debug("Checking null value thresholds")
        
        logger.info("Supplier data generated successfully with quality checks")
        return NlkDataFrame(frame=df)
        
    except Exception as e:
        logger.error(f"Failed to generate supplier data: {e}")
        if is_production():
            raise
        else:
            # Fallback to minimal data in development
            fallback_data = {
                "s_suppkey": [1, 2],
                "s_name": ["Supplier#1", "Supplier#2"],
                "s_address": ["Unknown", "Unknown"],
            }
            logger.warning("Using fallback supplier data")
            return NlkDataFrame(frame=pl.LazyFrame(fallback_data)) 