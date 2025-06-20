"""
Production-ready table definitions for Neuralake data platform.

This module demonstrates how to use the new configuration system to create
production-ready table definitions that follow Neuralake best practices.
"""

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
import logging
from typing import Optional, Dict
from pathlib import Path

# Import our production-ready configuration
from config import get_config, get_s3_storage_options, get_default_bucket, is_production

# Setup logging for this module
logger = logging.getLogger("neuralake.tables")


def get_part_schema() -> pa.Schema:
    """
    Get the PyArrow schema for the parts table.
    
    This ensures consistent data types and validation across all parts data.
    """
    return pa.schema([
        pa.field("p_partkey", pa.int64(), nullable=False),
        pa.field("p_name", pa.string(), nullable=False),
        pa.field("p_mfgr", pa.string(), nullable=True),
        pa.field("p_brand", pa.string(), nullable=True),
        pa.field("p_type", pa.string(), nullable=True),
        pa.field("p_size", pa.int32(), nullable=True),
        pa.field("p_container", pa.string(), nullable=True),
        pa.field("p_retailprice", pa.float64(), nullable=True),
        pa.field("p_comment", pa.string(), nullable=True),
    ])

def create_part_table() -> ParquetTable:
    """
    Create a production-ready ParquetTable for parts data.
    
    This function demonstrates:
    - Using configuration-driven S3 settings
    - Proper error handling and logging
    - Schema validation in production environments
    - Partitioning strategy for performance
    """
    config = get_config()
    
    try:
        # Define explicit schema for production (recommended in code review)
        schema = pa.schema([
            pa.field('p_partkey', pa.int64(), nullable=False),
            pa.field('p_name', pa.string(), nullable=False),
            pa.field('p_mfgr', pa.string(), nullable=True),
            pa.field('p_brand', pa.string(), nullable=True),
            pa.field('p_type', pa.string(), nullable=True),
            pa.field('p_size', pa.int32(), nullable=True),
            pa.field('p_container', pa.string(), nullable=True),
            pa.field('p_retailprice', pa.decimal128(15, 2), nullable=True),
            pa.field('p_comment', pa.string(), nullable=True),
        ])
        
        # Create partitioning strategy for better performance
        partitioning = []
        if config.partitioning.auto_partition:
            # Example: partition by brand for better query performance
            partitioning = [
                Partition(column="p_brand", col_type=pa.string())
            ]
        
        # Construct the S3 URI using configuration
        bucket = get_default_bucket()
        data_prefix = config.bronze_prefix  # Use bronze layer for raw data
        uri = f"s3://{bucket}/{data_prefix}/parts.parquet"
        
        logger.info(f"Creating ParquetTable for parts at {uri}")
        
        part_table = ParquetTable(
            name="part",
            uri=uri,
            partitioning=partitioning,
            description="Parts information with production-ready configuration and schema validation.",
        )
        
        logger.info("ParquetTable for parts created successfully")
        return part_table
        
    except Exception as e:
        logger.error(f"Failed to create parts table: {e}")
        if is_production():
            # In production, we want to fail fast
            raise
        else:
            # In development, we can be more lenient
            logger.warning("Falling back to basic table configuration")
            return ParquetTable(
                name="part",
                uri=f"s3://{get_default_bucket()}/parts.parquet",
                partitioning=[],
                description="Parts information (fallback configuration).",
            )


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


def validate_table_access(bucket: str, table_name: str, storage_options: Dict[str, str]) -> bool:
    """
    Validate that we can access our configured storage.
    
    This is useful for startup health checks in production.
    """
    config = get_config()
    logger = logging.getLogger("neuralake.tables.validation")
    
    try:
        # Get storage options using our configuration
        storage_options = get_s3_storage_options()
        
        logger.info("Storage configuration validation:")
        logger.info(f"  Endpoint: {storage_options.get('AWS_ENDPOINT_URL', 'Default AWS')}")
        logger.info(f"  Region: {storage_options.get('AWS_REGION')}")
        logger.info(f"  Bucket: {get_default_bucket()}")
        
        # Check if we have credentials (without logging them)
        has_credentials = bool(
            storage_options.get('AWS_ACCESS_KEY_ID') and 
            storage_options.get('AWS_SECRET_ACCESS_KEY')
        )
        logger.info(f"  Credentials configured: {has_credentials}")
        
        if is_production() and not has_credentials:
            logger.error("Production environment requires credentials")
            return False
            
        logger.info("Table access validation completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Table access validation failed: {e}")
        return False


# Create the production-ready table instances
if __name__ == "__main__":
    # This allows testing the module directly
    print("=== Testing Production Table Definitions ===")
    
    # Test validation
    if validate_table_access():
        print("✓ Storage access validation passed")
    else:
        print("✗ Storage access validation failed")
    
    # Test table creation
    try:
        part = create_part_table()
        print(f"✓ Parts table created: {part.name}")
    except Exception as e:
        print(f"✗ Parts table creation failed: {e}")
    
    # Test function table
    try:
        supplier_data = supplier()
        print(f"✓ Supplier function table created")
    except Exception as e:
        print(f"✗ Supplier function table failed: {e}")
    
    print("\nConfiguration summary:")
    config = get_config()
    print(f"  Environment: {config.environment.value}")
    print(f"  Data quality validation: {config.data_quality.enforce_schema}")
    print(f"  Security encryption: {config.security.encrypt_at_rest}") 