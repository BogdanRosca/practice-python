# Day 004: Dunder Methods for Containers & Operators (~5 min)

Day 002 made `Money` immutable; Day 003 showed `Canvas` *having* a list instead of *being* one. Today: make your own objects work with Python's syntax (`len(x)`, `x[i]`, `in`, `for`, `+`, `sum()`) by implementing the **protocols** the interpreter calls.

## 1. Container protocol
| Syntax | Calls |
|---|---|
| `len(c)` | `c.__len__()` (must return an `int >= 0`) |
| `c[k]` | `c.__getitem__(k)`; `k` may be an `int` **or a `slice`** |
| `x in c` | `c.__contains__(x)` (fallback: iterate) |
| `for x in c` | `iter(c)` -> `c.__iter__()` (fallback: `__getitem__(0, 1, ...)` until `IndexError`) |
| `bool(c)` | `__bool__`, else `__len__() != 0` |

```python
class Playlist:
    def __init__(self, songs=()):
        self._songs = list(songs)

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(self._songs[index])   # slicing returns a Playlist
        return self._songs[index]                    # list handles IndexError / negatives

    def __iter__(self):
        return iter(self._songs)

    def __contains__(self, song):
        return song in self._songs

p = Playlist(["a", "b", "c"])
print(len(p), p[-1], p[:2]._songs, "b" in p, list(p))   # 3 c ['a', 'b'] True ['a', 'b', 'c']
```
Delegating to the wrapped list gives you negative indices, `IndexError` and slicing for free.

## 2. Operator protocol
`a + b` tries `a.__add__(b)`; if that returns **`NotImplemented`** (the singleton, not an exception), Python tries `b.__radd__(a)`; if both decline -> `TypeError`.

```python
class Vec:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, other):
        if not isinstance(other, Vec):
            return NotImplemented
        return Vec(self.x + other.x, self.y + other.y)
    def __mul__(self, k):                 # Vec * 3
        if not isinstance(k, int | float):
            return NotImplemented
        return Vec(self.x * k, self.y * k)
    __rmul__ = __mul__                    # 3 * Vec
    def __repr__(self):
        return f"Vec({self.x}, {self.y})"

print(Vec(1, 2) + Vec(3, 4), 3 * Vec(1, 2))   # Vec(4, 6) Vec(3, 6)
```
`sum(items)` starts from `0`, so it computes `0 + item` -> needs `__radd__` that accepts `0`.

`a += b` calls `__iadd__` if defined (mutate in place, `return self`), otherwise falls back to `a = a + b`. **Immutable** types should *not* define `__iadd__`.

## Pitfalls
- `raise NotImplementedError` vs `return NotImplemented`: operators **return** `NotImplemented` so the other operand gets a turn. Raising stops that.
- Forgetting `slice` in `__getitem__`: `c[1:3]` passes a `slice` object, not an int.
- Returning a new object from operators on immutable types; don't mutate `self`.
- `bool` is an `int` subclass: `Money(5, "USD") * True` works unless you exclude it.
- Defining `__eq__` sets `__hash__` to `None` (Day 001!); containers holding mutable state usually *should* be unhashable.
