from pathlib import Path
import sys


def setup_path():
    """Setup the Python path for local imports."""
    proj_root = Path(__file__).parent.parent
    if str(proj_root) not in sys.path:
        sys.path.append(str(proj_root))


def main():
    """
    Demonstrates how to use the neuralake demo catalog to query multiple tables.
    
    This script showcases:
    1. Basic table querying from the demo catalog
    2. Multiple table types (function tables, static tables)
    3. Environment-aware configuration (local vs production S3)
    4. Data exploration and simple analytics
    
    The underlying data source (local S3, production S3) is determined
    by the configuration loaded via the NEURALAKE_ENV environment variable.

    By default, the config will load the 'local' environment, which is
    pre-configured to connect to the local MinIO S3 instance.
    You can switch to a different environment (e.g., production) by setting
    the 'NEURALAKE_ENV' environment variable before running this script.
    For example:
    NEURALAKE_ENV=production python -m neuralake.query_data
    """
    setup_path()

    from config import get_config, is_production
    from my_catalog import DemoCatalog, list_tables
    import polars as pl

    config = get_config()
    env = "Production" if is_production() else "Local"
    print(f"🌐 Neuralake Demo Catalog Query ({env} Environment)")
    print(f"📊 S3 Endpoint: {config.s3.endpoint_url}")
    print("=" * 60)

    # List all available tables
    available_tables = list_tables()
    print(f"\n📚 Available Tables in Catalog ({len(available_tables)} total):")
    for table in available_tables:
        metadata = DemoCatalog.describe_table(table)
        table_type = metadata.get('table_type', 'unknown')
        description = metadata.get('description', 'No description')
        print(f"  • {table:20} ({table_type:8}) - {description[:50]}...")

    print("\n" + "=" * 60)
    print("🔍 Running Demo Queries...")

    # Query 1: Users table (function-based)
    print(f"\n1️⃣  Querying 'users' table (Function Table):")
    try:
        users_data = DemoCatalog.table("users").limit(5).collect()
        print(f"✅ Successfully fetched user data: {users_data.shape}")
        print(users_data)
    except Exception as e:
        print(f"❌ Failed to query users table: {e}")

    # Query 2: User events table with filtering
    print(f"\n2️⃣  Querying 'user_events' table with filtering:")
    try:
        events_data = DemoCatalog.table("user_events").filter(
            pl.col("event_type") == "page_view"
        ).limit(3).collect()
        print(f"✅ Successfully fetched filtered events: {events_data.shape}")
        print(events_data)
    except Exception as e:
        print(f"❌ Failed to query user_events table: {e}")

    # Query 3: Neural signals with aggregation
    print(f"\n3️⃣  Querying 'neural_signals' with aggregation:")
    try:
        signals_summary = DemoCatalog.table("neural_signals").group_by(
            "cortical_region"
        ).agg([
            pl.count().alias("signal_count"),
            pl.col("signal_strength").mean().alias("avg_strength"),
            pl.col("spike_detected").sum().alias("total_spikes")
        ]).collect()
        print(f"✅ Successfully aggregated neural signals: {signals_summary.shape}")
        print(signals_summary)
    except Exception as e:
        print(f"❌ Failed to query neural_signals table: {e}")

    # Query 4: Static table (transactions)
    print(f"\n4️⃣  Querying 'transactions' table (Static/Delta Table):")
    try:
        transactions_data = DemoCatalog.table("transactions").limit(5).collect()
        print(f"✅ Successfully fetched transactions: {transactions_data.shape}")
        print(transactions_data)
    except Exception as e:
        print(f"❌ Failed to query transactions table: {e}")

    # Query 5: Join between users and user_events
    print(f"\n5️⃣  Joining users and user_events:")
    try:
        users_df = DemoCatalog.table("users")
        events_df = DemoCatalog.table("user_events")
        
        joined_data = events_df.join(
            users_df, 
            on="user_id", 
            how="inner"
        ).select([
            "username",
            "event_type", 
            "timestamp",
            "user_type"
        ]).limit(10).collect()
        
        print(f"✅ Successfully joined tables: {joined_data.shape}")
        print(joined_data)
    except Exception as e:
        print(f"❌ Failed to join tables: {e}")

    # Query 6: Try the original 'part' table if it exists
    print(f"\n6️⃣  Checking for 'part' table (Original S3 Demo):")
    try:
        # Check if part table exists in catalog
        if "part" in available_tables:
            part_data = DemoCatalog.table("part").limit(5).collect()
            print(f"✅ Successfully fetched part data: {part_data.shape}")
            print(part_data)
        else:
            print("ℹ️  'part' table not found in demo catalog (this is expected)")
            print("    The demo catalog focuses on the new function-based tables")
    except Exception as e:
        print(f"⚠️  Could not query part table: {e}")

    print("\n" + "=" * 60)
    print("🎉 Demo catalog queries completed!")
    print(f"💡 To generate a browsable catalog site, run:")
    print(f"   python -c \"from src.my_catalog import generate_catalog_site; generate_catalog_site()\"")
    print(f"   Then open the generated HTML file in your browser")


if __name__ == "__main__":
    main()
