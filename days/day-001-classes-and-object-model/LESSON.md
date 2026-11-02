# Day 001: Classes & the Python object model

We assume you can write a basic class. Here we look at what actually makes an object tick.

## 1. Everything is an object; names are references
```python
a = [1, 2]
b = a            # same object, two names
b.append(3)
print(a)         # [1, 2, 3]
print(a is b, id(a) == id(b))  # True True
```
`==` compares values (via `__eq__`), `is` compares identity. Mutable objects shared by reference are the root of many bugs.

## 2. Instance state vs class state
```python
class Counter:
    instances = 0              # class attribute: shared
    def __init__(self, start=0):
        self.value = start     # instance attribute: per object
        Counter.instances += 1

c1, c2 = Counter(), Counter(5)
print(Counter.instances, c1.value, c2.value)  # 2 0 5
```
Attribute lookup: instance `__dict__` first, then the class (then its bases). Assigning `c1.instances = 9` creates a *new instance attribute* and shadows the class one.

Pitfall: never use a mutable default argument.
```python
def add(x, bucket=[]):      # bug: one list shared across calls
    bucket.append(x); return bucket
def add(x, bucket=None):    # fix
    bucket = [] if bucket is None else bucket
    bucket.append(x); return bucket
```

## 3. Methods: instance, class, static
```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, f):      # alternative constructor
        return cls((f - 32) * 5 / 9)

    @staticmethod
    def is_valid(c):                  # no self/cls needed
        return c >= -273.15
```

## 4. Making objects behave: `__repr__`, `__eq__`, `__hash__`
```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x!r}, {self.y!r})"   # unambiguous, ideally eval-able

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))             # must agree with __eq__

print({Point(1, 2), Point(1, 2)})   # one element
```
Rules: if you define `__eq__`, Python sets `__hash__` to `None` unless you also define it. Equal objects must have equal hashes, and hashed fields should not change while the object is in a set/dict key.

Return `NotImplemented` (not `False`) for unsupported types so Python can try the other operand.

## Pitfalls
- Forgetting `__repr__`: debugging output becomes `<__main__.Point object at 0x...>`.
- Defining `__eq__` without `__hash__` makes instances unhashable.
- Mutating a hashed object that lives in a set/dict.
- Shared mutable class attributes (`items = []` at class level).
