# Day 007: Context Managers & Decorators (~5 min)

Both are about **wrapping** code: a context manager wraps a *block* (setup → body → guaranteed teardown), a decorator wraps a *function* (before → call → after). Day 002's descriptors and Day 005's generators are the building blocks for both.

## 1. The context manager protocol
`with cm as x:` calls `x = cm.__enter__()`, runs the body, then **always** calls `cm.__exit__(exc_type, exc, tb)`, even on exceptions or `return`.
```python
import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self                      # what `as` binds to
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        return False                     # falsy -> exception (if any) propagates

with Timer() as t:
    sum(range(1_000_000))
print(f"{t.elapsed:.3f}s")
```
`__exit__` returning **True suppresses** the exception. Do that deliberately or never.

## 2. `@contextmanager`: a generator does the same job
```python
from contextlib import contextmanager

@contextmanager
def transaction(wallet):
    snapshot = list(wallet.items)        # setup
    try:
        yield wallet                     # body of the `with` runs here
    except Exception:
        wallet.items[:] = snapshot       # rollback
        raise                            # re-raise, don't swallow
```
Code before `yield` = `__enter__`, after = `__exit__`. The body's exception is **re-raised at the `yield`**, so without `try/finally` (or `except`) your teardown is skipped. Also handy: `contextlib.suppress(KeyError)`, `ExitStack` (dynamic number of CMs), `redirect_stdout`.

## 3. Decorators are just functions taking functions
```python
import functools

def logged(func):
    @functools.wraps(func)               # keep __name__, __doc__, __wrapped__
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}{args} -> {result!r}")
        return result
    return wrapper

@logged                                  # same as: add = logged(add)
def add(a, b): return a + b
```
**With arguments** you need one more level: the outer call returns the real decorator.
```python
def retry(times: int, on: type[Exception] = Exception):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except on:
                    if attempt == times:
                        raise
        return wrapper
    return decorator

@retry(times=3, on=ConnectionError)      # retry(...) runs first, returns decorator
def fetch(): ...
```
State lives in the closure (or as an attribute on `wrapper`, e.g. `wrapper.calls = 0`).

## Pitfalls
- Forgetting `@functools.wraps`: every decorated function is called `wrapper` in tracebacks, logs and pytest output.
- `@retry` without parentheses when the decorator expects arguments: `fetch` becomes `decorator`, and the bug only shows up at call time.
- `@contextmanager` without `try/finally`: cleanup never runs when the body raises.
- Catching too broadly in `__exit__` / `except Exception: pass` hides real bugs. Suppress specific types only.
- Decorating methods: `wrapper(*args)` receives `self` as `args[0]`. That's fine, just don't assume `args[0]` is your data.
- Decorators run **at import time** (definition), the wrapper at **call time**. Expensive setup belongs in the decorator, not the wrapper.
