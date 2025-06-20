"""
Demo Catalog - Showcase "Code as a Catalog" Implementation

This module demonstrates the complete catalog system with:
- Function-based tables using @table decorator
- Static table registration for Delta/Parquet tables
- Rich metadata and schema definitions
- Multiple table types and use cases
"""
import polars as pl
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

# Import our catalog system
try:
    from .catalog_core import table, register_static_table, TableType, default_catalog
    from .delta_tables import NeuralakeDeltaTable
except ImportError:
    # Fallback for direct script execution
    from catalog_core import table, register_static_table, TableType, default_catalog
    from delta_tables import NeuralakeDeltaTable

logger = logging.getLogger(__name__)

# Function-based tables using @table decorator

@table(
    description="Enterprise user data with comprehensive user profiles",
    tags=["users", "core", "analytics"],
    owner="data-engineering",
    schema={
        "user_id": "Int64",
        "username": "Utf8", 
        "email": "Utf8",
        "created_at": "Datetime",
        "last_login": "Datetime",
        "is_active": "Boolean",
        "user_type": "Utf8"
    }
)
def users():
    """
    User master data with authentication and profile information.
    
    This table contains the core user registry for the platform,
    including authentication details and profile metadata.
    """
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
        "last_login": [
            datetime(2025, 6, 19, 10, 30),
            datetime(2025, 6, 18, 14, 45),
            datetime(2025, 6, 19, 9, 15),
            datetime(2025, 6, 17, 16, 20),
            datetime(2025, 6, 19, 11, 0)
        ],
        "is_active": [True, True, False, True, True],
        "user_type": ["analyst", "analyst", "engineer", "scientist", "admin"]
    })

@table(
    description="Real-time event stream data with user interactions",
    tags=["events", "streaming", "analytics", "real-time"],
    owner="data-engineering",
    partition_columns=["event_date", "event_type"],
    schema={
        "event_id": "Utf8",
        "user_id": "Int64",
        "event_type": "Utf8",
        "event_data": "Utf8", 
        "timestamp": "Datetime",
        "event_date": "Date",
        "session_id": "Utf8"
    }
)
def user_events():
    """
    User interaction events captured in real-time.
    
    Tracks all user interactions including clicks, page views,
    API calls, and system events for analytics and monitoring.
    """
    base_time = datetime(2025, 6, 19, 12, 0)
    
    events = []
    for i in range(50):
        event_time = base_time + timedelta(minutes=i*2)
        events.append({
            "event_id": f"evt_{i:03d}",
            "user_id": (i % 5) + 1,  # Cycle through users 1-5
            "event_type": ["page_view", "click", "api_call", "login", "logout"][i % 5],
            "event_data": f'{{"page": "/dashboard", "duration": {(i*17) % 300}}}',
            "timestamp": event_time,
            "event_date": event_time.date(),
            "session_id": f"sess_{(i // 10):02d}"
        })
    
    return pl.LazyFrame(events)

@table(
    description="Neural signal data from research experiments",
    tags=["neuroscience", "signals", "research", "time-series"],
    owner="research-team",
    schema={
        "signal_id": "Utf8",
        "neuron_id": "Int64",
        "cortical_region": "Utf8",
        "signal_strength": "Float64",
        "frequency_hz": "Float64",
        "timestamp": "Datetime",
        "experiment_id": "Utf8",
        "spike_detected": "Boolean"
    }
)
def neural_signals():
    """
    Neural signal recordings from cortical electrodes.
    
    High-frequency neural data captured during experiments,
    including spike detection and frequency analysis results.
    """
    import random
    random.seed(42)  # For reproducible demo data
    
    cortical_regions = ["motor_cortex", "visual_cortex", "auditory_cortex", "prefrontal"]
    base_time = datetime(2025, 6, 19, 9, 0)
    
    signals = []
    for i in range(100):
        timestamp = base_time + timedelta(milliseconds=i*10)
        region = cortical_regions[i % 4]
        
        # Simulate realistic neural signal patterns
        base_freq = {"motor_cortex": 40, "visual_cortex": 60, "auditory_cortex": 80, "prefrontal": 20}[region]
        signal_strength = random.normalvariate(0.5, 0.15)
        frequency = base_freq + random.normalvariate(0, 5)
        
        signals.append({
            "signal_id": f"sig_{i:04d}",
            "neuron_id": (i % 20) + 1,
            "cortical_region": region,
            "signal_strength": signal_strength,
            "frequency_hz": frequency,
            "timestamp": timestamp,
            "experiment_id": f"exp_{(i // 25) + 1:02d}",
            "spike_detected": signal_strength > 0.7
        })
    
    return pl.LazyFrame(signals)

