"""
Delta Lake configuration for MinIO integration.

This module provides configuration utilities for Delta Lake operations
with our MinIO S3 backend, integrating with the existing config system.
"""
import os
from typing import Dict, Any
from config import get_s3_storage_options


def get_delta_storage_options() -> Dict[str, Any]:
    """Get storage options for Delta Lake with MinIO.
    
    Integrates with existing config system to provide consistent
    S3 configuration for Delta Lake operations.
    
    Returns:
        Dictionary of storage options for delta-rs
    """
    # Get base S3 options from existing config
    s3_options = get_s3_storage_options()
    
    # Convert to delta-rs format
    # The config system already returns AWS format, so we use those keys
    delta_options = {
        "AWS_ENDPOINT_URL": s3_options.get("AWS_ENDPOINT_URL", "http://localhost:9000"),
        "AWS_ACCESS_KEY_ID": "minioadmin",  # Default MinIO credentials
        "AWS_SECRET_ACCESS_KEY": "minioadmin",  # Default MinIO credentials
        "AWS_REGION": s3_options.get("AWS_REGION", "us-east-1"),
        "AWS_S3_ALLOW_UNSAFE_RENAME": "true",  # Required for MinIO compatibility
        "AWS_ALLOW_HTTP": "true",              # Allow HTTP for local MinIO
        "AZURE_STORAGE_USE_EMULATOR": "false", # Disable Azure emulation
    }
    
    return delta_options


def get_delta_table_uri(table_name: str, bucket: str = "neuralake-bucket") -> str:
    """Get S3 URI for Delta table.
    
    Args:
        table_name: Name of the Delta table
        bucket: S3 bucket name (default from config)
        
    Returns:
        S3 URI for the Delta table
    """
    return f"s3://{bucket}/delta-tables/{table_name}"


def set_delta_environment_variables() -> None:
    """Set Delta Lake environment variables for MinIO compatibility.
    
    This ensures that delta-rs can find the S3 credentials and configuration
    even when they're not explicitly passed to each operation.
    """
    delta_options = get_delta_storage_options()
    
    for key, value in delta_options.items():
        if key not in os.environ:  # Don't override existing env vars
            os.environ[key] = str(value)


def get_delta_write_options(
    mode: str = "append",
    schema_mode: str = "merge",
    partition_by: list = None
) -> Dict[str, Any]:
    """Get standardized write options for Delta Lake operations.
    
    Args:
        mode: Write mode ('append', 'overwrite', 'error')
        schema_mode: Schema handling ('merge', 'overwrite') 
        partition_by: Optional list of columns to partition by
        
    Returns:
        Dictionary of write options
    """
    options = {
        "mode": mode,
        "schema_mode": schema_mode,
        "storage_options": get_delta_storage_options(),
    }
    
    if partition_by:
        options["partition_by"] = partition_by
        
    return options


def validate_delta_environment() -> Dict[str, bool]:
    """Validate that Delta Lake environment is properly configured.
    
    Returns:
        Dictionary with validation results
    """
    validation = {
        "deltalake_imported": False,
        "pyarrow_imported": False,
        "s3_config_available": False,
        "minio_accessible": False,
    }
    
    # Check imports
    try:
        import deltalake
        validation["deltalake_imported"] = True
    except ImportError:
        pass
        
    try:
        import pyarrow
        validation["pyarrow_imported"] = True
    except ImportError:
        pass
    
    # Check S3 configuration
    try:
        s3_options = get_s3_storage_options()
        # The config returns AWS format keys, check for those
        validation["s3_config_available"] = bool(
            s3_options.get("AWS_ENDPOINT_URL") or s3_options.get("endpoint_url")
        )
    except Exception:
        pass
    
    # Check MinIO accessibility (basic connection test)
    try:
        import requests
        s3_options = get_s3_storage_options()
        endpoint = s3_options.get("AWS_ENDPOINT_URL") or s3_options.get("endpoint_url", "http://localhost:9000")
        response = requests.get(f"{endpoint}/minio/health/live", timeout=2)
        validation["minio_accessible"] = response.status_code == 200
    except Exception:
        pass
    
    return validation


# Convenience function for initialization
def initialize_delta_environment() -> None:
    """Initialize Delta Lake environment with proper configuration.
    
    Call this once at application startup to ensure Delta Lake
    operations have access to proper S3 configuration.
    """
    set_delta_environment_variables()
    
    # Validate environment
    validation = validate_delta_environment()
    
    # Log validation results
    import logging
    logger = logging.getLogger(__name__)
    
    for check, passed in validation.items():
        status = "✅" if passed else "❌"
        logger.info(f"{status} Delta Lake {check}: {passed}")
    
    if not all(validation.values()):
        logger.warning("⚠️ Some Delta Lake validation checks failed")
    else:
        logger.info("🚀 Delta Lake environment fully initialized") 