"""
Production-ready catalog implementation for Neuralake data platform.

This module demonstrates how to create a production-ready catalog using
the new configuration system and following data engineering best practices.
"""

from neuralake.core import ModuleDatabase, Catalog
import logging
from pathlib import Path
from typing import Optional
import warnings

# Import our production-ready configuration
from config import (
    get_config, 
    get_s3_storage_options, 
    get_default_bucket, 
    is_production
)

# Import our production table definitions
from my_tables_production import (
    create_part_table,
    supplier,
    validate_table_access
)

# Setup logging for this module
logger = logging.getLogger("neuralake.catalog")


class ProductionCatalog:
    """
    Production-ready catalog implementation with configuration management,
    error handling, and monitoring capabilities.
    """
    
    def __init__(self, validate_on_startup: bool = True):
        """
        Initialize the production catalog.
        
        Args:
            validate_on_startup: Whether to validate storage access on initialization
        """
        self.config = get_config()
        self._catalog = None
        self._is_initialized = False
        
        # Logging is already configured by get_config()
        logger.info(f"Initializing Neuralake catalog for environment: {self.config.environment.value}")
        
        if validate_on_startup:
            self._validate_environment()
        
        # Initialize the catalog
        self._initialize_catalog()
    
    def _validate_environment(self) -> None:
        """Validate the environment configuration and storage access."""
        logger.info("Validating environment configuration...")
        
        # Check storage access
        bucket = get_default_bucket()
        storage_options = get_s3_storage_options()
        if not validate_table_access(bucket, "validation-test", storage_options):
            error_msg = "Storage validation failed - cannot initialize catalog"
            logger.error(error_msg)
            if is_production():
                raise RuntimeError(error_msg)
            else:
                logger.warning("Continuing with storage validation failure in non-production environment")
        
        # Production-specific validations
        if is_production():
            storage_options = get_s3_storage_options()
            
            # Ensure credentials are present
            if not (storage_options.get('AWS_ACCESS_KEY_ID') and 
                   storage_options.get('AWS_SECRET_ACCESS_KEY')):
                raise ValueError("Production environment requires AWS credentials")
            
            # Ensure secure connections
            if storage_options.get('AWS_ALLOW_HTTP', False):
                raise ValueError("Production environment cannot use HTTP connections")
            
            # Check encryption settings
            if not self.config.security.encrypt_at_rest:
                warnings.warn("Encryption at rest is recommended for production")
        
        logger.info("Environment validation completed successfully")
    
    def _initialize_catalog(self) -> None:
        """Initialize the catalog with production-ready tables."""
        try:
            logger.info("Creating ModuleDatabase...")
            
            # Import the module containing our tables
            import my_tables_production as tables_module
            
            # Create the database with our production tables module
            db = ModuleDatabase(db=tables_module)
            
            logger.info("ModuleDatabase created with production tables module")
            
            # Create the catalog with the database
            self._catalog = Catalog(dbs={"production": db})
            
            # Apply storage options globally
            storage_options = get_s3_storage_options()
            logger.info(f"Applied S3 storage options: {len(storage_options)} options configured")
            
            self._is_initialized = True
            logger.info("Catalog initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize catalog: {e}")
            if is_production():
                raise
            else:
                logger.warning("Catalog initialization failed, some functionality may be limited")
    
    def get_catalog(self) -> Optional[Catalog]:
        """Get the initialized catalog."""
        if not self._is_initialized:
            logger.warning("Catalog not properly initialized")
        return self._catalog
    
    def health_check(self) -> dict:
        """
        Perform a comprehensive health check of the catalog.
        
        Returns:
            Dictionary with health check results
        """
        health_status = {
            "catalog_initialized": self._is_initialized,
            "environment": self.config.environment.value,
            "timestamp": self.config.created_at.isoformat(),
            "storage_accessible": False,
            "tables_count": 0,
            "errors": []
        }
        
        try:
            # Check storage access
            bucket = get_default_bucket()
            storage_options = get_s3_storage_options()
            health_status["storage_accessible"] = validate_table_access(bucket, "health-check", storage_options)
            
            # Check catalog state
            if self._catalog:
                databases = self._catalog.dbs()
                health_status["databases_count"] = len(databases)
                
                # Count tables across all databases
                total_tables = 0
                for db_name in databases:
                    db = self._catalog.db(db_name)
                    if db:
                        tables = db.tables()
                        total_tables += len(tables)
                        logger.debug(f"Database {db_name} has {len(tables)} tables")
                
                health_status["tables_count"] = total_tables
            
            logger.info(f"Health check completed: {health_status}")
            
        except Exception as e:
            health_status["errors"].append(str(e))
            logger.error(f"Health check failed: {e}")
        
        return health_status
    
    def get_storage_info(self) -> dict:
        """Get information about the configured storage."""
        storage_options = get_s3_storage_options()
        
        # Filter out sensitive information
        safe_info = {
            "endpoint": storage_options.get('AWS_ENDPOINT_URL', 'Default AWS'),
            "region": storage_options.get('AWS_REGION'),
            "bucket": get_default_bucket(),
            "allow_http": storage_options.get('AWS_ALLOW_HTTP', False),
            "max_connections": storage_options.get('AWS_MAX_CONNECTIONS'),
            "has_credentials": bool(
                storage_options.get('AWS_ACCESS_KEY_ID') and 
                storage_options.get('AWS_SECRET_ACCESS_KEY')
            )
        }
        
        return safe_info


def create_production_catalog() -> ProductionCatalog:
    """
    Factory function to create a production-ready catalog.
    
    This is the recommended way to create a catalog in production applications.
    """
    logger.info("Creating production catalog...")
    return ProductionCatalog(validate_on_startup=True)


# For backward compatibility and direct usage
def get_catalog() -> Catalog:
    """
    Get a configured catalog instance.
    
    This function maintains backward compatibility while using the new
    production-ready configuration system.
    """
    prod_catalog = create_production_catalog()
    catalog = prod_catalog.get_catalog()
    
    if catalog is None:
        raise RuntimeError("Failed to initialize catalog")
    
    return catalog


# Module-level testing
if __name__ == "__main__":
    print("=== Testing Production Catalog ===")
    
    try:
        # Test catalog creation
        prod_catalog = create_production_catalog()
        print("✓ Production catalog created successfully")
        
        # Test health check
        health = prod_catalog.health_check()
        print(f"✓ Health check completed")
        print(f"  - Initialized: {health['catalog_initialized']}")
        print(f"  - Environment: {health['environment']}")
        print(f"  - Tables: {health['tables_count']}")
        print(f"  - Storage accessible: {health['storage_accessible']}")
        
        if health['errors']:
            print(f"  - Errors: {health['errors']}")
        
        # Test storage info
        storage_info = prod_catalog.get_storage_info()
        print(f"✓ Storage info retrieved")
        print(f"  - Endpoint: {storage_info['endpoint']}")
        print(f"  - Bucket: {storage_info['bucket']}")
        print(f"  - Has credentials: {storage_info['has_credentials']}")
        
        # Test catalog access
        catalog = prod_catalog.get_catalog()
        if catalog:
            databases = catalog.dbs()
            print(f"✓ Catalog accessible with {len(databases)} databases")
            
            for db_name in databases:
                db = catalog.db(db_name)
                if db:
                    tables = db.tables()
                    print(f"  - Database '{db_name}': {len(tables)} tables")
        
        print("\n=== Production Catalog Test Completed Successfully ===")
        
    except Exception as e:
        print(f"✗ Production catalog test failed: {e}")
        import traceback
        traceback.print_exc() 