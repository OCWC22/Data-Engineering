# API Reference: `NlkDataFrame`

Representation of a Lazy computation graph/query against a DataFrame.

This allows for whole-query optimisation in addition to parallelism, and
is the preferred (and highest-performance) mode of operation for polars.

### Parameters

- **`data`** (*dict*)
  Sequence, ndarray, Series, or pandas.DataFrame Two-dimensional data in various forms; dict input must contain Sequences, Generators, or a `range`. Sequence may contain Series or other Sequences.

- **`schema`** (*Sequence of str*)
  (str,DataType) pairs, or a {str:DataType,} dict The LazyFrame schema may be declared in several ways: * As a dict of {name:type} pairs; if type is None, it will be auto-inferred. * As a list of column names; in this case types are automatically inferred. * As a list of (name,type) pairs; this is equivalent to the dictionary form. If you supply a list of column names that does not match the names in the underlying data, the names given here will overwrite them. The number of names given in the schema should match the underlying data dimensions.

- **`schema_overrides`** (*dict*)
  default None Support type specification or override of one or more columns; note that any dtypes inferred from the schema param will be overridden. The number of entries in the schema should match the underlying data dimensions, unless a sequence of dictionaries is being passed, in which case a *partial* schema can be declared to prevent specific fields from being loaded.

- **`strict`** (*bool*)
  default True Throw an error if any `data` value does not exactly match the given or inferred data type for that column. If set to `False`, values that do not match the data type are cast to that data type or, if casting is not possible, set to null instead.

- **`orient`** (*{'col'*)
  'row'}, default None Whether to interpret two-dimensional data as columns or as rows. If None, the orientation is inferred by matching the columns and data dimensions. If this does not yield conclusive results, column orientation is used.

- **`infer_schema_length`** (*int or None The maximum number of rows to scan for schema inference. If set to `None`*)
  the full data may be scanned *(this can be slow)*. This parameter only applies if the input data is a sequence or generator of rows; other input is read as-is.

- **`nan_to_null`** (*bool*)
  default False If the data comes from one or more numpy arrays, can optionally convert input data np.nan values to null instead. This is a no-op for all other input data. Notes Initialising `LazyFrame(...)` directly is equivalent to `DataFrame(...).lazy()`. Examples Constructing a LazyFrame directly from a dictionary: ╞═════╪═════╡ Notice that the dtypes are automatically inferred as Polars Int64: [Int64, Int64] To specify a more detailed/specific frame schema you can supply the `schema` parameter with a dictionary of (name,dtype) pairs... ╞══════╪══════╡ ...a sequence of (name,dtype) pairs... ╞══════╪══════╡ ...or a list of typed Series. ...     pl.Series("col1", [1, 2], dtype=pl.Float32), ...     pl.Series("col2", [3, 4], dtype=pl.Int64), ... ] ╞══════╪══════╡ Constructing a LazyFrame from a numpy ndarray, specifying column names: ╞═════╪═════╡ Constructing a LazyFrame from a list of lists, row orientation specified: ╞═════╪═════╪═════╡

## Constructor

```python
def __init__(self, frame: polars.lazyframe.frame.LazyFrame = None, *args, **kwargs):
```

Initialize self.  See help(type(self)) for accurate signature.

## Methods

### `__repr__`

```python
def __repr__(self) -> 'str':
```

Return repr(self).

### `__str__`

```python
def __str__(self) -> 'str':
```

Return str(self).

### `approx_n_unique`

```python
def approx_n_unique(self) -> 'LazyFrame':
```

Approximate count of unique values.

.. deprecated:: 0.20.11
Use `select(pl.all().approx_n_unique())` instead.

This is done using the HyperLogLog++ algorithm for cardinality estimation.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "a": [1, 2, 3, 4],
...         "b": [1, 2, 1, 1],
...     }
... )

```
>>> lf.approx_n_unique().collect()  # doctest: +SKIP
shape: (1, 2)
┌─────┬─────┐
│ a   ┆ b   │
│ --- ┆ --- │
│ u32 ┆ u32 │
```

╞═════╪═════╡

```
│ 4   ┆ 2   │
└─────┴─────┘
```

### `bottom_k`

```python
def bottom_k(self, k: 'int', *, by: 'IntoExpr | Iterable[IntoExpr]', reverse: 'bool | Sequence[bool]' = False) -> 'LazyFrame':
```

Return the `k` smallest rows.

Non-null elements are always preferred over null elements, regardless of
the value of `reverse`. The output is not guaranteed to be in any
particular order, call :func:`sort` after this function if you wish the
output to be sorted.

### `cache`

```python
def cache(self) -> 'LazyFrame':
```

Cache the result once the execution of the physical plan hits this node.

It is not recommended using this as the optimizer likely can do a better job.

### `cast`

```python
def cast(self, dtypes: 'Mapping[ColumnNameOrSelector | PolarsDataType, PolarsDataType] | PolarsDataType', *, strict: 'bool' = True) -> 'LazyFrame':
```

Cast LazyFrame column(s) to the specified dtype(s).

### `clear`

```python
def clear(self, n: 'int' = 0) -> 'LazyFrame':
```

Create an empty copy of the current LazyFrame, with zero to 'n' rows.

Returns a copy with an identical schema but no data.

### Parameters

- **`clone`** (*Cheap deepcopy/clone. Examples ...     { ...         "a": [None*)
  2, 3, 4], ...         "b": [0.5, None, 2.5, 13], ...         "c": [True, True, False, None], ...     } ... ) ╞═════╪═════╪══════╡ ╞══════╪══════╪══════╡

### `clone`

```python
def clone(self) -> 'LazyFrame':
```

Create a copy of this LazyFrame.

This is a cheap operation that does not copy data.

See Also

```
--------
```

### Parameters

- **`clear`** (*Create an empty copy of the current LazyFrame*)
  with identical schema but no data. Examples ...     { ...         "a": [None, 2, 3, 4], ...         "b": [0.5, None, 2.5, 13], ...         "c": [True, True, False, None], ...     } ... ) <LazyFrame at ...>

### `collect`

```python
def collect(self, *, type_coercion: 'bool' = True, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, simplify_expression: 'bool' = True, slice_pushdown: 'bool' = True, comm_subplan_elim: 'bool' = True, comm_subexpr_elim: 'bool' = True, cluster_with_columns: 'bool' = True, collapse_joins: 'bool' = True, no_optimization: 'bool' = False, streaming: 'bool' = False, engine: 'EngineType' = 'cpu', background: 'bool' = False, _eager: 'bool' = False, **_kwargs: 'Any') -> 'DataFrame | InProcessQuery':
```

Materialize this LazyFrame into a DataFrame.

By default, all query optimizations are enabled. Individual optimizations may
be disabled by setting the corresponding parameter to `False`.

### Parameters

