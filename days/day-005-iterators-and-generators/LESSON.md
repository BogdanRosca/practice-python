# Day 005: Iterators & Generators (~5 min)

Day 004's `Wallet.__iter__` just returned `iter(self._items)`. Today: what `iter()`/`next()` actually do, how to write your own lazy iterators, and why generators are usually the easiest way.

## 1. Iterable vs iterator
| | Has | Meaning |
|---|---|---|
| **Iterable** | `__iter__()` returning an iterator | "can be looped over, many times" (list, Wallet) |
| **Iterator** | `__next__()` + `__iter__()` returning `self` | "a cursor": one pass, then exhausted |

`for x in obj` is just:
```python
it = iter(obj)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    ...
```

A hand-written iterator class:
```python
class Countdown:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self                 # iterators are iterable too
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

c = Countdown(3)
print(list(c), list(c))   # [3, 2, 1] []   <- exhausted after one pass!
```

## 2. Generators: iterators for free
A function containing `yield` returns a **generator** (an iterator) when called. Its body runs lazily, pausing at each `yield`; returning ends it with `StopIteration`.
```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1

class Countdown2:               # re-iterable: each loop gets a fresh generator
    def __init__(self, start):
        self.start = start
    def __iter__(self):
        yield from countdown(self.start)   # __iter__ as a generator method

c = Countdown2(3)
print(list(c), list(c))   # [3, 2, 1] [3, 2, 1]
```
Rule of thumb: **containers** implement `__iter__` (often as a generator); only **cursors** implement `__next__`.

## 3. Laziness & pipelines
Generators compute values on demand, so they can be infinite and chain cheaply:
```python
import itertools

def naturals():
    n = 0
    while True:
        yield n
        n += 1

evens = (n for n in naturals() if n % 2 == 0)      # generator expression
squares = (n * n for n in evens)
print(list(itertools.islice(squares, 5)))          # [0, 4, 16, 36, 64]
```
Nothing runs until something pulls values (`next`, `for`, `list`, `sum`, ...).

## Pitfalls
- **Single use:** a generator/iterator is exhausted after one pass. `gen = (x for x in data); sum(gen); max(gen)` -> `ValueError` on empty.
- **`__iter__` returning `self` on a container** makes it a one-shot object: nested loops over it break.
- **Don't `raise StopIteration` inside a generator** (it becomes `RuntimeError`, PEP 479); just `return`.
- **Mutating a list while iterating** it skips elements; iterate over a copy or build a new list.
- `list(infinite_gen)` never returns; use `itertools.islice` or a `break`.
