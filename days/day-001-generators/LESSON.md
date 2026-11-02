# Day 001: Generators & lazy iteration

## Concept
A **generator** is a function that uses `yield`. Calling it returns an iterator
immediately; the body runs only when you ask for the next value, pausing at each
`yield` and keeping its local state. A **generator expression** `(x*x for x in xs)`
is the compact form of the same idea.

## Why it matters
- **Memory**: process huge files/streams one item at a time.
- **Pipelines**: chain small lazy steps (`read -> parse -> filter`) with no intermediate lists.
- **Infinite sequences**: model them naturally and cut with `itertools.islice`.

## Examples
```python
from itertools import islice

def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

print(list(islice(fib(), 8)))  # [0, 1, 1, 2, 3, 5, 8, 13]
```

```python
def read_nonblank(lines):
    for line in lines:
        line = line.strip()
        if line:
            yield line

def upper(items):
    for s in items:
        yield s.upper()

print(list(upper(read_nonblank(["a\n", "\n", "b\n"]))))  # ['A', 'B']
```

```python
def inner():
    yield 1
    yield 2

def outer():
    yield 0
    yield from inner()   # delegate to a sub-generator
    yield 3

print(list(outer()))  # [0, 1, 2, 3]
```

## Pitfalls
- A generator is **single-use**: once exhausted, iterating again yields nothing.
- `len()` and indexing don't work; wrap with `list()` only when you need to.
- Nothing runs until the first `next()`, so errors in the body surface late.
- `return value` inside a generator ends it (value goes into `StopIteration`); don't `raise StopIteration` yourself.
- Avoid materialising (`list(gen)`) in the middle of a pipeline - it defeats laziness.