- **`Use`** (*func:`explain` to see if Polars can process the query in streaming mode. engine Select the engine used to process the query*)
  optional. If set to `"cpu"` (default), the query is run using the polars CPU engine. If set to `"gpu"`, the GPU engine is used. Fine-grained control over the GPU engine, for example which device to use on a system with multiple devices, is possible by providing a :class:`~.GPUEngine` object with configuration options. .. note:: GPU mode is considered **unstable**. Not all queries will run successfully on the GPU, however, they should fall back transparently to the default engine if execution is not supported. Running with `POLARS_VERBOSE=1` will provide information if a query falls back (and why). .. note:: The GPU engine does not support streaming, or running in the background. If either are enabled, then GPU execution is switched off. background Run the query in the background and get a handle to the query. This handle can be used to fetch the result or cancel the query. .. warning:: Background mode is considered **unstable**. It may be changed at any point without it being considered a breaking change.

- **`explain`** (*Print the query plan that is evaluated with collect.*)

- **`profile`** (*Collect the LazyFrame and time each node in the computation graph. polars.collect_all : Collect multiple LazyFrames at the same time. polars.Config.set_streaming_chunk_size : Set the size of streaming batches. Examples ...     { ...         "a": ["a"*)
  "b", "a", "b", "b", "c"], ...         "b": [1, 2, 3, 4, 5, 6], ...         "c": [6, 5, 4, 3, 2, 1], ...     } ... ) ╞═════╪═════╪═════╡ Collect in streaming mode ...     streaming=True ... )  # doctest: +SKIP ╞═════╪═════╪═════╡ Collect in GPU mode ╞═════╪═════╪═════╡ With control over the device used ...     engine=pl.GPUEngine(device=1) ... )  # doctest: +SKIP ╞═════╪═════╪═════╡

### `collect_async`

```python
def collect_async(self, *, gevent: 'bool' = False, type_coercion: 'bool' = True, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, simplify_expression: 'bool' = True, no_optimization: 'bool' = False, slice_pushdown: 'bool' = True, comm_subplan_elim: 'bool' = True, comm_subexpr_elim: 'bool' = True, cluster_with_columns: 'bool' = True, collapse_joins: 'bool' = True, streaming: 'bool' = False) -> 'Awaitable[DataFrame] | _GeventDataFrameResult[DataFrame]':
```

Collect DataFrame asynchronously in thread pool.

.. warning::
This functionality is considered **unstable**. It may be changed
at any point without it being considered a breaking change.

Collects into a DataFrame (like :func:`collect`) but, instead of returning
a DataFrame directly, it is scheduled to be collected inside a thread pool,
while this method returns almost instantly.

This can be useful if you use `gevent` or `asyncio` and want to release
control to other greenlets/tasks while LazyFrames are being collected.

### Parameters

- **`Use`** (*func:`explain` to see if Polars can process the query in streaming mode.*)

### `collect_schema`

```python
def collect_schema(self) -> 'Schema':
```

Resolve the schema of this LazyFrame.

Examples

```
--------
```

Determine the schema.


```
>>> lf = pl.LazyFrame(
```

...     {
...         "foo": [1, 2, 3],
...         "bar": [6.0, 7.0, 8.0],
...         "ham": ["a", "b", "c"],
...     }
... )

```
>>> lf.collect_schema()
```

Schema({'foo': Int64, 'bar': Float64, 'ham': String})

Access various properties of the schema.


```
>>> schema = lf.collect_schema()
>>> schema["bar"]
```

Float64

```
>>> schema.names()
```

['foo', 'bar', 'ham']

```
>>> schema.dtypes()
```

[Int64, Float64, String]

```
>>> schema.len()
```

3

### `count`

```python
def count(self) -> 'LazyFrame':
```

Return the number of non-null elements for each column.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {"a": [1, 2, 3, 4], "b": [1, 2, 1, None], "c": [None, None, None, None]}
... )

```
>>> lf.count().collect()
shape: (1, 3)
┌─────┬─────┬─────┐
│ a   ┆ b   ┆ c   │
│ --- ┆ --- ┆ --- │
│ u32 ┆ u32 ┆ u32 │
```

╞═════╪═════╪═════╡

```
│ 4   ┆ 3   ┆ 0   │
└─────┴─────┴─────┘
```

### `describe`

```python
def describe(self, percentiles: 'Sequence[float] | float | None' = (0.25, 0.5, 0.75), *, interpolation: 'RollingInterpolationMethod' = 'nearest') -> 'DataFrame':
```

Creates a summary of statistics for a LazyFrame, returning a DataFrame.

### Parameters

- **`interpolation`** (*{'nearest'*)
  'higher', 'lower', 'midpoint', 'linear'} Interpolation method used when calculating percentiles.

### `deserialize`

```python
def deserialize(source: 'str | Path | IOBase', *, format: 'SerializationFormat' = 'binary') -> 'LazyFrame':
```

Read a logical plan from a file to construct a LazyFrame.

### `drop`

```python
def drop(self, *columns: 'ColumnNameOrSelector | Iterable[ColumnNameOrSelector]', strict: 'bool' = True) -> 'LazyFrame':
```

Remove columns from the DataFrame.

### `drop_nulls`

```python
def drop_nulls(self, subset: 'ColumnNameOrSelector | Collection[ColumnNameOrSelector] | None' = None) -> 'LazyFrame':
```

Drop all rows that contain null values.

The original order of the remaining rows is preserved.

### `explain`

```python
def explain(self, *, format: 'ExplainFormat' = 'plain', optimized: 'bool' = True, type_coercion: 'bool' = True, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, simplify_expression: 'bool' = True, slice_pushdown: 'bool' = True, comm_subplan_elim: 'bool' = True, comm_subexpr_elim: 'bool' = True, cluster_with_columns: 'bool' = True, collapse_joins: 'bool' = True, streaming: 'bool' = False, tree_format: 'bool | None' = None) -> 'str':
```

Create a string representation of the query plan.

Different optimizations can be turned on or off.

### Parameters

- **`format`** (*{'plain'*)
  'tree'} The format to use for displaying the logical plan. optimized Return an optimized query plan. Defaults to `True`. If this is set to `True` the subsequent optimization flags control which optimizations run. type_coercion Do type coercion optimization. predicate_pushdown Do predicate pushdown optimization. projection_pushdown Do projection pushdown optimization. simplify_expression Run simplify expressions optimization. slice_pushdown Slice pushdown optimization. comm_subplan_elim Will try to cache branching subplans that occur on self-joins or unions. comm_subexpr_elim Common subexpressions will be cached and reused. cluster_with_columns Combine sequential independent calls to with_columns collapse_joins Collapse a join and filters into a faster join streaming Run parts of the query in a streaming fashion (this is in an alpha state) .. warning:: Streaming mode is considered **unstable**. It may be changed at any point without it being considered a breaking change. tree_format Format the output as a tree. .. deprecated:: 0.20.30 Use `format="tree"` instead. Examples ...     { ...         "a": ["a", "b", "a", "b", "b", "c"], ...         "b": [1, 2, 3, 4, 5, 6], ...         "c": [6, 5, 4, 3, 2, 1], ...     } ... ) ...     "a" ... ).explain()  # doctest: +SKIP

### `explode`

```python
def explode(self, columns: 'str | Expr | Sequence[str | Expr]', *more_columns: 'str | Expr') -> 'LazyFrame':
```

Explode the DataFrame to long format by exploding the given columns.

### `fetch`

