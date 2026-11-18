# Assignment 004: Money arithmetic + a `Wallet` container (~15 min)

Create `solution.py` in this folder, push to this branch, merge the PR. Start by copying your immutable `Money` from Day 002 (with the REVIEW.md fixes if you like: `type(self)(...)`).

**Part 1 - operators on `Money`** (all return **new** objects; never mutate):
1. `m1 + m2` and `m1 - m2` for the same currency. Different currencies -> `ValueError`. Non-`Money` operand -> `return NotImplemented` (so `m + 5` ends in `TypeError`). A subtraction that would go negative -> `ValueError` (amount is still >= 0).
2. `m * 3` **and** `3 * m` with an `int` only (reject `float` and `bool` via `NotImplemented`).
3. `sum([m1, m2, m3])` works without passing a start value (hint: `__radd__` must accept `0`).
4. `bool(Money(0, "USD"))` is `False`, any positive amount is `True`.

**Part 2 - `Wallet` container** (composition: wrap a `list` of `Money`, single currency set in `__init__(self, currency)`):
1. `add(money)` - `TypeError` if not `Money`, `ValueError` if wrong currency.
2. `len(w)`, `w[0]`, `w[-1]`, and `w[1:3]` returning a **new `Wallet`** (same currency), not a list.
3. `money in w` and `for m in w: ...` work.
4. `w.total()` returns a `Money` (use `sum`; an empty wallet returns `Money(0, currency)`).
5. `__repr__` like `Wallet('USD', 3 items, total 12.34 USD)`.

Bonus: `w1 + w2` returns a new `Wallet` with both contents (same currency only), and explain in a comment why `Wallet` *should* define `__iadd__` while `Money` should not.

End with an `if __name__ == "__main__":` demo printing each behaviour (including the errors, via `try/except`).
