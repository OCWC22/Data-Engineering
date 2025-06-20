"""
Test the catalog core functionality.
"""
import pytest
import polars as pl
from src.catalog_core import (
    table, register_static_table, Catalog, TableType, 
    default_catalog, _catalog_registry
)
from src.delta_tables import NeuralakeDeltaTable

@pytest.fixture(autouse=True)
def clear_registry():
    """Clear the registry before each test."""
    _catalog_registry._tables.clear()
    _catalog_registry._table_functions.clear()
    _catalog_registry._table_objects.clear()
    yield
    # Clear after test too
    _catalog_registry._tables.clear()
    _catalog_registry._table_functions.clear()
    _catalog_registry._table_objects.clear()

def test_function_table_registration():
    """Test registering function-based tables."""
    
    @table(description="Test user data")
    def test_users():
        """User data for testing."""
        return pl.LazyFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35]
        })
    
    # Verify registration
    tables = default_catalog.list_tables()
    assert "test_users" in tables
    
    # Test table access
    data = default_catalog.table("test_users").collect()
    assert data.height == 3
    assert set(data.columns) == {"id", "name", "age"}
    
    # Test metadata
    metadata = default_catalog.describe_table("test_users")
    assert metadata["metadata"]["description"] == "Test user data"
    assert metadata["metadata"]["table_type"] == "function"

def test_static_table_registration():
    """Test registering static table objects."""
    # Mock DeltaTable for testing
    class MockDeltaTable:
        def __init__(self, name):
            self.name = name
        
        def query(self, **kwargs):
            return pl.LazyFrame({
                "event_id": [1, 2, 3],
                "event_type": ["click", "view", "purchase"],
                "timestamp": ["2025-01-01", "2025-01-02", "2025-01-03"]
            })
    
    mock_table = MockDeltaTable("events")
    register_static_table(
        mock_table, 
        "events",
        description="User events data",
        tags=["events", "analytics"]
    )
    
    # Verify registration
    tables = default_catalog.list_tables()
    assert "events" in tables
    
    # Test table access
    data = default_catalog.table("events").collect()
    assert data.height == 3
    assert set(data.columns) == {"event_id", "event_type", "timestamp"}
    
    # Test metadata
    metadata = default_catalog.describe_table("events")
    assert metadata["metadata"]["description"] == "User events data"
    assert "events" in metadata["metadata"]["tags"]

def test_catalog_table_listing():
    """Test table listing and filtering."""
    
    @table(description="Function table")
    def func_table():
        return pl.LazyFrame({"id": [1]})
    
    # Register a mock static table
    class MockTable:
        def query(self):
            return pl.LazyFrame({"id": [1]})
    
    register_static_table(MockTable(), "static_table", description="Static table")
    
    # Test listing all tables
    all_tables = default_catalog.list_tables()
    assert "func_table" in all_tables
    assert "static_table" in all_tables
    
    # Test filtering by type
    function_tables = default_catalog.list_tables(TableType.FUNCTION)
    assert "func_table" in function_tables
    assert "static_table" not in function_tables

def test_catalog_metadata_export():
    """Test exporting catalog metadata."""
    
    @table(description="Export test table", tags=["test"])
    def export_test():
        return pl.LazyFrame({"col1": [1, 2], "col2": ["a", "b"]})
    
    metadata = default_catalog.export_catalog_metadata()
    
    assert "tables" in metadata
    assert "export_test" in metadata["tables"]
    assert metadata["tables"]["export_test"]["description"] == "Export test table"
    assert "test" in metadata["tables"]["export_test"]["tags"]
    assert metadata["total_tables"] >= 1

def test_table_schema_inference():
    """Test schema inference from table data."""
    
    @table(description="Schema test")
    def schema_table():
        return pl.LazyFrame({
            "int_col": [1, 2, 3],
            "str_col": ["a", "b", "c"],
            "float_col": [1.1, 2.2, 3.3],
            "bool_col": [True, False, True]
        })
    
    description = default_catalog.describe_table("schema_table")
    schema = description["inferred_schema"]
    
    assert "int_col" in schema
    assert "str_col" in schema
    assert "float_col" in schema
    assert "bool_col" in schema
    assert description["column_count"] == 4

def test_table_decorator_with_docstring():
    """Test that table decorator extracts docstring when no description provided."""
    
    @table()
    def docstring_table():
        """This is a test table with docstring."""
        return pl.LazyFrame({"test": [1, 2, 3]})
    
    metadata = default_catalog.describe_table("docstring_table")
    assert metadata["metadata"]["description"] == "This is a test table with docstring."

def test_table_not_found_error():
    """Test error handling when table is not found."""
    
    with pytest.raises(ValueError, match="Table 'nonexistent' not found"):
        default_catalog.table("nonexistent")
    
    with pytest.raises(ValueError, match="Table 'nonexistent' not found"):
        default_catalog.describe_table("nonexistent")

def test_table_with_parameters():
    """Test table function that accepts parameters."""
    
    @table(description="Parameterized table")
    def param_table(limit: int = 10):
        data = {"id": list(range(limit)), "value": [f"val_{i}" for i in range(limit)]}
        return pl.LazyFrame(data)
    
    # Test with default parameter
    data_default = default_catalog.table("param_table").collect()
    assert data_default.height == 10
    
    # Test with custom parameter
    data_custom = default_catalog.table("param_table", limit=5).collect()
    assert data_custom.height == 5

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 