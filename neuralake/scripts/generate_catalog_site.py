#!/usr/bin/env python3
"""
Generate Static Catalog Site

Script to generate a browsable HTML catalog from the existing table definitions.
Demonstrates Task 5's "Code as a Catalog" static site generation capability.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from catalog_core import default_catalog
from ssg import CatalogSiteGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Generate the catalog site from existing registered tables."""
    
    logger.info("🌐 Starting Catalog Site Generation")
    
    # Check if we have any tables registered
    tables = default_catalog.list_tables()
    logger.info(f"Found {len(tables)} registered tables: {tables}")
    
    if not tables:
        logger.warning("No tables found in catalog. Registering example tables...")
        
        # Import tables to register them (this runs the decorators)
        try:
            from my_tables import supplier, part
            logger.info("✅ Successfully imported table definitions")
            
            # Check again
            tables = default_catalog.list_tables()
            logger.info(f"Now found {len(tables)} tables: {tables}")
            
        except Exception as e:
            logger.error(f"❌ Failed to import tables: {e}")
            return
    
    # Export catalog metadata
    logger.info("📊 Exporting catalog metadata...")
    catalog_metadata = default_catalog.export_catalog_metadata()
    
    # Show what we found
    logger.info(f"Metadata export contains {catalog_metadata['total_tables']} tables")
    for table_name, table_info in catalog_metadata['tables'].items():
        logger.info(f"  - {table_name} ({table_info['table_type']}): {table_info['description']}")
    
    # Generate the static site
    output_dir = Path("catalog-site")
    logger.info(f"🎨 Generating static site in: {output_dir.absolute()}")
    
    generator = CatalogSiteGenerator(output_dir)
    generator.generate_site(
        catalog_metadata, 
        project_name="Neuralake Data Catalog"
    )
    
    logger.info("✅ Catalog site generation complete!")
    logger.info(f"   Open: file://{output_dir.absolute()}/index.html")
    
    # Test a table query to verify functionality
    logger.info("\n🧪 Testing table access...")
    try:
        test_table = tables[0] if tables else None
        if test_table:
            df = default_catalog.table(test_table)
            data = df.collect()
            logger.info(f"✅ Successfully queried '{test_table}': {data.shape} rows/cols")
            logger.info(f"   Columns: {data.columns}")
    except Exception as e:
        logger.error(f"❌ Failed to query test table: {e}")

if __name__ == "__main__":
    main() 