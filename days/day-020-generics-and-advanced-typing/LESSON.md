# Day 020: Generics & advanced typing (~5 min read)

Type hints pay off most in shared code: framework helpers, API clients, test utilities. Writing `list[Any]` or `Callable[..., Any]` there means callers lose all checking and autocomplete. **Generics** let one function or class keep the caller's real types: `Stack[int]` stays `int` from `push` to `pop`, and a decorator keeps the wrapped function's exact signature.

Everything here is checked by a static type checker (`mypy`, `pyright`) and does nothing at runtime. Install one with `pip install mypy`, then run `mypy --strict file.py`.

## 1. `TypeVar`: "the same type in and out"
```python
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")
D = TypeVar("D")

def first(items: Iterable[T], default: D) -> T | D:
    return next(iter(items), default)

reveal_type(first([1, 2], None))   # mypy: "int | None"
reveal_type(first("ab", ""))       # mypy: "str"
```
A `TypeVar` is a placeholder the checker fills in **for each call**. With `Any`, the result would be `Any` and every typo after it goes unchecked.

**Bounds** restrict what a `TypeVar` can be. Combine one with a `Protocol` to say "anything that supports `<`":
```python
from typing import Any, Protocol

class SupportsLessThan(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...

CT = TypeVar("CT", bound=SupportsLessThan)

def smallest(items: Iterable[CT]) -> CT: ...   # ints in, int out; object() is rejected
```
`TypeVar("N", int, float)` (a **constrained** TypeVar) is different: it must be exactly one of those types.

## 2. Generic classes
```python
from typing import Generic

class Box(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item
    def get(self) -> T:
        return self.item

b = Box(42)            # inferred Box[int]
e: Box[str] = Box("")  # or annotate explicitly
```
On Python 3.12+ you can write `class Box[T]:` and `def first[T](items: Iterable[T]) -> T:` without declaring `TypeVar`s. Both styles mean the same thing. This lesson uses the older style so it works on 3.10+.

## 3. Typing decorators with `ParamSpec`
A decorator typed `Callable[..., Any]` erases the signature: `add(1, "2")` is no longer an error. `ParamSpec` captures the parameters, and `TypeVar` captures the return type:
```python
import functools
from collections.abc import Callable
from typing import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def logged(fn: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("calling", fn.__name__)
        return fn(*args, **kwargs)
    return wrapper
```
A decorator **factory** (`@retry(3)`) adds one layer: `def retry(times: int) -> Callable[[Callable[P, R]], Callable[P, R]]`.

## 4. `@overload`: different return types for different calls
```python
from typing import overload

@overload
def get(key: str) -> str | None: ...
@overload
def get(key: str, default: D) -> str | D: ...
def get(key: str, default: object = None) -> object:   # the real implementation, not visible to callers
    return ENV.get(key, default)
```
Callers see only the overloads. The checker doesn't verify the implementation against them, so keep it simple.

## 5. Testing your types
`reveal_type(x)` makes mypy print the inferred type. To check that bad code is *rejected*, put `# type: ignore[code]` on it and run with `--warn-unused-ignores`. If the line ever stops being an error, mypy reports the ignore as unused, so it works like a test that fails.

## Common pitfalls
- **One `TypeVar` per role.** `def f(a: T, b: T)` with `f(1, "x")` gets solved as `T = object`, not rejected. Use bounds when "same type" really matters.
- **`list` is invariant**: a `list[bool]` isn't a `list[int]`, because you could append an `int` to it. Accept `Sequence[int]` or `Iterable[int]` when you only read.
- **Don't reuse a class's `T` in a method** that should be generic on its own. Give that method a fresh `TypeVar`.
- **`Optional` returns force checks**: `peek() -> T | None` means callers must handle `None`. That's the point, but only use it when "no value" really can happen.
- Generics are erased at runtime: `isinstance(x, Box[int])` is a `TypeError`. Use `isinstance(x, Box)`.
