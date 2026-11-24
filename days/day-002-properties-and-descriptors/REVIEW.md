# Review: Day 002 - Properties, descriptors & encapsulation

**Tests:** none (self-checked via the `__main__` demo). I ran the demo and extra probes by hand; everything in the spec behaves correctly.

## Done well
- `Bounded` is textbook: `__set_name__`, per-instance storage, `return self` on class access, and `type(value) is not int` correctly rejects `bool` (which `isinstance` would let through).
- `Money` is now properly immutable: read-only properties + `__slots__`, so hashing is safe. The demo proves it (`still in set: True`).
- Day 001's review fixes were all applied: strip + `is_valid_currency`, strict `int` check, `with_amount` returns a new object.
- Good demo coverage of every error path.

## Improvements
1. **Bonus half-finished.** `Discount` uses `Bounded`, but `Money.apply(discount)` is missing. Also the demo creates `e = Discount()` and then tests `d` instead, so `e` is unused.
2. **Reading an unset descriptor gives a confusing error:** `Discount().percent` -> `AttributeError: ... no attribute '_percent'` leaks the private storage name. Either set a default or raise a clear message:
   ```python
   def __get__(self, obj, objtype=None):
       if obj is None:
           return self
       try:
           return getattr(obj, self.name)
       except AttributeError:
           raise AttributeError(f"{self.public_name!r} has not been set") from None
   ```
3. **Small edge cases:** `with_amount` hard-codes `Money(...)`, so a subclass gets a plain `Money` back; use `type(self)(...)`. And `str.isalpha()` accepts non-ASCII (`Money(5, 'ééé')` -> `ÉÉÉ`); add `and code.isascii()` if you want ISO-style codes.
4. Style: trailing whitespace, and the error message `type(1)` could just be `int.__name__`.
