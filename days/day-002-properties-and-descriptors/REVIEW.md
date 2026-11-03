# Review: Day 002 - Properties, descriptors & encapsulation

**Tests:** none (assignment is self-checked via the `__main__` demo). I ran your demo and extra probes by hand.

**Result:** Part 1 and Part 2 complete (all 6 requirements met); bonus half done (`Discount` yes, `Money.apply` missing).

## Done well
- `Bounded` is a correct data descriptor: `__set_name__`, per-instance storage, `return self` on class access, inclusive bounds, and `type(value) is not int` rejects `True` and `5.0`. `isinstance` would have let `True` through, since `bool` subclasses `int`.
- All of Day 001's review is fixed: strict `int` amount, `.strip()` + `is_valid_currency` in the constructor, and a separate `TypeError` for a non-`str` currency. It's now immutable through read-only properties and `__slots__`, so hashing is safe, and the set demo proves it.
- `__eq__` still returns `NotImplemented`, `__hash__` matches `__eq__`, and the demo covers every requirement, errors included.

## Improvements
1. **`Bounded` breaks on a `__slots__` class.** It stores through `setattr(obj, "_percent", ...)`, so an owner with `__slots__` (like your own `Money`) fails with `AttributeError: no attribute '_p'`. Reading before any assignment also gives a confusing `'_percent'` error. Because a *data* descriptor beats the instance `__dict__`, you can store under the public name and raise a clear error:

   ```python
   def __set_name__(self, owner, name):
       self.public, self.private = name, f"_{name}"

   def __get__(self, obj, objtype=None):
       if obj is None:
           return self
       try:
           return getattr(obj, self.private)
       except AttributeError:
           raise AttributeError(f"{self.public!r} has not been set") from None
   ```
   (For slotted owners, list `_percent` in `__slots__`. Either way, the error now names the real attribute.)

2. **Error messages.** `f"Expected {type(1)} got {type(value)}"` prints `<class 'int'>`. Use `type(value).__name__` as you did in `Money`, and say *what* was out of range: `f"percent must be between 0 and 100, got 101"`. In a test failure, that's the line you read first.

3. **Subclass-friendly + finish the bonus.** `with_amount` hard-codes `Money(...)`, so a subclass gets a plain `Money` back. Use `type(self)(amount, self._currency)`. `apply` is then a few lines:

   ```python
   def apply(self, discount: "Discount") -> "Money":
       return self.with_amount(self._amount * (100 - discount.percent) // 100)
   ```

Small things: the demo assigns `d.percent = "23"` but created `e` for it (`c`, `d`, `e` could all be one `Discount()`). `Money` has no type hints, though `Bounded` does. `m._amount = 5` still works: properties signal intent, they don't enforce privacy. If you need it truly frozen, use `@dataclass(frozen=True, slots=True)`.
