# API Reference: `ParquetTable`

Base class for protocol classes.

Protocol classes are defined as::

class Proto(Protocol):
def meth(self) -> int:
...

Such classes are primarily used with static type checkers that recognize
structural subtyping (static duck-typing), for example::

class C:
def meth(self) -> int:
return 0

def func(x: Proto) -> int:
return x.meth()

func(C())  # Passes static type check

See PEP 544 for details. Protocol classes decorated with
@typing.runtime_checkable act as simple-minded runtime protocols that check
only the presence of given attributes, ignoring their type signatures.
Protocol classes can be generic, they are defined as::

class GenProto(Protocol[T]):
def meth(self) -> T:
...

## Constructor

```python
def __init__(self, name: str, uri: str, partitioning: list[neuralake.core.tables.util.Partition], partitioning_scheme: neuralake.core.tables.util.PartitioningScheme = <PartitioningScheme.DIRECTORY: 1>, description: str = '', docs_filters: list[neuralake.core.tables.filters.Filter] = [], docs_columns: list[str] | None = None, roapi_opts: neuralake.core.tables.util.RoapiOptions | None = None, parquet_file_name: str = 'df.parquet', table_metadata_args: dict[str, typing.Any] | None = None):
```

Initialize self.  See help(type(self)) for accurate signature.

## Methods

### `__call__`

```python
def __call__(self, filters: Union[Sequence[neuralake.core.tables.filters.Filter], Sequence[Sequence[neuralake.core.tables.filters.Filter]], NoneType] = None, columns: Optional[list[str]] = None, boto3_session: boto3.session.Session | None = None, endpoint_url: str | None = None, **kwargs: Any) -> neuralake.core.dataframe.frame.NlkDataFrame:
```

Call self as a function.

### `build_file_fragment`

```python
def build_file_fragment(self, filters: list[neuralake.core.tables.filters.Filter]) -> str:
```

Returns a file path from the base table URI with the given filters.
This will raise an error if the filter does not specify all partitions.

This is currently used to generate the file path used by ROAPI to infer schemas.

### `get_schema`

```python
def get_schema(self) -> neuralake.core.tables.metadata.TableSchema:
```

Returns the schema of the table, used to generate the web catalog.
