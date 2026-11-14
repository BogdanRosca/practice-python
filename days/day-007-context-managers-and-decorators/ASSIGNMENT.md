# Assignment 007: Transactions & instrumentation for `Wallet` (~15 min)

Create `solution.py` in this folder, push to this branch, merge the PR. Reuse your Day 006 `Money`/`Wallet` dataclasses (copy them in, or a minimal `Wallet` with `items: list[Money]` and `add()`). Type-hint everything.

**Part 1 - `transaction` context manager (class-based)**
1. `class Transaction` with `__init__(self, wallet: Wallet)`, `__enter__` returning the wallet, and `__exit__` that restores `wallet.items` to its pre-`with` contents if the body raised.
2. Exceptions must **propagate** (don't suppress). Restore the list *in place*, so other references to `wallet.items` see the rollback.
3. Demo: a `with` block that adds two items and then raises `ValueError` → the wallet is unchanged and the error is still caught by your outer `try/except`.

**Part 2 - same thing with `@contextmanager`**
1. `def transaction(wallet: Wallet) -> Iterator[Wallet]` decorated with `@contextmanager`, same behaviour as Part 1.
2. Add one extra behaviour: after a **successful** block, print `committed N item(s)` (N = number of items added).

**Part 3 - decorators**
1. `count_calls`: no arguments; stores the number of calls on `wrapper.calls`. Use `functools.wraps`; show `add.__name__` is still `"add"`.
2. `max_total(limit: Decimal)`: decorator *with arguments* for `Wallet` methods; after the method runs, if any currency's total exceeds `limit`, undo the change (hint: reuse your `transaction`) and raise `ValueError`. Apply it to `Wallet.add`.
3. Demo: stacking `@count_calls` over `@max_total(...)` on `add`, and one add that gets rejected and rolled back.

Bonus: make `Transaction` usable as **both** a context manager and a decorator by subclassing `contextlib.ContextDecorator` (`@Transaction(wallet)` on a function). Note in a comment why this only works nicely when the wallet is known at decoration time.

End with an `if __name__ == "__main__":` demo printing each behaviour (errors via `try/except`).
