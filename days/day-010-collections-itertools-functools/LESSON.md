# Day 010: `collections`, `itertools` & `functools` (~5 min)

For nine days you built containers, iterators and decorators by hand. The standard library already ships well-tested versions of most of them. Knowing these three modules means less custom code and fewer bugs.

## 1. `collections`: specialised containers
```python
from collections import Counter, defaultdict, deque, namedtuple, ChainMap

Counter("mississippi").most_common(2)        # [('i', 4), ('s', 4)]
Counter(a=3, b=1) - Counter(a=1, b=5)        # Counter({'a': 2}); counts <= 0 are dropped

by_currency: defaultdict[str, list[int]] = defaultdict(list)
for amount, cur in [(10, "USD"), (5, "EUR"), (7, "USD")]:
    by_currency[cur].append(amount)          # no "if key not in d" dance

last3 = deque(maxlen=3)                      # O(1) appends/pops at both ends
for x in range(5): last3.append(x)           # deque([2, 3, 4], maxlen=3)

defaults = {"currency": "EUR", "rounding": 2}
cfg = ChainMap({"currency": "USD"}, defaults)   # lookups go through layers
cfg["currency"], cfg["rounding"]                # ('USD', 2)
```
- `defaultdict(list)` takes a **factory** (`list`), not a value (`[]`).
- Reading a missing key on a `defaultdict` **inserts** it. Use `key in d` for a check that has no side effects.
- `list.pop(0)` is O(n). Use `deque.popleft()` for queues.

## 2. `itertools`: lazy building blocks (they pair well with Day 005)
```python
from itertools import groupby, islice, chain, accumulate, pairwise, batched, count

list(accumulate([10, -3, 5]))                # [10, 7, 12], running balance
list(pairwise([1, 4, 9]))                    # [(1, 4), (4, 9)]  (3.10+)
list(batched(range(7), 3))                   # [(0,1,2), (3,4,5), (6,)]  (3.12+)
list(islice(count(100, 10), 3))              # [100, 110, 120], slicing an infinite iterator
list(chain.from_iterable([[1], [2, 3]]))     # [1, 2, 3], flattens one level

rows = sorted([("USD", 10), ("EUR", 5), ("USD", 7)])
{k: [v for _, v in g] for k, g in groupby(rows, key=lambda r: r[0])}
# {'EUR': [5], 'USD': [7, 10]}
```
- **Pitfall #1:** `groupby` only groups **consecutive** equal keys. Sort by the same key first, or use `defaultdict`.
- **Pitfall #2:** iterators are single-use. Each `g` from `groupby` is invalid once you move to the next group, so consume it right away.

## 3. `functools`: tools for working with functions
```python
from functools import cache, lru_cache, partial, reduce, singledispatch, total_ordering, cached_property
import operator

@cache                                        # = lru_cache(maxsize=None)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)
fib(80); fib.cache_info()                     # hits/misses for free

reduce(operator.mul, [1, 2, 3, 4], 1)         # 24; always pass an initial value
to_usd = partial(round, ndigits=2)            # fix some arguments now, pass the rest later

@singledispatch
def fmt(x) -> str: return str(x)
@fmt.register
def _(x: float) -> str: return f"{x:.2f}"     # dispatches on the type of the first argument
fmt(3.14159), fmt(7)                          # ('3.14', '7')
```
- `@cache` arguments must be **hashable**, and the cache keeps them alive forever. If you put it on a method, `self` is cached too, which leaks instances. Use `cached_property` for per-instance values, or `lru_cache(maxsize=...)` for a bounded cache.
- `@total_ordering`: define `__eq__` and one of `__lt__`/`__le__`/`__gt__`/`__ge__`, and it fills in the rest (this would have shortened Day 004).
- Inside your own decorators, use `functools.wraps` (Day 007) so that `__name__` and `__doc__` survive.

## When to reach for which
| Need | Use |
|------|-----|
| Count things / top-N | `Counter` |
| Group into buckets (unsorted input) | `defaultdict(list)` |
| Group runs of a sorted/streamed input | `itertools.groupby` |
| Sliding window, queue, "last N" | `deque(maxlen=N)` |
| Running totals | `itertools.accumulate` |
| Expensive pure function called repeatedly | `functools.cache` / `lru_cache` |
| Same function, different behaviour per type | `functools.singledispatch` |
