"""
Core catalog system implementing 'Code as a Catalog' philosophy.
Allows defining tables in code using decorators and class definitions.
"""
import inspect
import logging
from typing import Dict, Any, Optional, List, Callable, Union, Type
from dataclasses import dataclass, field
from enum import Enum
import polars as pl
from pathlib import Path
import json
from datetime import datetime

try:
    from .delta_tables import NeuralakeDeltaTable
except ImportError:
    # Fallback for direct script execution
    from delta_tables import NeuralakeDeltaTable
try:
    from .config import get_config
except ImportError:
    # Fallback for direct script execution
    from config import get_config

logger = logging.getLogger(__name__)

class TableType(Enum):
    """Types of tables supported in the catalog."""
    PARQUET = "parquet"
    DELTA = "delta"
    FUNCTION = "function"
    VIEW = "view"

@dataclass
class TableMetadata:
    """Metadata for catalog tables."""
    name: str
    table_type: TableType
    description: str = ""
    schema: Optional[Dict[str, str]] = None
    partition_columns: List[str] = field(default_factory=list)
    source_module: str = ""
    source_function: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    owner: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for serialization."""
        return {
            "name": self.name,
            "table_type": self.table_type.value,
            "description": self.description,
            "schema": self.schema or {},
            "partition_columns": self.partition_columns,
            "source_module": self.source_module,
            "source_function": self.source_function,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "owner": self.owner
        }

class CatalogRegistry:
    """Central registry for all catalog tables."""
    
    def __init__(self):
        self._tables: Dict[str, TableMetadata] = {}
        self._table_functions: Dict[str, Callable] = {}
        self._table_objects: Dict[str, Any] = {}
    
    def register_table(self, metadata: TableMetadata, 
                      table_obj: Any = None, 
                      table_func: Callable = None):
        """Register a table in the catalog."""
        self._tables[metadata.name] = metadata
        
        if table_obj is not None:
            self._table_objects[metadata.name] = table_obj
        
        if table_func is not None:
            self._table_functions[metadata.name] = table_func
        
        logger.info(f"Registered table '{metadata.name}' of type {metadata.table_type.value}")
    
    def get_table_metadata(self, name: str) -> Optional[TableMetadata]:
        """Get metadata for a table."""
        return self._tables.get(name)
    
    def get_table_function(self, name: str) -> Optional[Callable]:
        """Get function for a function-based table."""
        return self._table_functions.get(name)
    
    def get_table_object(self, name: str) -> Any:
        """Get table object (ParquetTable, DeltaTable, etc.)."""
        return self._table_objects.get(name)
    
    def list_tables(self, table_type: Optional[TableType] = None) -> List[str]:
        """List all tables, optionally filtered by type."""
        if table_type is None:
            return list(self._tables.keys())
        
        return [name for name, metadata in self._tables.items() 
                if metadata.table_type == table_type]
    
    def export_metadata(self) -> Dict[str, Any]:
        """Export all table metadata for static site generation."""
        return {
            "tables": {name: metadata.to_dict() 
                      for name, metadata in self._tables.items()},
            "export_time": datetime.now().isoformat(),
            "total_tables": len(self._tables)
        }

# Global registry instance
_catalog_registry = CatalogRegistry()

def table(name: Optional[str] = None, 
         description: str = "",
         table_type: TableType = TableType.FUNCTION,
         schema: Optional[Dict[str, str]] = None,
         partition_columns: List[str] = None,
         tags: List[str] = None,
         owner: str = ""):
    """
    Decorator to register a function as a table in the catalog.
    
    Usage:
        @table(description="User data from API")
        def users() -> pl.LazyFrame:
            return pl.LazyFrame({"id": [1, 2], "name": ["Alice", "Bob"]})
    """
    def decorator(func: Callable) -> Callable:
        table_name = name or func.__name__
        
        # Extract docstring if no description provided
        table_description = description or (func.__doc__ or "").strip()
        
        # Get module information
        module_name = func.__module__ if hasattr(func, '__module__') else ""
        
        # Create metadata
        metadata = TableMetadata(
            name=table_name,
            table_type=table_type,
            description=table_description,
            schema=schema,
            partition_columns=partition_columns or [],
            source_module=module_name,
            source_function=func.__name__,
            tags=tags or [],
            owner=owner
        )
        
        # Register in global catalog
        _catalog_registry.register_table(metadata, table_func=func)
        
        # Add metadata to function
        func._catalog_metadata = metadata
        
        return func
    
    return decorator

def register_static_table(table_obj: Union[NeuralakeDeltaTable, Any], 
                         name: str,
                         description: str = "",
                         schema: Optional[Dict[str, str]] = None,
                         partition_columns: List[str] = None,
                         tags: List[str] = None,
                         owner: str = ""):
    """
    Register a static table object (DeltaTable, ParquetTable, etc.) in the catalog.
    
    Usage:
        delta_table = NeuralakeDeltaTable("user_events")
        register_static_table(delta_table, "user_events", 
                             description="User interaction events")
    """
    # Determine table type
    if isinstance(table_obj, NeuralakeDeltaTable):
        table_type = TableType.DELTA
    else:
        # Assume ParquetTable or similar
        table_type = TableType.PARQUET
    
    metadata = TableMetadata(
        name=name,
        table_type=table_type,
        description=description,
        schema=schema,
        partition_columns=partition_columns or [],
        tags=tags or [],
        owner=owner
    )
    
    _catalog_registry.register_table(metadata, table_obj=table_obj)

class Catalog:
    """
    High-level catalog interface providing unified access to all tables.
    """
    
    def __init__(self, registry: CatalogRegistry = None):
        self.registry = registry or _catalog_registry
    
    def table(self, name: str, **kwargs) -> pl.LazyFrame:
        """
        Get a table as a Polars LazyFrame.
        
        Args:
            name: Table name
            **kwargs: Additional arguments passed to table function/object
        
        Returns:
            Polars LazyFrame with the table data
        """
        metadata = self.registry.get_table_metadata(name)
        if not metadata:
            raise ValueError(f"Table '{name}' not found in catalog")
        
        if metadata.table_type == TableType.FUNCTION:
            # Execute function to get data
            func = self.registry.get_table_function(name)
            if not func:
                raise ValueError(f"Function for table '{name}' not found")
            
            result = func(**kwargs)
            
            # Ensure we return a LazyFrame
            if isinstance(result, pl.DataFrame):
                return result.lazy()
            elif isinstance(result, pl.LazyFrame):
                return result
            else:
                raise ValueError(f"Table function '{name}' must return DataFrame or LazyFrame")
        
        elif metadata.table_type in [TableType.DELTA, TableType.PARQUET]:
            # Get data from table object
            table_obj = self.registry.get_table_object(name)
            if not table_obj:
                raise ValueError(f"Table object for '{name}' not found")
            
            if isinstance(table_obj, NeuralakeDeltaTable):
                return table_obj.query(**kwargs)
            else:
                # Try query method first, then __call__ method
                if hasattr(table_obj, 'query'):
                    result = table_obj.query(**kwargs)
                else:
                    result = table_obj(**kwargs)
                
                if isinstance(result, pl.DataFrame):
                    return result.lazy()
                elif isinstance(result, pl.LazyFrame):
                    return result
                else:
                    # Convert to LazyFrame if needed
                    return pl.LazyFrame(result)
        
        else:
            raise ValueError(f"Unsupported table type: {metadata.table_type}")
    
    def list_tables(self, table_type: Optional[TableType] = None) -> List[str]:
        """List all available tables."""
        return self.registry.list_tables(table_type)
    
    def describe_table(self, name: str) -> Dict[str, Any]:
        """Get detailed information about a table."""
        metadata = self.registry.get_table_metadata(name)
        if not metadata:
            raise ValueError(f"Table '{name}' not found in catalog")
        
        # Get sample data to infer schema if not provided
        try:
            sample_data = self.table(name).limit(1).collect()
            inferred_schema = {col: str(dtype) for col, dtype in 
                             zip(sample_data.columns, sample_data.dtypes)}
        except Exception as e:
            logger.warning(f"Could not infer schema for table '{name}': {e}")
            inferred_schema = {}
        
        return {
            "metadata": metadata.to_dict(),
            "inferred_schema": inferred_schema,
            "column_count": len(inferred_schema),
            "available": True
        }
    
    def export_catalog_metadata(self, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """Export catalog metadata for static site generation."""
        metadata = self.registry.export_metadata()
        
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
        
        return metadata

# Global catalog instance
default_catalog = Catalog()

# Convenience functions
def get_table(name: str, **kwargs) -> pl.LazyFrame:
    """Get a table from the default catalog."""
    return default_catalog.table(name, **kwargs)

def list_catalog_tables(table_type: Optional[TableType] = None) -> List[str]:
    """List tables in the default catalog."""
    return default_catalog.list_tables(table_type)

def describe_catalog_table(name: str) -> Dict[str, Any]:
    """Describe a table in the default catalog."""
    return default_catalog.describe_table(name) 