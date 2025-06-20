#!/usr/bin/env python3
"""
Complete Neuralake Demo Workflow

This script demonstrates the full "Code as a Catalog" workflow:
1. Import and query demo tables
2. Generate browsable catalog site
3. Run comprehensive queries 
4. Show user how to explore the generated site

This is the main demonstration of the SSG + demo_catalog integration.
"""
import sys
from pathlib import Path
import logging

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the complete demo workflow."""
    
    print("🚀 Neuralake Complete Demo Workflow")
    print("=" * 60)
    
    try:
        from demo_catalog import generate_demo_catalog_site, list_demo_tables
        from my_catalog import DemoCatalog
        import polars as pl
        
        # Step 1: Show available tables
        print("\n📚 Step 1: Discovering Available Tables")
        tables = list_demo_tables()
        print(f"Found {len(tables)} tables in the demo catalog:")
        
        for table_name in tables:
            metadata = DemoCatalog.describe_table(table_name)
            table_type = metadata.get('table_type', 'unknown')
            tags = metadata.get('tags', [])
            owner = metadata.get('owner', 'unknown')
            description = metadata.get('description', 'No description')[:60]
            
            print(f"  📊 {table_name:20} ({table_type:8}) - {description}...")
            print(f"     Owner: {owner}, Tags: {', '.join(tags) if tags else 'none'}")
        
        # Step 2: Run sample queries
        print("\n🔍 Step 2: Running Sample Queries")
        
        # Query function tables
        print("\n  📈 Analytics Query: User Activity Summary")
        user_activity = DemoCatalog.table("user_events").group_by("user_id").agg([
            pl.len().alias("total_events"),
            pl.col("event_type").n_unique().alias("unique_event_types")
        ]).join(
            DemoCatalog.table("users").select(["user_id", "username", "user_type"]),
            on="user_id"
        ).sort("total_events", descending=True).collect()
        
        print("Top active users:")
        print(user_activity.head(3))
        
        # Query neural data  
        print("\n  🧠 Neural Signals Analysis:")
        neural_summary = DemoCatalog.table("neural_signals").group_by("cortical_region").agg([
            pl.len().alias("signal_count"),
            pl.col("signal_strength").mean().round(3).alias("avg_strength"),
            pl.col("spike_detected").sum().alias("spike_count"),
            pl.col("frequency_hz").mean().round(1).alias("avg_frequency")
        ]).collect()
        
        print(neural_summary)
        
        # Query static tables
        print("\n  💰 Financial Summary:")
        financial_summary = DemoCatalog.table("transactions").group_by("transaction_type").agg([
            pl.len().alias("transaction_count"),
            pl.col("amount").sum().round(2).alias("total_amount"),
            pl.col("amount").mean().round(2).alias("avg_amount")
        ]).collect()
        
        print(financial_summary)
        
        # Step 3: Generate catalog site
        print("\n🎨 Step 3: Generating Browsable Catalog Site")
        output_path = generate_demo_catalog_site("demo-catalog-site")
        
        print(f"✅ Static catalog site generated!")
        print(f"   📂 Location: {output_path}")
        print(f"   🌐 Main page: file://{output_path}/index.html")
        
        # Step 4: Show site contents
        print("\n📋 Step 4: Generated Site Contents")
        site_files = []
        if output_path.exists():
            site_files.append(f"  📄 index.html - Main catalog listing with search")
            site_files.append(f"  📄 api-reference.html - Python API documentation")
            site_files.append(f"  📄 search-index.json - Search index for filtering")
            
            tables_dir = output_path / "tables"
            if tables_dir.exists():
                table_files = list(tables_dir.glob("*.html"))
                site_files.append(f"  📁 tables/ - {len(table_files)} individual table pages:")
                for table_file in sorted(table_files):
                    site_files.append(f"     📊 {table_file.name} - Detailed table documentation")
            
            static_dir = output_path / "static"
            if static_dir.exists():
                site_files.append(f"  📁 static/ - CSS and JavaScript assets")
        
        for file_desc in site_files:
            print(file_desc)
        
        # Step 5: Usage instructions
        print("\n🎯 Step 5: How to Explore the Catalog")
        print("1. Open the main catalog page in your browser:")
        print(f"   file://{output_path}/index.html")
        print()
        print("2. Features to try:")
        print("   🔍 Search for tables by name or description")
        print("   🏷️ Filter by tags (click tag buttons)")
        print("   📊 Click any table card to see detailed info")
        print("   📋 Copy code snippets for immediate use")
        print("   🛠️ Browse the API reference for Python usage")
        print()
        print("3. Add your own tables:")
        print("   - Edit src/demo_catalog.py to add @table functions")
        print("   - Use register_static_table() for existing data")
        print("   - Re-run this script to update the site")
        
        # Step 6: Integration examples
        print("\n🔗 Step 6: Integration Examples")
        print("# Query any table programmatically:")
        print("from src.my_catalog import DemoCatalog")
        print("df = DemoCatalog.table('users').collect()")
        print()
        print("# Generate site from code:")
        print("from src.demo_catalog import generate_demo_catalog_site")
        print("generate_demo_catalog_site('my-catalog-site')")
        print()
        print("# List all available tables:")
        print("from src.my_catalog import list_tables")
        print("tables = list_tables()")
        
        print("\n🎉 Demo Complete!")
        print("You now have a fully functional 'Code as a Catalog' system")
        print("with browsable documentation generated from your table definitions!")
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 