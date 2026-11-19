# Day 003: Inheritance, `super()` & the MRO (~5 min)

Day 002 gave you immutable `Money`. Now: how classes reuse and extend each other, and when they *shouldn't*.

## 1. Inheritance and `super()`
A subclass inherits attributes/methods and can override them. Use `super()` to call the parent's version instead of copy-pasting it.

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def describe(self):
        return f"{self.owner}: {self.balance}"

class Savings(Account):
    def __init__(self, owner, balance=0, rate=0.02):
        super().__init__(owner, balance)   # reuse parent init
        self.rate = rate

    def describe(self):
        return super().describe() + f" @ {self.rate:.0%}"

print(Savings("Ana", 100).describe())   # Ana: 100 @ 2%
```
Forgetting `super().__init__(...)` is the classic bug: the parent's attributes silently never get set.

## 2. The MRO (Method Resolution Order)
With multiple inheritance Python linearises the class graph (C3 algorithm). `super()` doesn't mean "my parent" - it means **"the next class in the MRO"**.

```python
class A:
    def hi(self): return ["A"]
class B(A):
    def hi(self): return ["B"] + super().hi()
class C(A):
    def hi(self): return ["C"] + super().hi()
class D(B, C):
    def hi(self): return ["D"] + super().hi()

print(D().hi())        # ['D', 'B', 'C', 'A']  - A appears once (the "diamond")
print(D.__mro__)       # D, B, C, A, object
```
For this to work every class in the chain must call `super()` (cooperative inheritance). Inspect with `Cls.__mro__` or `Cls.mro()`.

## 3. Mixins and composition
A **mixin** is a small class adding one behaviour, not meant to stand alone:

```python
class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class User(JsonMixin, Account): ...
```
Rule of thumb: **inheritance = "is a"; composition = "has a"**. Prefer composition (hold another object and delegate) when you only want to reuse behaviour; deep hierarchies get brittle.

```python
class Logger:
    def log(self, msg): print("LOG", msg)

class Service:
    def __init__(self):
        self.logger = Logger()      # composition, easy to swap/mock
```

## Pitfalls
- Not calling `super().__init__()` (or calling the wrong parent explicitly in a diamond -> parent runs twice).
- Mixins listed *after* the base class: `class User(Account, JsonMixin)` puts the mixin later in the MRO, so it can't override.
- Inheriting just to reuse code when the relationship isn't "is a" (a `Stack(list)` exposes `insert`, `sort`, ... that break stack semantics).
- Mutable class attributes shared by all subclasses/instances (Day 001!).
- `isinstance(x, Base)` is true for subclasses; `type(x) is Base` is not.
