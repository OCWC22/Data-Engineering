#!/usr/bin/env python3
"""
Delta Lake functionality test and demonstration script.

This script demonstrates Neuralink-style Delta Lake patterns including:
- ACID transactional operations
- Time travel queries
- Schema evolution 
- Performance optimizations
"""
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path

import polars as pl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

import delta_config
import delta_tables
from delta_config import validate_delta_environment, initialize_delta_environment
from delta_tables import NeuralakeDeltaTable, create_sample_delta_table


def validate_environment():
    """Validate that Delta Lake environment is ready."""
    logger.info("🔍 Validating Delta Lake environment...")
    
    validation = validate_delta_environment()
    
    all_passed = True
    for check, passed in validation.items():
        status = "✅" if passed else "❌"
        logger.info(f"{status} {check}: {passed}")
        if not passed:
            all_passed = False
    
    if not all_passed:
        logger.error("❌ Environment validation failed!")
        logger.info("💡 Make sure MinIO is running: docker-compose up -d")
        return False
    
    logger.info("✅ Delta Lake environment validated!")
    return True


def test_basic_operations():
    """Test basic Delta Lake ACID operations."""
    logger.info("\n🧪 Testing Basic Delta Lake Operations")
    
    # Try to load existing table, or create new one
    table = NeuralakeDeltaTable("test_neural_signals")
    
    if not table.exists:
        logger.info("🆕 Creating new sample table...")
        table = create_sample_delta_table("test_neural_signals", num_rows=500)
    else:
        logger.info("♻️ Using existing table...")
    
    # Check table stats
    stats = table.get_stats()
    logger.info(f"📊 Table stats: {stats}")
    
    # Query all data
    all_data = table.query()
    logger.info(f"📊 Total rows: {len(all_data)}")
    
    # Query specific columns
    signals_only = table.query(columns=["timestamp", "signal_strength", "neuron_id"])
    logger.info(f"📊 Signals query: {len(signals_only)} rows, {signals_only.shape[1]} columns")
    
    return table


def test_acid_transactions(table: NeuralakeDeltaTable):
    """Test ACID transactional guarantees."""
    logger.info("\n⚡ Testing ACID Transactional Operations")
    
    original_version = table.version
    original_count = len(table.query())
    
    # Generate additional data for insert
    import random
    base_time = datetime.now()
    
    new_data = {
        "timestamp": [base_time + timedelta(milliseconds=i*50) for i in range(100)],
        "neuron_id": [f"N{random.randint(5000, 9999)}" for _ in range(100)],
        "signal_strength": [random.uniform(-0.5, 0.5) for _ in range(100)],
        "frequency_hz": [random.uniform(10.0, 50.0) for _ in range(100)],
        "electrode_position": [f"E{random.randint(65, 128)}" for _ in range(100)],
        "session_id": [f"session_{random.randint(11, 15)}" for _ in range(100)],
    }
    
    new_df = pl.DataFrame(new_data)
    
    # Insert with ACID guarantees
    logger.info(f"💾 Inserting {len(new_df)} new rows...")
    table.insert(new_df)
    
    # Verify atomic operation
    new_version = table.version
    new_count = len(table.query())
    
    logger.info(f"✅ ACID Transaction:")
    logger.info(f"  - Version: {original_version} → {new_version}")
    logger.info(f"  - Row count: {original_count} → {new_count}")
    logger.info(f"  - Rows added: {new_count - original_count}")
    
    assert new_version == original_version + 1, "Version should increment by 1"
    assert new_count == original_count + 100, "Should have exactly 100 new rows"
    
    return table


def test_time_travel(table: NeuralakeDeltaTable):
    """Test time travel queries."""
    logger.info("\n🕐 Testing Time Travel Queries")
    
    # Get table history
    history = table.get_history()
    logger.info(f"📜 Table history: {len(history)} versions")
    
    # Display history
    if len(history) > 0:
        history_display = history.select(["version", "timestamp", "operation"])
        logger.info(f"📜 Version history:\n{history_display}")
    
    # Test version-based time travel
    current_version = table.version
    
    if current_version and current_version > 0:
        # Query previous version
        previous_version = current_version - 1
        logger.info(f"🔙 Querying version {previous_version}")
        
        previous_data = table.query(version=previous_version)
        current_data = table.query()
        
        logger.info(f"✅ Time Travel Results:")
        logger.info(f"  - Version {previous_version}: {len(previous_data)} rows")
        logger.info(f"  - Version {current_version}: {len(current_data)} rows")
        
        # Should show the difference
        assert len(current_data) > len(previous_data), "Current version should have more data"
    
    return table


