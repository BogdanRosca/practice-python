# Assignment 010: Transaction analytics with the stdlib (~15 min)

Create `solution.py` in this folder, push to this branch, merge the PR. **Rule of the day:** no manual `if key in dict` bookkeeping and no hand-written index loops. Reach for `collections`, `itertools` and `functools`. Type-hint everything.

Start from this data (paste it in):
```python
from decimal import Decimal
from typing import NamedTuple

class Tx(NamedTuple):
    day: str          # "2026-11-01"
    category: str     # "food", "rent", ...
    amount: Decimal   # negative = spend, positive = income

TXS = [
    Tx("2026-11-01", "salary", Decimal("3000")),
    Tx("2026-11-01", "food",   Decimal("-12.50")),
    Tx("2026-11-02", "food",   Decimal("-8.20")),
    Tx("2026-11-02", "rent",   Decimal("-1200")),
    Tx("2026-11-03", "fun",    Decimal("-45")),
    Tx("2026-11-03", "food",   Decimal("-30.10")),
    Tx("2026-11-05", "fun",    Decimal("-15")),
]
```

**Part 1: `collections`**
1. `spend_by_category(txs) -> dict[str, Decimal]`: total spend per category (spend only, as positive numbers), using `defaultdict`.
2. `top_categories(txs, n) -> list[tuple[str, int]]`: the `n` categories with the most transactions, using `Counter`.
3. `recent(txs, n) -> list[Tx]`: the last `n` transactions, using a `deque(maxlen=n)` (pretend `txs` is a stream you can only iterate once).

**Part 2: `itertools`**
1. `running_balance(txs) -> list[Decimal]`, using `accumulate`.
2. `daily_totals(txs) -> dict[str, Decimal]`, using `groupby`. In a comment, say what breaks if `txs` isn't sorted by day.
3. `biggest_jump(txs) -> tuple[Decimal, Decimal]`: the pair of consecutive running balances with the largest absolute change, using `pairwise` and `max(..., key=...)`.

**Part 3: `functools`**
1. `fx_rate(currency: str) -> Decimal`: pretend it's slow (`time.sleep(0.2)`, then return from a dict). Cache it with `@lru_cache(maxsize=32)`. Call it 5 times, then print `fx_rate.cache_info()`.
2. `describe = singledispatch(...)` with overloads for `Tx` (`"2026-11-01 food -12.50"`), `Decimal` (`"€12.50"`, 2 dp) and `list` (each element described on its own line).

**Bonus:** `total_spend = reduce(...)` over the spends. In a comment, explain why `sum()` is the better choice here, and give one real case where `reduce` is the right tool. Also, in one sentence, explain why `@cache` on an instance method is a memory leak.

End with an `if __name__ == "__main__":` demo printing each result.
