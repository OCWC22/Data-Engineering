# API Reference: `ModuleDatabase`

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
def __init__(self, db: module) -> None:
```

Initialize self.  See help(type(self)) for accurate signature.

## Methods

### `get_tables`

```python
def get_tables(self, show_deprecated: bool = False) -> dict[str, neuralake.core.tables.metadata.TableProtocol]:
```

*No documentation available.*

### `table`

```python
def table(self, name: str, *args: Any, **kwargs: Any) -> neuralake.core.dataframe.frame.NlkDataFrame:
```

*No documentation available.*

### `tables`

```python
def tables(self, show_deprecated: bool = False) -> list[str]:
```

*No documentation available.*
