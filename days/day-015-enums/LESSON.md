# Day 015: Enums (~5 min read)

Magic strings and ints like `status == "actve"` or `if level == 3` fail quietly. An `Enum` gives you a closed set of named constants. Typos become `AttributeError`, an IDE can autocomplete the names, and each member knows its own name and value. Enums are also classes, so the classes and dunders from Days 001–002 apply to them.

## 1. The basics
```python
from enum import Enum, auto

class Status(Enum):
    PENDING = auto()      # 1
    RUNNING = auto()      # 2
    DONE = auto()         # 3

s = Status.RUNNING
print(s, s.name, s.value)      # Status.RUNNING RUNNING 2
print(Status(2) is s)          # lookup by value -> True (members are singletons)
print(Status["DONE"])          # lookup by name  -> Status.DONE
print(list(Status))            # iteration is in definition order
print(Status.DONE == 3)        # False: a plain Enum is NOT its value
```
Compare members with `is` or `==`. Because they're singletons, `is` is idiomatic. A bad lookup like `Status(99)` raises `ValueError`, and `Status["NOPE"]` raises `KeyError`.

## 2. Enums are classes: add behaviour
```python
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @property
    def is_urgent(self) -> bool:
        return self is Priority.HIGH

    def __lt__(self, other):            # make members orderable
        if not isinstance(other, Priority):
            return NotImplemented
        return self.value < other.value

    @classmethod
    def parse(cls, text: str) -> "Priority":
        return cls[text.strip().upper()]   # " high " -> Priority.HIGH

print(sorted([Priority.HIGH, Priority.LOW]))   # [<Priority.LOW: 1>, <Priority.HIGH: 3>]
```
You can also define `_missing_` as a classmethod hook. It runs when `Cls(value)` finds no member, so you can normalise input or return a default there.

## 3. `StrEnum`, `IntEnum` and `Flag`
```python
from enum import StrEnum, Flag, auto

class Color(StrEnum):           # 3.11+: members ARE strings
    RED = auto()                # value "red" (lower-cased name)
print(Color.RED == "red", f"{Color.RED}")   # True red  -> great for JSON / configs

class Perm(Flag):               # bit flags you can combine
    READ = auto()               # 1
    WRITE = auto()              # 2
    EXEC = auto()               # 4

rw = Perm.READ | Perm.WRITE
print(Perm.WRITE in rw, Perm.EXEC in rw)    # True False
print(rw & ~Perm.WRITE)                     # Perm.READ
print(list(rw))                             # [Perm.READ, Perm.WRITE]  (3.11+)
```
Use `StrEnum`/`IntEnum` only when you *need* the members to compare equal to raw values, for example at a serialisation boundary. Everywhere else, a plain `Enum` is safer.

## Common pitfalls
- **Duplicate values create aliases, not new members.** `A = 1; B = 1` makes `B` an alias of `A`. Add `@enum.unique` to make that an error.
- **`Status.DONE == "DONE"` is `False`** for a plain `Enum`. Compare to members, or parse the input first with `Status[...]` / `Status(...)`.
- **Members aren't orderable by default.** `<` raises `TypeError` unless you define it, or use `IntEnum`/`functools.total_ordering`.
- **Don't mutate members or add instance state.** They're shared singletons, so you'd be changing global state.
- `auto()` values are an implementation detail. Don't persist them if the definition order might change. Store `.name` instead.
