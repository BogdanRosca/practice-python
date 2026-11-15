# Assignment 008: A proper error API for `Money` & `Wallet` (~15 min)

Create `solution.py` in this folder, push to this branch, merge the PR. Start from your Day 006 dataclasses (copy them in, or a minimal frozen `Money(amount: Decimal, currency: str)` plus a `Wallet` with `items`, `MAX_ITEMS` and `add()`). Type-hint everything.

**Part 1 - the hierarchy**
1. `WalletError(Exception)` as the single base for the module.
2. `InvalidMoneyError(WalletError, ValueError)` for a bad amount or currency, with attribute `value` (the offending input).
3. `CurrencyMismatchError(WalletError, ValueError)` with attributes `left` and `right`.
4. `WalletFullError(WalletError)` with attribute `limit`.
5. Every class calls `super().__init__` with a readable message. Demo: `str(e)`, the attributes, and that `isinstance(e, ValueError)` is `True` for 2 and 3 but `False` for 4.

**Part 2 - use it**
1. `Money.__post_init__` raises `InvalidMoneyError`. A non-numeric amount like `"abc"` must raise it `from` the original `decimal.InvalidOperation`. Demo: print `e.__cause__`.
2. `Money.__add__` raises `CurrencyMismatchError`, and `Wallet.add` raises `WalletFullError`.
3. Show that an old-style caller doing `except ValueError` still catches the mismatch.

**Part 3 - batch import**
1. `def import_rows(wallet: Wallet, rows: list[tuple[str, str]]) -> None` takes `(amount, currency)` pairs. Add every valid row, collect every failure, and if there were any, raise `ExceptionGroup("import failed", errors)` at the end. Use `e.add_note(f"row {i}")` on each collected error so you can tell which row failed.
2. Demo with rows `[("10", "USD"), ("abc", "USD"), ("5", "usd"), ("3", "EUR")]`. Handle the result with `except* InvalidMoneyError` and print each error plus its notes (`e.__notes__`). Then show that the 2 valid rows are in the wallet.

Bonus: make `import_rows` atomic. If any row fails, the wallet must be unchanged. Reuse your Day 007 `transaction` context manager (or a `list` snapshot). In a comment, say whether the rollback should happen before or after raising the group, and why.

End with an `if __name__ == "__main__":` demo printing each behaviour (errors via `try/except`).
