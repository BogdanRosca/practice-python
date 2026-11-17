# Day 006: Dataclasses & Type Hints (~5 min)

Days 001-005 you hand-wrote `__init__`, `__repr__`, `__eq__`, `__hash__` and read-only properties for `Money`. `@dataclass` generates all of that from annotated fields, and type hints make the contract explicit for readers, IDEs and `mypy`.

## 1. What `@dataclass` writes for you
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float = 0.0          # defaults go after non-defaults

p = Point(1.5)
print(p)                    # Point(x=1.5, y=0.0)   <- __repr__
print(p == Point(1.5, 0))   # True                  <- __eq__ compares fields as a tuple
```
Only **annotated class attributes** become fields. `count = 0` without an annotation stays a plain class attribute.

Useful flags:
| Flag | Effect |
|---|---|
| `frozen=True` | assigning a field raises `FrozenInstanceError`; also generates `__hash__` |
| `order=True` | `<`, `<=`, ... comparing fields in declaration order |
| `slots=True` (3.10+) | `__slots__`: less memory, no accidental new attributes |
| `kw_only=True` (3.10+) | all fields keyword-only: `Point(x=1, y=2)` |

Hash rule (Day 001 again): `eq=True` + not frozen -> `__hash__ = None` (unhashable). That's the safe default for mutable objects.

## 2. Mutable defaults & `field()`
```python
from dataclasses import dataclass, field

@dataclass
class Wallet:
    owner: str
    items: list[str] = field(default_factory=list)   # NOT `= []`
    _cache: dict = field(default_factory=dict, repr=False, compare=False)
```
`items: list = []` is rejected with `ValueError` at class-creation time: dataclasses protect you from the shared-mutable-default bug. `field()` also controls `repr`, `compare`, `init`, `kw_only` per field.

## 3. Validation & derived values: `__post_init__`
The generated `__init__` calls `__post_init__` after assigning fields:
```python
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if len(self.currency) != 3:
            raise ValueError(f"bad currency {self.currency!r}")
        # frozen: self.amount = ... would raise, so bypass once:
        object.__setattr__(self, "amount", Decimal(self.amount).quantize(Decimal("0.01")))
```
Need a non-field that's computed? `total: Decimal = field(init=False)` and set it in `__post_init__`.

"Modify" a frozen instance by making a new one: `dataclasses.replace(m, amount=Decimal("5"))` (it re-runs `__init__` and `__post_init__`).

## 4. Type hints worth knowing (3.10+ syntax)
```python
from typing import ClassVar, Self   # Self: 3.11+
from collections.abc import Iterable, Iterator

def total(items: Iterable[Money]) -> Money | None: ...     # accept the loosest type
def evens(n: int) -> Iterator[int]: ...                    # generators: Iterator[T]

@dataclass
class Account:
    MAX: ClassVar[int] = 10      # ClassVar -> NOT a dataclass field
    tags: tuple[str, ...] = ()   # variable-length tuple
    def renamed(self, name: str) -> Self: ...
```
- Hints are **not enforced at runtime**. `Point("a", "b")` works fine. Validate in `__post_init__` if it matters, check statically with `mypy`.
- Accept abstract (`Iterable`, `Mapping`), return concrete (`list`, `dict`).

## Pitfalls
- **Field order**: a field without a default after one with a default -> `TypeError`. Fix with `kw_only=True` or reorder.
- **Inheritance**: subclass fields are appended after the parent's, so the same ordering rule bites across classes.
- `frozen=True` is shallow: a frozen dataclass holding a `list` can still have that list mutated. Prefer `tuple`.
- `order=True` compares the *whole* field tuple, including currency strings. Often you want a custom `__lt__` or `field(compare=False)` instead.
- `asdict()` deep-copies recursively: handy for JSON, slow on big object graphs.
