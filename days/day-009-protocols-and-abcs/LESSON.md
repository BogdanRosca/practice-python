# Day 009: Protocols, ABCs & Duck Typing (~5 min)

Python cares about *what an object can do*, not *what it is*. If it has `__len__` and `__getitem__`, it works like a sequence. That is **duck typing**. It's flexible, but the contract lives only in your head. ABCs and Protocols write the contract down, so the interpreter or the type checker can enforce it.

## 1. ABCs: nominal contracts enforced at runtime
```python
from abc import ABC, abstractmethod
from decimal import Decimal

class PaymentMethod(ABC):
    @abstractmethod
    def charge(self, amount: Decimal) -> str: ...

    def charge_twice(self, amount: Decimal) -> list[str]:   # concrete "template" method
        return [self.charge(amount), self.charge(amount)]

class Card(PaymentMethod):
    def charge(self, amount: Decimal) -> str:
        return f"card charged {amount}"

PaymentMethod()            # TypeError: Can't instantiate abstract class ... 'charge'
Card().charge_twice(Decimal("5"))   # ['card charged 5', 'card charged 5']
```
- Subclasses **must** inherit (that's *nominal* typing), and the error appears at instantiation, not when the method is called.
- Abstract methods can still have a body, which subclasses can reach with `super().charge(...)`.
- Stack `@property` over `@abstractmethod` (in that order) to require an attribute-like member.

## 2. `collections.abc`: implement 2 methods, get 10 for free
```python
from collections.abc import Sequence

class Ledger(Sequence):
    def __init__(self, entries): self._entries = list(entries)
    def __getitem__(self, i): return self._entries[i]
    def __len__(self): return len(self._entries)

l = Ledger([3, 1, 3])
print(3 in l, l.index(1), l.count(3), list(reversed(l)))   # True 1 2 [3, 1, 3]
```
These mixins give you `__contains__`, `__iter__`, `__reversed__`, `index` and `count` built on your Day 004 dunders. `isinstance(x, collections.abc.Iterable)` checks a *capability*. It's better than `isinstance(x, list)`.

## 3. Protocols: structural typing (static duck typing)
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Chargeable(Protocol):
    def charge(self, amount: Decimal) -> str: ...

class GiftCard:                       # no inheritance at all
    def charge(self, amount: Decimal) -> str:
        return f"gift card -{amount}"

def checkout(method: Chargeable, amount: Decimal) -> str:
    return method.charge(amount)

checkout(GiftCard(), Decimal("3"))    # mypy accepts it: the *shape* matches
isinstance(GiftCard(), Chargeable)    # True (only because of @runtime_checkable)
```
- Use a Protocol when you **don't own** the implementing classes, or you want loose coupling (great for test doubles: any fake with the right methods fits).
- Use an ABC when you want shared implementation, or a runtime error for an incomplete subclass.

## Pitfalls
- `@runtime_checkable` `isinstance` only checks that the **names exist**. It doesn't check signatures or return types. `charge = 42` would still pass.
- Forgetting `@abstractmethod` on one method means the "abstract" class can be instantiated.
- Inheriting from a Protocol makes the subclass a regular class that only inherits the Protocol's default bodies (`...` returns `None`). Usually you don't want to inherit at all.
- Writing `isinstance(x, list)` checks everywhere defeats duck typing. Check capabilities (`Iterable`, `Mapping`) or just try it (EAFP, Day 008).
- Don't create an ABC with a single implementation "just in case". Add the abstraction when the second implementation shows up.