```python
def fetch(self, n_rows: 'int' = 500, *, type_coercion: 'bool' = True, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, simplify_expression: 'bool' = True, no_optimization: 'bool' = False, slice_pushdown: 'bool' = True, comm_subplan_elim: 'bool' = True, comm_subexpr_elim: 'bool' = True, cluster_with_columns: 'bool' = True, collapse_joins: 'bool' = True, streaming: 'bool' = False) -> 'DataFrame':
```

Collect a small number of rows for debugging purposes.

.. deprecated:: 1.0

### Parameters

- **`Use`** (*meth:`collect` instead*)
  in conjunction with a call to :meth:`head`.` Notes This is similar to a :func:`collect` operation, but it overwrites the number of rows read by *every* scan operation. Be aware that `fetch` does not guarantee the final number of rows in the DataFrame. Filters, join operations and fewer rows being available in the scanned data will all influence the final number of rows (joins are especially susceptible to this, and may return no data at all if `n_rows` is too small as the join keys may not be present). Warnings This is strictly a utility function that can help to debug queries using a smaller number of rows, and should *not* be used in production code.

### `fill_nan`

```python
def fill_nan(self, value: 'int | float | Expr | None') -> 'LazyFrame':
```

Fill floating point NaN values.

### `fill_null`

```python
def fill_null(self, value: 'Any | Expr | None' = None, strategy: 'FillNullStrategy | None' = None, limit: 'int | None' = None, *, matches_supertype: 'bool' = True) -> 'LazyFrame':
```

Fill null values using the specified value or strategy.

### Parameters

- **`strategy`** (*{None*)
  'forward', 'backward', 'min', 'max', 'mean', 'zero', 'one'} Strategy used to fill null values. limit Number of consecutive null values to fill when using the 'forward' or 'backward' strategy. matches_supertype Fill all matching supertypes of the fill `value` literal. See Also fill_nan Examples ...     { ...         "a": [1, 2, None, 4], ...         "b": [0.5, 4, None, 13], ...     } ... ) ╞═════╪══════╡ ╞═════╪══════╡ ╞═════╪══════╡ ╞═════╪══════╡

### `filter`

```python
def filter(self, *predicates: 'IntoExprColumn | Iterable[IntoExprColumn] | bool | list[bool] | np.ndarray[Any, Any]', **constraints: 'Any') -> 'LazyFrame':
```

Filter the rows in the LazyFrame based on a predicate expression.

The original order of the remaining rows is preserved.

Rows where the filter does not evaluate to True are discarded, including nulls.

### `first`

```python
def first(self) -> 'LazyFrame':
```

Get the first row of the DataFrame.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "a": [1, 3, 5],
...         "b": [2, 4, 6],
...     }
... )

```
>>> lf.first().collect()
shape: (1, 2)
┌─────┬─────┐
│ a   ┆ b   │
│ --- ┆ --- │
│ i64 ┆ i64 │
```

╞═════╪═════╡

```
│ 1   ┆ 2   │
└─────┴─────┘
```

### `gather_every`

```python
def gather_every(self, n: 'int', offset: 'int' = 0) -> 'LazyFrame':
```

Take every nth row in the LazyFrame and return as a new LazyFrame.

### `group_by`

```python
def group_by(self, *by: 'IntoExpr | Iterable[IntoExpr]', maintain_order: 'bool' = False, **named_by: 'IntoExpr') -> 'LazyGroupBy':
```

Start a group by operation.

### `group_by_dynamic`

```python
def group_by_dynamic(self, index_column: 'IntoExpr', *, every: 'str | timedelta', period: 'str | timedelta | None' = None, offset: 'str | timedelta | None' = None, include_boundaries: 'bool' = False, closed: 'ClosedInterval' = 'left', label: 'Label' = 'left', group_by: 'IntoExpr | Iterable[IntoExpr] | None' = None, start_by: 'StartBy' = 'window') -> 'LazyGroupBy':
```

Group based on a time value (or index value of type Int32, Int64).

Time windows are calculated and rows are assigned to windows. Different from a
normal group by is that a row can be member of multiple groups.
By default, the windows look like:

- [start, start + period)
- [start + every, start + every + period)
- [start + 2*every, start + 2*every + period)
- ...

where `start` is determined by `start_by`, `offset`, `every`, and the earliest
datapoint. See the `start_by` argument description for details.

.. warning::
The index column must be sorted in ascending order. If `group_by` is passed, then
the index column must be sorted in ascending order within each group.

### Parameters

- **`closed`** (*{'left'*)
  'right', 'both', 'none'} Define which sides of the temporal interval are closed (inclusive).

- **`label`** (*{'left'*)
  'right', 'datapoint'} Define which label to use for the window: - 'left': lower boundary of the window - 'right': upper boundary of the window - 'datapoint': the first value of the index column in the given window. If you don't need the label to be at one of the boundaries, choose this option for maximum performance group_by Also group by this column/these columns

- **`start_by`** (*{'window'*)
  'datapoint', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'} The strategy to determine the start of the first window by. * 'window': Start by taking the earliest timestamp, truncating it with `every`, and then adding `offset`. Note that weekly windows start on Monday. * 'datapoint': Start from the first encountered data point. * a day of the week (only takes effect if `every` contains `'w'`): * 'monday': Start the window on the Monday before the first data point. * 'tuesday': Start the window on the Tuesday before the first data point. * ... * 'sunday': Start the window on the Sunday before the first data point. The resulting window is then shifted back until the earliest datapoint is in or in front of it.

- **`with`** (*func:`DataFrame.upsample`. 2) The `every`*)
  `period` and `offset` arguments are created with the following string language: - 1ns   (1 nanosecond) - 1us   (1 microsecond) - 1ms   (1 millisecond) - 1s    (1 second) - 1m    (1 minute) - 1h    (1 hour) - 1d    (1 calendar day) - 1w    (1 calendar week) - 1mo   (1 calendar month) - 1q    (1 calendar quarter) - 1y    (1 calendar year) - 1i    (1 index count) Or combine them: "3d12h4m25s" # 3 days, 12 hours, 4 minutes, and 25 seconds By "calendar day", we mean the corresponding time on the next day (which may not be 24 hours, due to daylight savings). Similarly for "calendar week", "calendar month", "calendar quarter", and "calendar year". In case of a group_by_dynamic on an integer column, the windows are defined by: - "1i"      # length 1 - "10i"     # length 10 Examples ...     { ...         "time": pl.datetime_range( ...             start=datetime(2021, 12, 16), ...             end=datetime(2021, 12, 16, 3), ...             interval="30m", ...             eager=True, ...         ), ...         "n": range(7), ...     } ... ) ╞═════════════════════╪═════╡ Group by windows of 1 hour. ...     pl.col("n") ... ).collect() ╞═════════════════════╪═══════════╡ The window boundaries can also be added to the aggregation result ...     "time", every="1h", include_boundaries=True, closed="right" ... ).agg(pl.col("n").mean()).collect() ╞═════════════════════╪═════════════════════╪═════════════════════╪═════╡ When closed="left", the window excludes the right end of interval: [lower_bound, upper_bound) ...     pl.col("n") ... ).collect() ╞═════════════════════╪═══════════╡ When closed="both" the time values at the window boundaries belong to 2 groups. ...     pl.col("n") ... ).collect() ╞═════════════════════╪═══════════╡ Dynamic group bys can also be combined with grouping on normal keys ╞═════════════════════╪═════╪════════╡ ...     "time", ...     every="1h", ...     closed="both", ...     group_by="groups", ...     include_boundaries=True, ... ).agg(pl.col("n")).collect() ╞════════╪═════════════════════╪═════════════════════╪═════════════════════╪═══════════╡ Dynamic group by on an index column ...     { ...         "idx": pl.int_range(0, 6, eager=True), ...         "A": ["A", "A", "B", "B", "B", "C"], ...     } ... ) ...     "idx", ...     every="2i", ...     period="3i", ...     include_boundaries=True, ...     closed="right", ... ).agg(pl.col("A").alias("A_agg_list")).collect() ╞═════════════════╪═════════════════╪═════╪═════════════════╡

### `head`

```python
def head(self, n: 'int' = 5) -> 'LazyFrame':
```

Get the first `n` rows.

### `inspect`

```python
def inspect(self, fmt: 'str' = '{}') -> 'LazyFrame':
```

Inspect a node in the computation graph.

Print the value that this node in the computation graph evaluates to and pass on
the value.

Examples

```
--------
>>> lf = pl.LazyFrame({"foo": [1, 1, -2, 3]})
>>> (
```

...     lf.with_columns(pl.col("foo").cum_sum().alias("bar"))
...     .inspect()  # print the node before the filter
...     .filter(pl.col("bar") == pl.col("foo"))
... )  # doctest: +ELLIPSIS
<LazyFrame at ...>

### `interpolate`

```python
def interpolate(self) -> 'LazyFrame':
```

Interpolate intermediate values. The interpolation method is linear.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "foo": [1, None, 9, 10],
...         "bar": [6, 7, 9, None],
...         "baz": [1, None, None, 9],
...     }
... )

```
>>> lf.interpolate().collect()
shape: (4, 3)
┌──────┬──────┬──────────┐
│ foo  ┆ bar  ┆ baz      │
│ ---  ┆ ---  ┆ ---      │
│ f64  ┆ f64  ┆ f64      │
```

╞══════╪══════╪══════════╡

```
│ 1.0  ┆ 6.0  ┆ 1.0      │
│ 5.0  ┆ 7.0  ┆ 3.666667 │
│ 9.0  ┆ 9.0  ┆ 6.333333 │
│ 10.0 ┆ null ┆ 9.0      │
└──────┴──────┴──────────┘
```

### `join`

```python
def join(self, other: 'LazyFrame', on: 'str | Expr | Sequence[str | Expr] | None' = None, how: 'JoinStrategy' = 'inner', *, left_on: 'str | Expr | Sequence[str | Expr] | None' = None, right_on: 'str | Expr | Sequence[str | Expr] | None' = None, suffix: 'str' = '_right', validate: 'JoinValidation' = 'm:m', join_nulls: 'bool' = False, coalesce: 'bool | None' = None, allow_parallel: 'bool' = True, force_parallel: 'bool' = False) -> 'LazyFrame':
```

Add a join operation to the Logical Plan.

### Parameters

- **`how`** (*{'inner'*)
  'left', 'right', 'full', 'semi', 'anti', 'cross'} Join strategy. * *inner* * *left* right table * *right* left table * *full* * *cross* * *semi* * *anti* .. note:: A left join preserves the row order of the left DataFrame. left_on Join column of the left DataFrame. right_on Join column of the right DataFrame. suffix Suffix to append to columns with a duplicate name.

- **`validate`** (*{'m:m'*)
  'm:1', '1:m', '1:1'} Checks if join is of specified type. * *many_to_many* “m:m”: default, does not result in checks * *one_to_one* “1:1”: check if join keys are unique in both left and right datasets * *one_to_many* “1:m”: check if join keys are unique in left dataset * *many_to_one* “m:1”: check if join keys are unique in right dataset .. note:: This is currently not supported by the streaming engine. join_nulls Join on null values. By default null values will never produce matches. coalesce Coalescing behavior (merging of join columns). - None: -> join specific. - True: -> Always coalesce join columns. - False: -> Never coalesce join columns. Note that joining on any other expressions than `col` will turn off coalescing. allow_parallel Allow the physical plan to optionally evaluate the computation of both DataFrames up to the join in parallel. force_parallel Force the physical plan to evaluate the computation of both DataFrames up to the join in parallel. See Also join_asof Examples ...     { ...         "foo": [1, 2, 3], ...         "bar": [6.0, 7.0, 8.0], ...         "ham": ["a", "b", "c"], ...     } ... ) ...     { ...         "apple": ["x", "y", "z"], ...         "ham": ["a", "b", "d"], ...     } ... ) ╞═════╪═════╪═════╪═══════╡ ╞══════╪══════╪══════╪═══════╪═══════════╡ ╞═════╪═════╪═════╪═══════╡ ╞═════╪═════╪═════╡ ╞═════╪═════╪═════╡

### `join_asof`

```python
def join_asof(self, other: 'LazyFrame', *, left_on: 'str | None | Expr' = None, right_on: 'str | None | Expr' = None, on: 'str | None | Expr' = None, by_left: 'str | Sequence[str] | None' = None, by_right: 'str | Sequence[str] | None' = None, by: 'str | Sequence[str] | None' = None, strategy: 'AsofJoinStrategy' = 'backward', suffix: 'str' = '_right', tolerance: 'str | int | float | timedelta | None' = None, allow_parallel: 'bool' = True, force_parallel: 'bool' = False, coalesce: 'bool' = True) -> 'LazyFrame':
```

Perform an asof join.

This is similar to a left-join except that we match on nearest key rather than
equal keys.

Both DataFrames must be sorted by the join_asof key.

For each row in the left DataFrame:

- A "backward" search selects the last row in the right DataFrame whose
'on' key is less than or equal to the left's key.

- A "forward" search selects the first row in the right DataFrame whose
'on' key is greater than or equal to the left's key.

A "nearest" search selects the last row in the right DataFrame whose value
is nearest to the left's key. String keys are not currently supported for a
nearest search.

The default is "backward".

### Parameters

- **`strategy`** (*{'backward'*)
  'forward', 'nearest'} Join strategy. suffix Suffix to append to columns with a duplicate name. tolerance Numeric tolerance. By setting this the join will only be done if the near keys are within this distance. If an asof join is done on columns of dtype "Date", "Datetime", "Duration" or "Time", use either a datetime.timedelta object or the following string language: - 1ns   (1 nanosecond) - 1us   (1 microsecond) - 1ms   (1 millisecond) - 1s    (1 second) - 1m    (1 minute) - 1h    (1 hour) - 1d    (1 calendar day) - 1w    (1 calendar week) - 1mo   (1 calendar month) - 1q    (1 calendar quarter) - 1y    (1 calendar year) Or combine them: "3d12h4m25s" # 3 days, 12 hours, 4 minutes, and 25 seconds By "calendar day", we mean the corresponding time on the next day (which may not be 24 hours, due to daylight savings). Similarly for "calendar week", "calendar month", "calendar quarter", and "calendar year". allow_parallel Allow the physical plan to optionally evaluate the computation of both DataFrames up to the join in parallel. force_parallel Force the physical plan to evaluate the computation of both DataFrames up to the join in parallel. coalesce Coalescing behavior (merging of `on` / `left_on` / `right_on` columns): - True: -> Always coalesce join columns. - False: -> Never coalesce join columns. Note that joining on any other expressions than `col` will turn off coalescing. Examples ...     { ...         "date": pl.date_range( ...             date(2016, 1, 1), ...             date(2020, 1, 1), ...             "1y", ...             eager=True, ...         ), ...         "gdp": [4164, 4411, 4566, 4696, 4827], ...     } ... ) ╞════════════╪══════╡ ...     { ...         "date": [date(2016, 3, 1), date(2018, 8, 1), date(2019, 1, 1)], ...         "population": [82.19, 82.66, 83.12], ...     } ... ).sort("date") ╞════════════╪════════════╡ Note how the dates don't quite match. If we join them using `join_asof` and `strategy='backward'`, then each date from `population` which doesn't have an exact match is matched with the closest earlier date from `gdp`: ╞════════════╪════════════╪══════╡ Note how: - date `2016-03-01` from `population` is matched with `2016-01-01` from `gdp`; - date `2018-08-01` from `population` is matched with `2018-01-01` from `gdp`. You can verify this by passing `coalesce=False`: ...     gdp, on="date", strategy="backward", coalesce=False ... ).collect() ╞════════════╪════════════╪════════════╪══════╡ If we instead use `strategy='forward'`, then each date from `population` which doesn't have an exact match is matched with the closest later date from `gdp`: ╞════════════╪════════════╪══════╡ Note how: - date `2016-03-01` from `population` is matched with `2017-01-01` from `gdp`; - date `2018-08-01` from `population` is matched with `2019-01-01` from `gdp`. Finally, `strategy='nearest'` gives us a mix of the two results above, as each date from `population` which doesn't have an exact match is matched with the closest date from `gdp`, regardless of whether it's earlier or later: ╞════════════╪════════════╪══════╡ Note how: - date `2016-03-01` from `population` is matched with `2016-01-01` from `gdp`; - date `2018-08-01` from `population` is matched with `2019-01-01` from `gdp`. They `by` argument allows joining on another column first, before the asof join. In this example we join by `country` first, then asof join by date, as above. ...     date(2016, 1, 1), date(2020, 1, 1), "1y", eager=True ... ) ...     { ...         "country": ["Germany"] * 5 + ["Netherlands"] * 5, ...         "date": pl.concat([gdp_dates, gdp_dates]), ...         "gdp": [4164, 4411, 4566, 4696, 4827, 784, 833, 914, 910, 909], ...     } ... ).sort("country", "date") ╞═════════════╪════════════╪══════╡ ...     { ...         "country": ["Germany"] * 3 + ["Netherlands"] * 3, ...         "date": [ ...             date(2016, 3, 1), ...             date(2018, 8, 1), ...             date(2019, 1, 1), ...             date(2016, 3, 1), ...             date(2018, 8, 1), ...             date(2019, 1, 1), ...         ], ...         "population": [82.19, 82.66, 83.12, 17.11, 17.32, 17.40], ...     } ... ).sort("country", "date") ╞═════════════╪════════════╪════════════╡ ╞═════════════╪════════════╪════════════╪══════╡

### `join_where`

```python
def join_where(self, other: 'LazyFrame', *predicates: 'Expr | Iterable[Expr]', suffix: 'str' = '_right') -> 'LazyFrame':
```

Perform a join based on one or multiple (in)equality predicates.

This performs an inner join, so only rows where all predicates are true
are included in the result, and a row from either DataFrame may be included
multiple times in the result.

.. note::
The row order of the input DataFrames is not preserved.

.. warning::
This functionality is experimental. It may be
changed at any point without it being considered a breaking change.

### `last`

```python
def last(self) -> 'LazyFrame':
```

Get the last row of the DataFrame.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "a": [1, 5, 3],
...         "b": [2, 4, 6],
...     }
... )

```
>>> lf.last().collect()
shape: (1, 2)
┌─────┬─────┐
│ a   ┆ b   │
│ --- ┆ --- │
│ i64 ┆ i64 │
```

╞═════╪═════╡

```
│ 3   ┆ 6   │
└─────┴─────┘
```

### `lazy`

```python
def lazy(self) -> 'LazyFrame':
```

Return lazy representation, i.e. itself.

Useful for writing code that expects either a :class:`DataFrame` or
:class:`LazyFrame`. On LazyFrame this is a no-op, and returns the same object.

### `limit`

```python
def limit(self, n: 'int' = 5) -> 'LazyFrame':
```

Get the first `n` rows.

Alias for :func:`LazyFrame.head`.

### `map_batches`

```python
def map_batches(self, function: 'Callable[[DataFrame], DataFrame]', *, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, slice_pushdown: 'bool' = True, no_optimizations: 'bool' = False, schema: 'None | SchemaDict' = None, validate_output_schema: 'bool' = True, streamable: 'bool' = False) -> 'LazyFrame':
```

Apply a custom function.

It is important that the function returns a Polars DataFrame.

### `max`

```python
def max(self) -> 'LazyFrame':
```

Aggregate the columns in the LazyFrame to their maximum value.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "a": [1, 2, 3, 4],
...         "b": [1, 2, 1, 1],
...     }
... )

```
>>> lf.max().collect()
shape: (1, 2)
┌─────┬─────┐
│ a   ┆ b   │
│ --- ┆ --- │
│ i64 ┆ i64 │
```

╞═════╪═════╡

```
│ 4   ┆ 2   │
└─────┴─────┘
```

### `mean`

```python
def mean(self) -> 'LazyFrame':
```

Aggregate the columns in the LazyFrame to their mean value.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "a": [1, 2, 3, 4],
...         "b": [1, 2, 1, 1],
...     }
... )

```
>>> lf.mean().collect()
shape: (1, 2)
┌─────┬──────┐
│ a   ┆ b    │
│ --- ┆ ---  │
│ f64 ┆ f64  │
```

╞═════╪══════╡

```
│ 2.5 ┆ 1.25 │
└─────┴──────┘
```

### `median`

```python
def median(self) -> 'LazyFrame':
```

Aggregate the columns in the LazyFrame to their median value.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "a": [1, 2, 3, 4],
...         "b": [1, 2, 1, 1],
...     }
... )

```
>>> lf.median().collect()
shape: (1, 2)
┌─────┬─────┐
│ a   ┆ b   │
│ --- ┆ --- │
│ f64 ┆ f64 │
```

╞═════╪═════╡

```
│ 2.5 ┆ 1.0 │
└─────┴─────┘
```

### `melt`

```python
def melt(self, id_vars: 'ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None' = None, value_vars: 'ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None' = None, variable_name: 'str | None' = None, value_name: 'str | None' = None, *, streamable: 'bool' = True) -> 'LazyFrame':
```

Unpivot a DataFrame from wide to long format.

Optionally leaves identifiers set.

This function is useful to massage a DataFrame into a format where one or more
columns are identifier variables (id_vars) while all other columns, considered
measured variables (value_vars), are "unpivoted" to the row axis leaving just
two non-identifier columns, 'variable' and 'value'.

.. deprecated:: 1.0.0
Please use :meth:`.unpivot` instead.

### `merge_sorted`

```python
def merge_sorted(self, other: 'LazyFrame', key: 'str') -> 'LazyFrame':
```

Take two sorted DataFrames and merge them by the sorted key.

The output of this operation will also be sorted.
It is the callers responsibility that the frames are sorted
by that key otherwise the output will not make sense.

The schemas of both LazyFrames must be equal.

### `min`

```python
def min(self) -> 'LazyFrame':
```

Aggregate the columns in the LazyFrame to their minimum value.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "a": [1, 2, 3, 4],
...         "b": [1, 2, 1, 1],
...     }
... )

```
>>> lf.min().collect()
shape: (1, 2)
┌─────┬─────┐
│ a   ┆ b   │
│ --- ┆ --- │
│ i64 ┆ i64 │
```

╞═════╪═════╡

```
│ 1   ┆ 1   │
└─────┴─────┘
```

### `null_count`

```python
def null_count(self) -> 'LazyFrame':
```

Aggregate the columns in the LazyFrame as the sum of their null value count.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "foo": [1, None, 3],
...         "bar": [6, 7, None],
...         "ham": ["a", "b", "c"],
...     }
... )

```
>>> lf.null_count().collect()
shape: (1, 3)
┌─────┬─────┬─────┐
│ foo ┆ bar ┆ ham │
│ --- ┆ --- ┆ --- │
│ u32 ┆ u32 ┆ u32 │
```

╞═════╪═════╪═════╡

```
│ 1   ┆ 1   ┆ 0   │
└─────┴─────┴─────┘
```

### `pipe`

```python
def pipe(self, function: 'Callable[Concatenate[LazyFrame, P], T]', *args: 'P.args', **kwargs: 'P.kwargs') -> 'T':
```

Offers a structured way to apply a sequence of user-defined functions (UDFs).

### `profile`

```python
def profile(self, *, type_coercion: 'bool' = True, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, simplify_expression: 'bool' = True, no_optimization: 'bool' = False, slice_pushdown: 'bool' = True, comm_subplan_elim: 'bool' = True, comm_subexpr_elim: 'bool' = True, cluster_with_columns: 'bool' = True, collapse_joins: 'bool' = True, show_plot: 'bool' = False, truncate_nodes: 'int' = 0, figsize: 'tuple[int, int]' = (18, 8), streaming: 'bool' = False) -> 'tuple[DataFrame, DataFrame]':
```

Profile a LazyFrame.

This will run the query and return a tuple
containing the materialized DataFrame and a DataFrame that
contains profiling information of each node that is executed.

The units of the timings are microseconds.

### `quantile`

```python
def quantile(self, quantile: 'float | Expr', interpolation: 'RollingInterpolationMethod' = 'nearest') -> 'LazyFrame':
```

Aggregate the columns in the LazyFrame to their quantile value.

### Parameters

- **`interpolation`** (*{'nearest'*)
  'higher', 'lower', 'midpoint', 'linear'} Interpolation method. Examples ...     { ...         "a": [1, 2, 3, 4], ...         "b": [1, 2, 1, 1], ...     } ... ) ╞═════╪═════╡

### `rename`

```python
def rename(self, mapping: 'dict[str, str] | Callable[[str], str]', *, strict: 'bool' = True) -> 'LazyFrame':
```

Rename column names.

### `reverse`

```python
def reverse(self) -> 'LazyFrame':
```

Reverse the DataFrame.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "key": ["a", "b", "c"],
...         "val": [1, 2, 3],
...     }
... )

```
>>> lf.reverse().collect()
shape: (3, 2)
┌─────┬─────┐
│ key ┆ val │
│ --- ┆ --- │
│ str ┆ i64 │
```

╞═════╪═════╡

```
│ c   ┆ 3   │
│ b   ┆ 2   │
│ a   ┆ 1   │
└─────┴─────┘
```

### `rolling`

```python
def rolling(self, index_column: 'IntoExpr', *, period: 'str | timedelta', offset: 'str | timedelta | None' = None, closed: 'ClosedInterval' = 'right', group_by: 'IntoExpr | Iterable[IntoExpr] | None' = None) -> 'LazyGroupBy':
```

Create rolling groups based on a temporal or integer column.

Different from a `group_by_dynamic` the windows are now determined by the
individual values and are not of constant intervals. For constant intervals

### Parameters

- **`use`** (*func:`LazyFrame.group_by_dynamic`. If you have a time series `<t_0*)
  t_1, ..., t_n>`, then by default the windows created will be * (t_0 - period, t_0] * (t_1 - period, t_1] * ... * (t_n - period, t_n] whereas if you pass a non-default `offset`, then the windows will be * (t_0 + offset, t_0 + offset + period] * (t_1 + offset, t_1 + offset + period] * ... * (t_n + offset, t_n + offset + period] The `period` and `offset` arguments are created either from a timedelta, or by using the following string language: - 1ns   (1 nanosecond) - 1us   (1 microsecond) - 1ms   (1 millisecond) - 1s    (1 second) - 1m    (1 minute) - 1h    (1 hour) - 1d    (1 calendar day) - 1w    (1 calendar week) - 1mo   (1 calendar month) - 1q    (1 calendar quarter) - 1y    (1 calendar year) - 1i    (1 index count) Or combine them: "3d12h4m25s" # 3 days, 12 hours, 4 minutes, and 25 seconds By "calendar day", we mean the corresponding time on the next day (which may not be 24 hours, due to daylight savings). Similarly for "calendar week", "calendar month", "calendar quarter", and "calendar year".

- **`closed`** (*{'right'*)
  'left', 'both', 'none'} Define which sides of the temporal interval are closed (inclusive). group_by Also group by this column/these columns

### `select`

```python
def select(self, *exprs: 'IntoExpr | Iterable[IntoExpr]', **named_exprs: 'IntoExpr') -> 'LazyFrame':
```

Select columns from this LazyFrame.

### `select_seq`

```python
def select_seq(self, *exprs: 'IntoExpr | Iterable[IntoExpr]', **named_exprs: 'IntoExpr') -> 'LazyFrame':
```

Select columns from this LazyFrame.

This will run all expression sequentially instead of in parallel.
Use this when the work per expression is cheap.

### `serialize`

```python
def serialize(self, file: 'IOBase | str | Path | None' = None, *, format: 'SerializationFormat' = 'binary') -> 'bytes | str | None':
```

Serialize the logical plan of this LazyFrame to a file or string in JSON format.

### `set_sorted`

```python
def set_sorted(self, column: 'str', *, descending: 'bool' = False) -> 'LazyFrame':
```

Indicate that one or multiple columns are sorted.

This can speed up future operations.

### `shift`

```python
def shift(self, n: 'int | IntoExprColumn' = 1, *, fill_value: 'IntoExpr | None' = None) -> 'LazyFrame':
```

Shift values by the given number of indices.

### `show_graph`

```python
def show_graph(self, *, optimized: 'bool' = True, show: 'bool' = True, output_path: 'str | Path | None' = None, raw_output: 'bool' = False, figsize: 'tuple[float, float]' = (16.0, 12.0), type_coercion: 'bool' = True, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, simplify_expression: 'bool' = True, slice_pushdown: 'bool' = True, comm_subplan_elim: 'bool' = True, comm_subexpr_elim: 'bool' = True, cluster_with_columns: 'bool' = True, collapse_joins: 'bool' = True, streaming: 'bool' = False) -> 'str | None':
```

Show a plot of the query plan.

Note that graphviz must be installed to render the visualization (if not
already present you can download it here: <https://graphviz.org/download>`_).

