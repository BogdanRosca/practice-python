# Assignment 012: Closures & a production-grade `memoize` (~15 min)

Create `solution.py` in this folder, push it to this branch, and merge the PR. Type-hint everything (`Callable`, `ParamSpec`/`TypeVar` if you want a challenge). No `functools.lru_cache`/`cache` today, because you're building it.

**Part 1: closures (~3 min)**
1. `make_accumulator(start: float = 0) -> tuple[Callable[[float], float], Callable[[], None]]` returns `(add, reset)`. The two functions **share** one running total: `add(5)` → 5, `add(2)` → 7, `reset()`, `add(1)` → 1. Use `nonlocal`, not a list/dict hack.
2. This snippet prints `[6, 6, 6]`. Fix it in **two** different ways (default argument, `functools.partial`), and explain in one comment *why* it happens:
   ```python
   adders = [lambda x: x + n for n in (1, 2, 3)]
   print([f(3) for f in adders])   # want [4, 5, 6]
   ```

**Part 2: `memoize` (~8 min)**
Write `memoize` usable as **both** `@memoize` and `@memoize(maxsize=2)`:
1. The cache key includes positional **and** keyword arguments, so `f(1, b=2)` is cached, and the order of the kwargs shouldn't matter (`f(a=1, b=2)` and `f(b=2, a=1)` hit the same entry).
2. `maxsize=None` means unbounded. Otherwise evict the **least recently used** entry when full (hint: `collections.OrderedDict` with `move_to_end` / `popitem(last=False)`).
3. Expose `wrapper.cache_info()` returning `(hits, misses, currsize)` as a `NamedTuple`, and `wrapper.cache_clear()` which resets the cache *and* the counters.
4. Use `functools.wraps`, and show that `inspect.signature(fib)` still shows the real parameters.
5. Demo: a memoized recursive `fib(80)` that returns instantly, then an LRU demo with `maxsize=2` where `cache_info()` proves an eviction happened.

**Part 3: class-based decorator on methods (~4 min)**
1. `class RateLimit`: `@RateLimit(calls=3)` allows a function to be called at most 3 times and then raises a custom `RateLimitExceeded(Exception)` (Day 008 style: include the function name in the message).
2. It must work on **methods** (implement `__get__`), and the limit applies **per instance**: `a.ping()` ×3 then `b.ping()` still works. Hint: keep a `weakref.WeakKeyDictionary[obj, int]`, or think about why a plain dict would leak.

**Bonus:** print `add.__closure__` from Part 1 and show that `add` and `reset` share the **same cell object** (`is`). Then stack `@timed` (write a 5-line one) above and below `@memoize` on `fib`, and explain the difference in a comment.

End with an `if __name__ == "__main__":` demo for every part (errors via `try/except`).
