# Day 002: Properties, Descriptors & Encapsulation (~5 min)

Yesterday's review: `Money` was hashable *and* mutable, so changing `amount` after putting it in a set broke lookups. Today: controlling attribute access.

## 1. `@property`: validated, computed attributes
Python has no `private`; the convention is `_name` for internals, and `@property` lets you start with a plain attribute and add logic later **without changing callers**.

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius          # goes through the setter

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):               # read-only computed attribute
        return self._celsius * 9 / 5 + 32
```
No setter = read-only (assigning raises `AttributeError`). Note `__init__` assigns via `self.celsius`, so validation runs there too.

## 2. Descriptors: reusable properties
A property is just a descriptor. Any object defining `__get__` / `__set__` / `__set_name__` in a **class attribute** controls access. Write the logic once, reuse across attributes and classes:

```python
class Positive:
    def __set_name__(self, owner, name):
        self.name = "_" + name
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                  # accessed on the class
        return getattr(obj, self.name)
    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError(f"{self.name[1:]} must be positive")
        setattr(obj, self.name, value)

class Rect:
    width = Positive()
    height = Positive()
    def __init__(self, w, h):
        self.width, self.height = w, h
```

## 3. `__slots__` and immutability
`__slots__ = ("a", "b")` removes the per-instance `__dict__` (less memory, typos like `obj.colour = ...` raise). For read-only objects combine private storage with getter-only properties (or `__setattr__` raising `AttributeError`).

## Pitfalls
- Inside a setter, assign `self._x`, not `self.x` -> infinite recursion.
- A descriptor must store data **per instance** (on `obj`), never on `self`, or all instances share one value.
- Data descriptors (with `__set__`) beat the instance `__dict__`; non-data ones (only `__get__`, e.g. functions) lose to it.
- `__get__` should handle `obj is None` (class access).
