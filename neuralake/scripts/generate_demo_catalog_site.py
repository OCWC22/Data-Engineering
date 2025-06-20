#!/usr/bin/env python3
"""
Generate Demo Catalog Site

Script to generate a browsable HTML catalog site from the demo_catalog system.
This demonstrates the complete "Code as a Catalog" workflow with the SSG.
"""
import sys
from pathlib import Path
import logging

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Generate the demo catalog site."""
    
    logger.info("🌐 Starting Demo Catalog Site Generation")
    
    # Import after setting up path
    try:
        from demo_catalog import generate_demo_catalog_site, list_demo_tables
        from my_catalog import DemoCatalog
        
        # Check what tables are available
        tables = list_demo_tables()
        logger.info(f"📚 Found {len(tables)} registered tables:")
        for table_name in tables:
            try:
                metadata = DemoCatalog.describe_table(table_name)
                table_type = metadata.get('table_type', 'unknown')
                description = metadata.get('description', 'No description')[:50]
                logger.info(f"  • {table_name:20} ({table_type:8}) - {description}...")
            except Exception as e:
                logger.warning(f"  • {table_name:20} (error) - Could not get metadata: {e}")
        
        # Test table access
        logger.info("\n🧪 Testing table access...")
        test_tables = ["users", "user_events", "neural_signals"]
        for table_name in test_tables:
            if table_name in tables:
                try:
                    df = DemoCatalog.table(table_name).limit(1).collect()
                    logger.info(f"✅ Successfully queried '{table_name}': {df.shape}")
                except Exception as e:
                    logger.error(f"❌ Failed to query '{table_name}': {e}")
            else:
                logger.warning(f"⚠️  Table '{table_name}' not found in catalog")
        
        # Generate the static site
        logger.info("\n🎨 Generating static catalog site...")
        output_path = generate_demo_catalog_site("demo-catalog-site")
        
        logger.info("✅ Demo catalog site generation complete!")
        logger.info(f"   📂 Output directory: {output_path}")
        logger.info(f"   🌐 Open in browser: file://{output_path}/index.html")
        
        # Test queries for verification
        logger.info("\n📊 Running sample queries for verification...")
        try:
            # Sample analytics queries
            users_count = DemoCatalog.table("users").select("user_id").count().collect()
            events_count = DemoCatalog.table("user_events").select("event_id").count().collect() 
            
            logger.info(f"  📈 Total users: {users_count.item()}")
            logger.info(f"  📈 Total events: {events_count.item()}")
            
            # Check for most active user
            import polars as pl
            most_active = DemoCatalog.table("user_events").group_by("user_id").agg(
                pl.count().alias("event_count")
            ).sort("event_count", descending=True).limit(1).collect()
            
            if len(most_active) > 0:
                logger.info(f"  🏆 Most active user ID: {most_active['user_id'][0]} ({most_active['event_count'][0]} events)")
            
        except Exception as e:
            logger.warning(f"⚠️  Could not run verification queries: {e}")
        
        logger.info("\n🎉 All done! The demo catalog site is ready to browse.")
        
    except Exception as e:
        logger.error(f"❌ Failed to generate demo catalog site: {e}")
        logger.error("Make sure all dependencies are installed and the demo_catalog module is working correctly")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 