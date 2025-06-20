"""
My Catalog - Connection to Demo Catalog System

This module provides access to the demo catalog with all registered tables.
Use this as the main entry point for accessing catalog functionality.
"""

# Import the demo catalog system
try:
    from .demo_catalog import get_demo_catalog, list_demo_tables, generate_demo_catalog_site
    from .catalog_core import default_catalog
except ImportError:
    # Fallback for direct script execution
    from demo_catalog import get_demo_catalog, list_demo_tables, generate_demo_catalog_site
    from catalog_core import default_catalog

# Create a catalog reference - this is the main catalog to use
DemoCatalog = get_demo_catalog()

# Convenience functions
def list_tables():
    """List all available tables in the catalog."""
    return list_demo_tables()

def get_table(name: str, **kwargs):
    """Get a table as a Polars LazyFrame."""
    return DemoCatalog.table(name, **kwargs)

def describe_table(name: str):
    """Get detailed metadata about a table."""
    return DemoCatalog.describe_table(name)

def generate_catalog_site(output_dir: str = "catalog-site"):
    """Generate static site for the catalog."""
    return generate_demo_catalog_site(output_dir)

# For backwards compatibility
def db(name: str = "demo"):
    """Get database reference (for backwards compatibility)."""
    class DatabaseWrapper:
        def table(self, table_name: str, **kwargs):
            return DemoCatalog.table(table_name, **kwargs)
    
    return DatabaseWrapper()

# Export the main catalog as DemoCatalog for easy access
__all__ = ['DemoCatalog', 'list_tables', 'get_table', 'describe_table', 'generate_catalog_site', 'db']
