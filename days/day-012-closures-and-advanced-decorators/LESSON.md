# Day 012: Closures & advanced decorators (~5 min)

Day 007 showed the *shape* of a decorator. Today is about the machinery underneath: **closures**, meaning functions that remember variables from the scope they were defined in. With that you can write decorators that carry state, accept optional arguments and still work on methods.

## 1. A closure captures *variables*, not values
```python
def make_multiplier(k):
    def mul(x):
        return x * k        # `k` is a free variable, stored in a "cell"
    return mul

triple = make_multiplier(3)
triple(5)                                   # 15
triple.__code__.co_freevars                 # ('k',)
triple.__closure__[0].cell_contents         # 3
```
The cell holds a **reference to the variable**, not a snapshot of its value. That is why the classic **late-binding bug** happens:
```python
fns = [lambda x: x * i for i in range(3)]
[f(10) for f in fns]                        # [20, 20, 20]  every lambda sees the final i

fns = [lambda x, i=i: x * i for i in range(3)]          # fix 1: default arg binds now
fns = [functools.partial(operator.mul, i) for i in range(3)]   # fix 2: partial
[f(10) for f in fns]                        # [0, 10, 20]
```

## 2. `nonlocal`: rebinding a captured variable
Reading a captured name is free. **Assigning** to it makes it local, unless you declare `nonlocal`:
```python
def make_counter():
    count = 0
    def incr():
        nonlocal count      # without this: UnboundLocalError on `count += 1`
        count += 1
        return count
    return incr
```
Mutating a captured object (`cache[key] = v`, `items.append(x)`) needs no `nonlocal`, because you are not rebinding the name.

## 3. Decorators with *optional* arguments
You often want both `@memoize` and `@memoize(maxsize=128)`. Use a keyword-only argument and check whether a function was passed:
```python
import functools

def memoize(func=None, *, maxsize=None):
    def decorator(f):
        cache = {}                              # state lives in the closure
        @functools.wraps(f)
        def wrapper(*args):
            if args not in cache:
                cache[args] = f(*args)
            return cache[args]
        wrapper.cache_clear = cache.clear       # expose helpers as attributes
        return wrapper
    if func is not None:                        # used as bare @memoize
        return decorator(func)
    return decorator                            # used as @memoize(...)
```
This is exactly how `functools.lru_cache` and `dataclasses.dataclass` accept both forms.

## 4. Class-based decorators, and why methods break
A class with `__call__` can be a decorator, and its state lives in plain attributes:
```python
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)    # the class version of @wraps
        self.func, self.calls = func, 0
    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)
```
On a **method** this fails: `obj.method()` → `TypeError: missing 'self'`. Plain functions are **descriptors** (Day 002): their `__get__` binds `self`. Your instance isn't one, so add a `__get__`:
```python
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                          # accessed on the class
        return functools.partial(self, obj)      # bind obj as the first argument
```

## 5. Stacking order
```python
@a
@b
def f(): ...        # f = a(b(f)): b wraps first, a is the outermost layer
```
`a`'s wrapper runs first at call time. Put timing or logging **outside** caching if you want to measure cache hits, and **inside** it if you only want to measure real work.

## Pitfalls
- Late binding in loops (lambdas, callbacks, `threading.Thread(target=...)`). Bind with a default argument or `partial`.
- `x += 1` on a captured name without `nonlocal` raises `UnboundLocalError`.
- Mutable cache keys: `args` containing a `list` is unhashable → `TypeError`. Decide whether to reject it or convert it.
- Only including `args` in the cache key: `f(1, b=2)` and `f(1, 2)` are different keys, and `**kwargs` would be ignored entirely if you forgot them.
- Class decorators on methods without `__get__`. A shared counter on the decorator also means **all instances share state**, which may or may not be what you want.
- `@wraps` copies `__name__`, `__doc__`, `__module__`, `__qualname__`, `__dict__` and sets `__wrapped__`, which `inspect.signature` follows. Without it, your decorated function's signature shows up as `(*args, **kwargs)`.
