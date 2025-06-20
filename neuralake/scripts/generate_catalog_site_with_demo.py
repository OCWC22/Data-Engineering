#!/usr/bin/env python3
"""
Generate Static Catalog Site with Demo Tables

Script to generate a browsable HTML catalog with demonstration tables.
Shows the complete "Code as a Catalog" workflow.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from catalog_core import default_catalog, table, register_static_table
from ssg import CatalogSiteGenerator
import logging
import polars as pl
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define demo tables directly in this script

@table(
    description="Enterprise user data with comprehensive user profiles",
    tags=["users", "core", "analytics"],
    owner="data-engineering"
)
def users():
    """User master data with authentication and profile information."""
    return pl.LazyFrame({
        "user_id": [1, 2, 3, 4, 5],
        "username": ["alice_data", "bob_analyst", "charlie_eng", "diana_sci", "eve_admin"],
        "email": [
            "alice@neuralake.com",
            "bob@neuralake.com", 
            "charlie@neuralake.com",
            "diana@neuralake.com",
            "eve@neuralake.com"
        ],
        "created_at": [
            datetime(2024, 1, 15),
            datetime(2024, 2, 20),
            datetime(2024, 3, 10),
            datetime(2024, 4, 5),
            datetime(2024, 5, 12)
        ],
        "is_active": [True, True, False, True, True],
        "user_type": ["analyst", "analyst", "engineer", "scientist", "admin"]
    })

@table(
    description="Real-time event stream data with user interactions",
    tags=["events", "streaming", "analytics", "real-time"],
    owner="data-engineering",
    partition_columns=["event_date", "event_type"]
)
def user_events():
    """User interaction events captured in real-time."""
    base_time = datetime(2025, 6, 19, 12, 0)
    
    events = []
    for i in range(20):
        event_time = base_time + timedelta(minutes=i*2)
        events.append({
            "event_id": f"evt_{i:03d}",
            "user_id": (i % 5) + 1,
            "event_type": ["page_view", "click", "api_call", "login", "logout"][i % 5],
            "timestamp": event_time,
            "event_date": event_time.date(),
            "session_id": f"sess_{(i // 10):02d}"
        })
    
    return pl.LazyFrame(events)

@table(
    description="Neural signal data from research experiments",
    tags=["neuroscience", "signals", "research", "time-series"],
    owner="research-team"
)
def neural_signals():
    """Neural signal recordings from cortical electrodes."""
    cortical_regions = ["motor_cortex", "visual_cortex", "auditory_cortex", "prefrontal"]
    base_time = datetime(2025, 6, 19, 9, 0)
    
    signals = []
    for i in range(50):
        timestamp = base_time + timedelta(milliseconds=i*10)
        region = cortical_regions[i % 4]
        
        signals.append({
            "signal_id": f"sig_{i:04d}",
            "neuron_id": (i % 20) + 1,
            "cortical_region": region,
            "signal_strength": 0.5 + (i % 10) * 0.1,
            "frequency_hz": 40 + (i % 4) * 20,
            "timestamp": timestamp,
            "experiment_id": f"exp_{(i // 25) + 1:02d}",
            "spike_detected": (i % 3) == 0
        })
    
    return pl.LazyFrame(signals)

# Register a mock static table
class MockDeltaTable:
    def __init__(self, name):
        self.name = name
        
    def query(self, **kwargs):
        """Mock query method that returns sample data."""
        return pl.LazyFrame({
            "transaction_id": [f"txn_{i:05d}" for i in range(10)],
            "user_id": [i % 5 + 1 for i in range(10)],
            "amount": [round(100 + i * 25.5, 2) for i in range(10)],
            "transaction_type": [["purchase", "refund"][i % 2] for i in range(10)],
            "timestamp": [datetime(2025, 6, 19, 10, i) for i in range(10)]
        })

def main():
    """Generate the catalog site with demo tables."""
    
    logger.info("🌐 Starting Catalog Site Generation with Demo Tables")
    
    # Register the mock Delta table
    mock_transactions = MockDeltaTable("transactions")
    register_static_table(
        mock_transactions,
        "transactions", 
        description="Financial transaction records with ACID guarantees",
        tags=["finance", "transactions", "delta", "acid"],
        owner="finance-team"
    )
    
    # Check registered tables
    tables = default_catalog.list_tables()
    logger.info(f"Found {len(tables)} registered tables: {tables}")
    
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
        project_name="Neuralake Data Catalog - Demo"
    )
    
    logger.info("✅ Catalog site generation complete!")
    logger.info(f"   Open: file://{output_dir.absolute()}/index.html")
    
    # Test a table query to verify functionality
    logger.info("\n🧪 Testing table access...")
    try:
        for test_table in tables[:2]:  # Test first 2 tables
            df = default_catalog.table(test_table)
            data = df.collect()
            logger.info(f"✅ Successfully queried '{test_table}': {data.shape} rows/cols")
            logger.info(f"   Columns: {data.columns}")
    except Exception as e:
        logger.error(f"❌ Failed to query test table: {e}")

if __name__ == "__main__":
    main() 