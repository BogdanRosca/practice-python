# Assignment 002: Safer Money + a reusable descriptor (~15 min)

Create `solution.py` in this folder, push to this branch, merge the PR.

**Part 1 - descriptor.** Write a data descriptor `class Bounded` taking `minimum` and `maximum` (`Bounded(0, 100)`). It must use `__set_name__`, store the value per instance, raise `ValueError` when out of range (inclusive bounds) and `TypeError` if the value isn't an `int`, and return the descriptor itself when accessed on the class.

**Part 2 - immutable `Money`.** Rework Day 001's `Money` (take the good bits of your solution and the REVIEW.md fixes):
1. `amount` (int cents) and `currency` are **read-only properties**; assigning raises `AttributeError`.
2. Constructor validation: amount must be an `int` (`TypeError` otherwise) and >= 0 (`ValueError`); currency must pass `is_valid_currency` after `.strip()` and is upper-cased.
3. Keep `__repr__`, `__str__`, `__eq__`, `__hash__`; now hashing is safe - demonstrate it.
4. Add a read-only computed property `dollars` returning `amount / 100`.
5. Add `with_amount(self, amount)` returning a **new** `Money` (same currency) since the object can't change.
6. Use `__slots__`; show that `m.foo = 1` raises `AttributeError`.

Bonus: use `Bounded(0, 100)` in a small `Discount` class (`percent = Bounded(0, 100)`) and add `Money.apply(discount)` returning the discounted `Money`.

End the file with an `if __name__ == "__main__":` demo that prints each behaviour (including the errors, via `try/except`).
