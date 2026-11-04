# Day 003: Inheritance, `super()`, MRO & composition (~5 min)

Day 002's `Money` was a closed, immutable value. Today: extending classes safely, and knowing when *not* to.

## 1. Inheritance and `super()`
A subclass reuses and specialises a parent. `super()` delegates to "the next class in line", not necessarily the direct parent.

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner, self.balance = owner, balance

    def describe(self):
        return f"{self.owner}: {self.balance}"

class Savings(Account):
    def __init__(self, owner, balance=0, rate=0.02):
        super().__init__(owner, balance)   # never forget this
        self.rate = rate

    def describe(self):
        return super().describe() + f" @ {self.rate:.0%}"

print(Savings("Ana", 100).describe())      # Ana: 100 @ 2%
```

## 2. MRO: the method resolution order
With multiple inheritance Python linearises the hierarchy (C3 algorithm). Inspect it with `Cls.__mro__`. Each `super()` call moves one step along **that list**, so cooperative classes all get called once.

```python
class Base:
    def hello(self): return ["Base"]

class Loud(Base):
    def hello(self): return ["Loud"] + super().hello()

class Polite(Base):
    def hello(self): return ["Polite"] + super().hello()

class Both(Loud, Polite): pass

print(Both().hello())                       # ['Loud', 'Polite', 'Base']
print([c.__name__ for c in Both.__mro__])   # ['Both', 'Loud', 'Polite', 'Base', 'object']
```
`Loud`'s `super()` reaches `Polite`, a class `Loud` knows nothing about. That is why cooperative methods should use `super()` and accept/forward `**kwargs`.

## 3. Mixins and composition
A **mixin** is a small class adding one behaviour, never instantiated alone; put it *left* of the main base so it wins in the MRO.

```python
class ReprMixin:
    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({fields})"

class Point(ReprMixin):
    def __init__(self, x, y): self.x, self.y = x, y

print(Point(1, 2))                          # Point(x=1, y=2)
```
Rule of thumb: inherit for **"is-a"** (`Savings` is an `Account`); use **composition** ("has-a", hold another object and delegate) when you only want to reuse behaviour. Composition is easier to change and test (swap the part).

```python
class Logger:
    def log(self, msg): print("LOG:", msg)

class Service:
    def __init__(self, logger): self.logger = logger   # has-a
    def run(self): self.logger.log("running")
```

## Pitfalls
- Forgetting `super().__init__(...)`: parent state silently missing.
- Hard-coding `Parent.method(self)` in a diamond calls shared bases twice (or skip siblings); use `super()`.
- Deep hierarchies and "inherit just to reuse a helper" get brittle. Prefer composition.
- `isinstance(x, Parent)` is True for subclasses; `type(x) is Parent` is not. Choose deliberately.
- Mixins relying on attributes the host class must provide: document them.