### `sink_csv`

```python
def sink_csv(self, path: 'str | Path', *, include_bom: 'bool' = False, include_header: 'bool' = True, separator: 'str' = ',', line_terminator: 'str' = '\n', quote_char: 'str' = '"', batch_size: 'int' = 1024, datetime_format: 'str | None' = None, date_format: 'str | None' = None, time_format: 'str | None' = None, float_scientific: 'bool | None' = None, float_precision: 'int | None' = None, null_value: 'str | None' = None, quote_style: 'CsvQuoteStyle | None' = None, maintain_order: 'bool' = True, type_coercion: 'bool' = True, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, simplify_expression: 'bool' = True, slice_pushdown: 'bool' = True, collapse_joins: 'bool' = True, no_optimization: 'bool' = False) -> 'None':
```

Evaluate the query in streaming mode and write to a CSV file.

.. warning::
Streaming mode is considered **unstable**. It may be changed
at any point without it being considered a breaking change.

This allows streaming results that are larger than RAM to be written to disk.

### Parameters

- **`quote_style`** (*{'necessary'*)
  'always', 'non_numeric', 'never'} Determines the quoting strategy used. - necessary (default): This puts quotes around fields only when necessary. They are necessary when fields contain a quote, delimiter or record terminator. Quotes are also necessary when writing an empty record (which is indistinguishable from a record with one empty field). This is the default. - always: This puts quotes around every field. Always. - never: This never puts quotes around fields, even if that results in invalid CSV data (e.g.: by not quoting strings containing the separator). - non_numeric: This puts quotes around all fields that are non-numeric. Namely, when writing a field that does not parse as a valid float or integer, then quotes will be used even if they aren`t strictly necessary. maintain_order Maintain the order in which data is processed. Setting this to `False` will be slightly faster. type_coercion Do type coercion optimization. predicate_pushdown Do predicate pushdown optimization. projection_pushdown Do projection pushdown optimization. simplify_expression Run simplify expressions optimization. slice_pushdown Slice pushdown optimization. collapse_joins Collapse a join and filters into a faster join no_optimization Turn off (certain) optimizations.

### `sink_ipc`

```python
def sink_ipc(self, path: 'str | Path', *, compression: 'str | None' = 'zstd', maintain_order: 'bool' = True, type_coercion: 'bool' = True, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, simplify_expression: 'bool' = True, slice_pushdown: 'bool' = True, collapse_joins: 'bool' = True, no_optimization: 'bool' = False) -> 'None':
```

Evaluate the query in streaming mode and write to an IPC file.

.. warning::
Streaming mode is considered **unstable**. It may be changed
at any point without it being considered a breaking change.

This allows streaming results that are larger than RAM to be written to disk.

### Parameters

- **`compression`** (*{'lz4'*)
  'zstd'} Choose "zstd" for good compression performance. Choose "lz4" for fast compression/decompression. maintain_order Maintain the order in which data is processed. Setting this to `False` will be slightly faster. type_coercion Do type coercion optimization. predicate_pushdown Do predicate pushdown optimization. projection_pushdown Do projection pushdown optimization. simplify_expression Run simplify expressions optimization. slice_pushdown Slice pushdown optimization. collapse_joins Collapse a join and filters into a faster join no_optimization Turn off (certain) optimizations.

### `sink_ndjson`

```python
def sink_ndjson(self, path: 'str | Path', *, maintain_order: 'bool' = True, type_coercion: 'bool' = True, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, simplify_expression: 'bool' = True, slice_pushdown: 'bool' = True, collapse_joins: 'bool' = True, no_optimization: 'bool' = False) -> 'None':
```

Evaluate the query in streaming mode and write to an NDJSON file.

.. warning::
Streaming mode is considered **unstable**. It may be changed
at any point without it being considered a breaking change.

This allows streaming results that are larger than RAM to be written to disk.

### `sink_parquet`

```python
def sink_parquet(self, path: 'str | Path', *, compression: 'str' = 'zstd', compression_level: 'int | None' = None, statistics: 'bool | str | dict[str, bool]' = True, row_group_size: 'int | None' = None, data_page_size: 'int | None' = None, maintain_order: 'bool' = True, type_coercion: 'bool' = True, predicate_pushdown: 'bool' = True, projection_pushdown: 'bool' = True, simplify_expression: 'bool' = True, slice_pushdown: 'bool' = True, collapse_joins: 'bool' = True, no_optimization: 'bool' = False) -> 'None':
```

Evaluate the query in streaming mode and write to a Parquet file.

.. warning::
Streaming mode is considered **unstable**. It may be changed
at any point without it being considered a breaking change.

This allows streaming results that are larger than RAM to be written to disk.

### Parameters

- **`compression`** (*{'lz4'*)
  'uncompressed', 'snappy', 'gzip', 'lzo', 'brotli', 'zstd'} Choose "zstd" for good compression performance. Choose "lz4" for fast compression/decompression. Choose "snappy" for more backwards compatibility guarantees when you deal with older parquet readers. compression_level The level of compression to use. Higher compression means smaller files on disk. - "gzip" : min-level: 0, max-level: 10. - "brotli" : min-level: 0, max-level: 11. - "zstd" : min-level: 1, max-level: 22. statistics Write statistics to the parquet headers. This is the default behavior. Possible values: - `True`: enable default set of statistics (default) - `False`: disable all statistics - "full": calculate and write all available statistics. Cannot be combined with `use_pyarrow`. - `{ "statistic-key": True / False, ... }`. Cannot be combined with `use_pyarrow`. Available keys: - "min": column minimum value (default: `True`) - "max": column maximum value (default: `True`) - "distinct_count": number of unique column values (default: `False`) - "null_count": number of null values in column (default: `True`) row_group_size Size of the row groups in number of rows. If None (default), the chunks of the `DataFrame` are used. Writing in smaller chunks may reduce memory pressure and improve writing speeds. data_page_size Size limit of individual data pages. If not set defaults to 1024 * 1024 bytes maintain_order Maintain the order in which data is processed. Setting this to `False` will be slightly faster. type_coercion Do type coercion optimization. predicate_pushdown Do predicate pushdown optimization. projection_pushdown Do projection pushdown optimization. simplify_expression Run simplify expressions optimization. slice_pushdown Slice pushdown optimization. collapse_joins Collapse a join and filters into a faster join no_optimization Turn off (certain) optimizations.

### `slice`

```python
def slice(self, offset: 'int', length: 'int | None' = None) -> 'LazyFrame':
```

Get a slice of this DataFrame.

### `sort`

```python
def sort(self, by: 'IntoExpr | Iterable[IntoExpr]', *more_by: 'IntoExpr', descending: 'bool | Sequence[bool]' = False, nulls_last: 'bool | Sequence[bool]' = False, maintain_order: 'bool' = False, multithreaded: 'bool' = True) -> 'LazyFrame':
```

Sort the LazyFrame by the given columns.

### `sql`

```python
def sql(self, query: 'str', *, table_name: 'str' = 'self') -> 'LazyFrame':
```

Execute a SQL query against the LazyFrame.

.. versionadded:: 0.20.23

.. warning::
This functionality is considered **unstable**, although it is close to
being considered stable. It may be changed at any point without it being
considered a breaking change.

### `std`

```python
def std(self, ddof: 'int' = 1) -> 'LazyFrame':
```

Aggregate the columns in the LazyFrame to their standard deviation value.

### `sum`

```python
def sum(self) -> 'LazyFrame':
```

Aggregate the columns in the LazyFrame to their sum value.

Examples

```
--------
>>> lf = pl.LazyFrame(
```

...     {
...         "a": [1, 2, 3, 4],
...         "b": [1, 2, 1, 1],
...     }
... )

```
>>> lf.sum().collect()
shape: (1, 2)
┌─────┬─────┐
│ a   ┆ b   │
│ --- ┆ --- │
│ i64 ┆ i64 │
```

╞═════╪═════╡

```
│ 10  ┆ 5   │
└─────┴─────┘
```

### `tail`

```python
def tail(self, n: 'int' = 5) -> 'LazyFrame':
```

Get the last `n` rows.

### `top_k`

```python
def top_k(self, k: 'int', *, by: 'IntoExpr | Iterable[IntoExpr]', reverse: 'bool | Sequence[bool]' = False) -> 'LazyFrame':
```

Return the `k` largest rows.

Non-null elements are always preferred over null elements, regardless of
the value of `reverse`. The output is not guaranteed to be in any
particular order, call :func:`sort` after this function if you wish the
output to be sorted.

### `unique`

```python
def unique(self, subset: 'ColumnNameOrSelector | Collection[ColumnNameOrSelector] | None' = None, *, keep: 'UniqueKeepStrategy' = 'any', maintain_order: 'bool' = False) -> 'LazyFrame':
```

Drop duplicate rows from this DataFrame.

### Parameters

- **`keep`** (*{'first'*)
  'last', 'any', 'none'} Which of the duplicate rows to keep. * 'any': Does not give any guarantee of which row is kept. This allows more optimizations. * 'none': Don't keep duplicate rows. * 'first': Keep first unique row. * 'last': Keep last unique row. maintain_order Keep the same order as the original DataFrame. This is more expensive to compute. Settings this to `True` blocks the possibility to run on the streaming engine.

### `unnest`

```python
def unnest(self, columns: 'ColumnNameOrSelector | Collection[ColumnNameOrSelector]', *more_columns: 'ColumnNameOrSelector') -> 'LazyFrame':
```

Decompose struct columns into separate columns for each of their fields.

The new columns will be inserted into the DataFrame at the location of the
struct column.

### `unpivot`

```python
def unpivot(self, on: 'ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None' = None, *, index: 'ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None' = None, variable_name: 'str | None' = None, value_name: 'str | None' = None, streamable: 'bool' = True) -> 'LazyFrame':
```

Unpivot a DataFrame from wide to long format.

Optionally leaves identifiers set.

This function is useful to massage a DataFrame into a format where one or more
columns are identifier variables (index) while all other columns, considered
measured variables (on), are "unpivoted" to the row axis leaving just
two non-identifier columns, 'variable' and 'value'.

### `update`

```python
def update(self, other: 'LazyFrame', on: 'str | Sequence[str] | None' = None, how: "Literal['left', 'inner', 'full']" = 'left', *, left_on: 'str | Sequence[str] | None' = None, right_on: 'str | Sequence[str] | None' = None, include_nulls: 'bool' = False) -> 'LazyFrame':
```

Update the values in this `LazyFrame` with the values in `other`.

.. warning::
This functionality is considered **unstable**. It may be changed
at any point without it being considered a breaking change.

### Parameters

- **`how`** (*{'left'*)
  'inner', 'full'} * 'left' will keep all rows from the left table; rows may be duplicated if multiple rows in the right frame match the left row's key. * 'inner' keeps only those rows where the key exists in both frames. * 'full' will update existing rows where the key matches while also adding any new rows contained in the given frame. left_on Join column(s) of the left DataFrame. right_on Join column(s) of the right DataFrame. include_nulls Overwrite values in the left frame with null values from the right frame. If set to `False` (default), null values in the right frame are ignored. Notes This is syntactic sugar for a left/inner join, with an optional coalesce when `include_nulls = False`. Examples ...     { ...         "A": [1, 2, 3, 4], ...         "B": [400, 500, 600, 700], ...     } ... ) ╞═════╪═════╡ ...     { ...         "B": [-66, None, -99], ...         "C": [5, 3, 1], ...     } ... ) Update `df` values with the non-null values in `new_df`, by row index: ╞═════╪═════╡ Update `df` values with the non-null values in `new_df`, by row index, but only keeping those rows that are common to both frames: ╞═════╪═════╡ Update `df` values with the non-null values in `new_df`, using a full outer join strategy that defines explicit join columns in each frame: ╞═════╪═════╡ Update `df` values including null values in `new_df`, using a full outer join strategy that defines explicit join columns in each frame: ...     new_lf, left_on="A", right_on="C", how="full", include_nulls=True ... ).collect() ╞═════╪══════╡

### `var`

```python
def var(self, ddof: 'int' = 1) -> 'LazyFrame':
```

Aggregate the columns in the LazyFrame to their variance value.

### `with_columns`

```python
def with_columns(self, *exprs: 'IntoExpr | Iterable[IntoExpr]', **named_exprs: 'IntoExpr') -> 'LazyFrame':
```

Add columns to this LazyFrame.

Added columns will replace existing columns with the same name.

### `with_columns_seq`

```python
def with_columns_seq(self, *exprs: 'IntoExpr | Iterable[IntoExpr]', **named_exprs: 'IntoExpr') -> 'LazyFrame':
```

Add columns to this LazyFrame.

Added columns will replace existing columns with the same name.

This will run all expression sequentially instead of in parallel.
Use this when the work per expression is cheap.

### `with_context`

```python
def with_context(self, other: 'Self | list[Self]') -> 'LazyFrame':
```

Add an external context to the computation graph.

.. deprecated:: 1.0.0

### Parameters

- **`Use`** (*func:`concat` instead with `how='horizontal'` This allows expressions to also access columns from DataFrames that are not part of this one.*)

### `with_row_count`

```python
def with_row_count(self, name: 'str' = 'row_nr', offset: 'int' = 0) -> 'LazyFrame':
```

Add a column at index 0 that counts the rows.

.. deprecated:: 0.20.4

### Parameters

- **`Use`** (*meth:`with_row_index` instead. Note that the default column name has changed from 'row_nr' to 'index'.*)

### `with_row_index`

```python
def with_row_index(self, name: 'str' = 'index', offset: 'int' = 0) -> 'LazyFrame':
```

Add a row index as the first column in the LazyFrame.

### Parameters

- **`and`** (*func:`len`. ...     pl.int_range(pl.len()*)
  dtype=pl.UInt32).alias("index"), ...     pl.all(), ... ).collect() ╞═══════╪═════╪═════╡
