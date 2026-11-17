# Assignment 005: Lazy iteration over money (~15 min)

Create `solution.py` in this folder, push to this branch, merge the PR. Reuse your `Money` and `Wallet` from Day 004 (or a minimal version: `Money(amount, currency)` with `__add__` and an `amount` property, and a `Wallet` wrapping a list).

**Part 1 - fix up `Wallet` iteration**
1. Rewrite `Wallet.__iter__` as a **generator method** (`yield`/`yield from`), not `return iter(...)`.
2. Prove it is re-iterable: two nested `for` loops over the same wallet print every pair.

**Part 2 - generator functions** (module-level, lazy: no building full lists internally)
1. `running_totals(moneys)` - yields the cumulative `Money` after each item: `[1, 2, 3] USD` -> `1, 3, 6 USD`. Empty input yields nothing.
2. `in_batches(iterable, size)` - yields lists of up to `size` items: `in_batches(range(5), 2)` -> `[0, 1], [2, 3], [4]`. `size < 1` -> `ValueError` (hint: where does the error fire for a generator? Make it fire at **call** time, not at first `next()`, by splitting into a plain function that validates and an inner generator).
3. It must work on an **infinite** input: `next(in_batches(itertools.count(), 3))` -> `[0, 1, 2]`.

**Part 3 - a hand-written iterator class**
`Installments(total: Money, parts: int)` - an **iterator** (`__iter__` returns `self`, `__next__` raises `StopIteration`) yielding `parts` `Money` values that add up exactly to `total`, with the remainder cents spread over the first ones: `Installments(Money(10.00, "USD"), 3)` -> `3.34, 3.33, 3.33`. Show in the demo that it is exhausted after one `list(...)`.

Bonus: `Wallet.largest(n)` returning the `n` biggest items using `heapq.nlargest` with a `key`, and a one-line comment on why it accepts any iterable.

End with an `if __name__ == "__main__":` demo printing each behaviour (including the `ValueError`, via `try/except`).