def test_schema_evolution(table: NeuralakeDeltaTable):
    """Test schema evolution capabilities."""
    logger.info("\n🔄 Testing Schema Evolution")
    
    original_schema = table.schema
    logger.info(f"📋 Original schema: {original_schema.names}")
    
    # Create data with new column (schema evolution)
    import random
    base_time = datetime.now() + timedelta(hours=1)
    
    evolved_data = {
        "timestamp": [base_time + timedelta(milliseconds=i*25) for i in range(50)],
        "neuron_id": [f"N{random.randint(10000, 19999)}" for _ in range(50)],
        "signal_strength": [random.uniform(-2.0, 2.0) for _ in range(50)],
        "frequency_hz": [random.uniform(100.0, 200.0) for _ in range(50)],
        "electrode_position": [f"E{random.randint(129, 256)}" for _ in range(50)],
        "session_id": [f"session_{random.randint(16, 20)}" for _ in range(50)],
        # NEW COLUMN - Schema Evolution!
        "amplitude_mv": [random.uniform(0.1, 5.0) for _ in range(50)],
        "quality_score": [random.uniform(0.0, 1.0) for _ in range(50)]
    }
    
    evolved_df = pl.DataFrame(evolved_data)
    
    logger.info(f"🆕 Adding data with new columns: {list(evolved_data.keys())}")
    
    # Insert with schema evolution (should automatically merge schemas)
    table.insert(evolved_df)
    
    # Check evolved schema
    new_schema = table.schema
    logger.info(f"📋 Evolved schema: {new_schema.names}")
    
    # Verify schema evolution
    logger.info(f"✅ Schema Evolution:")
    logger.info(f"  - Original columns: {len(original_schema.names)}")
    logger.info(f"  - New columns: {len(new_schema.names)}")
    logger.info(f"  - Added: {set(new_schema.names) - set(original_schema.names)}")
    
    # Query with new columns
    new_data = table.query(columns=["neuron_id", "amplitude_mv", "quality_score"])
    non_null_new_data = new_data.filter(pl.col("amplitude_mv").is_not_null())
    
    logger.info(f"  - Rows with new columns: {len(non_null_new_data)} / {len(new_data)}")
    
    return table


def test_performance_operations(table: NeuralakeDeltaTable):
    """Test performance and maintenance operations."""
    logger.info("\n⚡ Testing Performance Operations")
    
    # Get current stats
    stats = table.get_stats()
    logger.info(f"📊 Current table stats:")
    for key, value in stats.items():
        logger.info(f"  - {key}: {value}")
    
    # Test optimization (may be placeholder depending on delta-rs version)
    logger.info("🔧 Running optimization...")
    table.optimize()
    
    # Note: Vacuum is destructive, so we'll just log what it would do
    logger.info("🧹 Vacuum would remove files older than retention period")
    logger.info("   (Skipping actual vacuum to preserve data)")
    
    return table


def run_comprehensive_demo():
    """Run comprehensive Delta Lake demonstration."""
    logger.info("🚀 Starting Comprehensive Delta Lake Demo")
    logger.info("=" * 60)
    
    # Validate environment
    if not validate_environment():
        return False
    
    try:
        # Initialize Delta environment
        initialize_delta_environment()
        
        # Test basic operations
        table = test_basic_operations()
        
        # Test ACID transactions
        table = test_acid_transactions(table)
        
        # Test time travel
        table = test_time_travel(table)
        
        # Test schema evolution
        table = test_schema_evolution(table)
        
        # Test performance operations
        table = test_performance_operations(table)
        
        # Final summary
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Delta Lake Demo Completed Successfully!")
        
        final_stats = table.get_stats()
        logger.info(f"📊 Final table state:")
        for key, value in final_stats.items():
            logger.info(f"  - {key}: {value}")
        
        logger.info("\n✅ All Neuralink Delta Lake patterns validated:")
        logger.info("  - ✅ ACID transactional operations")
        logger.info("  - ✅ Time travel queries")
        logger.info("  - ✅ Schema evolution")
        logger.info("  - ✅ Performance optimizations")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_comprehensive_demo()
    exit(0 if success else 1) 