@table(
    description="Data quality metrics and validation results",
    tags=["quality", "monitoring", "validation", "metadata"],
    owner="data-engineering",
    schema={
        "table_name": "Utf8",
        "check_timestamp": "Datetime",
        "completeness_score": "Float64",
        "accuracy_score": "Float64",
        "consistency_score": "Float64",
        "timeliness_score": "Float64",
        "overall_score": "Float64",
        "issues_found": "Int64",
        "last_updated": "Datetime"
    }
)
def data_quality_metrics():
    """
    Data quality assessment results across all datasets.
    
    Tracks completeness, accuracy, consistency, and timeliness
    metrics for all tables in the data platform.
    """
    return pl.LazyFrame({
        "table_name": ["users", "user_events", "neural_signals", "part", "supplier"],
        "check_timestamp": [datetime(2025, 6, 19, 8, 0) for _ in range(5)],
        "completeness_score": [0.98, 0.95, 0.99, 0.97, 0.96],
        "accuracy_score": [0.99, 0.94, 0.98, 0.95, 0.97],
        "consistency_score": [0.97, 0.93, 0.99, 0.96, 0.95],
        "timeliness_score": [0.95, 0.99, 0.98, 0.90, 0.92],
        "overall_score": [0.97, 0.95, 0.99, 0.95, 0.95],
        "issues_found": [2, 8, 1, 5, 4],
        "last_updated": [datetime(2025, 6, 19, 7, 30) for _ in range(5)]
    })

# Example of registering a Delta table (if Delta Lake is available)
def register_delta_tables():
    """Register Delta Lake tables in the catalog."""
    try:
        # Example Delta table registration
        # In practice, this would point to existing Delta tables
        
        # Mock registration since we may not have actual Delta tables
        class MockDeltaTable:
            def __init__(self, name):
                self.name = name
                
            def query(self, **kwargs):
                """Mock query method that returns sample data."""
                if self.name == "transactions":
                    return pl.LazyFrame({
                        "transaction_id": [f"txn_{i:05d}" for i in range(10)],
                        "user_id": [i % 5 + 1 for i in range(10)],
                        "amount": [round(100 + i * 25.5, 2) for i in range(10)],
                        "transaction_type": [["purchase", "refund"][i % 2] for i in range(10)],
                        "timestamp": [datetime(2025, 6, 19, 10, i) for i in range(10)]
                    })
                elif self.name == "inventory":
                    return pl.LazyFrame({
                        "item_id": [f"item_{i:03d}" for i in range(15)],
                        "quantity": [100 - i*3 for i in range(15)],
                        "location": [f"warehouse_{(i % 3) + 1}" for i in range(15)],
                        "last_updated": [datetime(2025, 6, 19, 8, i*2) for i in range(15)]
                    })
                else:
                    return pl.LazyFrame({"id": [1], "data": ["sample"]})
        
        # Register mock Delta tables
        mock_transactions = MockDeltaTable("transactions")
        register_static_table(
            mock_transactions,
            "transactions", 
            description="Financial transaction records with ACID guarantees",
            tags=["finance", "transactions", "delta", "acid"],
            owner="finance-team",
            schema={
                "transaction_id": "Utf8",
                "user_id": "Int64", 
                "amount": "Float64",
                "transaction_type": "Utf8",
                "timestamp": "Datetime"
            }
        )
        
        mock_inventory = MockDeltaTable("inventory") 
        register_static_table(
            mock_inventory,
            "inventory",
            description="Real-time inventory tracking with warehouse locations",
            tags=["inventory", "warehouse", "real-time", "delta"],
            owner="operations-team",
            partition_columns=["location"],
            schema={
                "item_id": "Utf8",
                "quantity": "Int64",
                "location": "Utf8", 
                "last_updated": "Datetime"
            }
        )
        
        logger.info("✅ Successfully registered Delta tables in catalog")
        
    except Exception as e:
        logger.warning(f"Could not register Delta tables: {e}")

# Auto-register Delta tables when module is imported
register_delta_tables()

# Create a convenience function to get the demo catalog
def get_demo_catalog():
    """Get the default catalog with all demo tables registered."""
    return default_catalog

# Function to list all demo tables
def list_demo_tables():
    """List all tables registered in the demo catalog."""
    return default_catalog.list_tables()

# Function to generate catalog site
def generate_demo_catalog_site(output_dir: str = "demo-catalog-site"):
    """
    Generate static site for the demo catalog.
    
    Args:
        output_dir: Directory to output the static site
    """
    try:
        from .ssg import CatalogSiteGenerator
    except ImportError:
        from ssg import CatalogSiteGenerator
    
    # Export catalog metadata
    catalog_metadata = default_catalog.export_catalog_metadata()
    
    # Generate site
    from pathlib import Path
    generator = CatalogSiteGenerator(Path(output_dir))
    generator.generate_site(catalog_metadata, "Neuralake Demo Data Catalog")
    
    logger.info(f"📚 Demo catalog site generated at: {Path(output_dir).absolute()}")
    logger.info(f"   Open: file://{Path(output_dir).absolute()}/index.html")
    
    return Path(output_dir).absolute()

logger.info("📚 Demo catalog tables registered successfully")
logger.info("   Function tables: users, user_events, neural_signals, data_quality_metrics")
logger.info("   Static tables: transactions, inventory")
logger.info("   Use demo_catalog.generate_demo_catalog_site() to create static site") 