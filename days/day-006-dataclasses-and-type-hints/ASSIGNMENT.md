# Assignment 006: Rebuild `Money` & `Wallet` as dataclasses (~15 min)

Create `solution.py` in this folder, push to this branch, merge the PR. Fully type-hint every function and method (aim for `mypy --strict` clean, optional to actually run).

**Part 1 - `Money` as a frozen dataclass**
1. `@dataclass(frozen=True, slots=True) class Money` with fields `amount: Decimal` and `currency: str`. No hand-written `__init__`, `__repr__`, `__eq__` or `__hash__`.
2. `__post_init__`: accept `int`/`str`/`Decimal` amounts (convert via `Decimal(str(...))`, quantize to 2 places); currency must be 3 uppercase letters, else `ValueError`.
3. `__add__` returning a new `Money` (different currencies -> `ValueError`; return `NotImplemented` for non-`Money`).
4. Demo: `Money("1.005", "USD")` repr, that `m.amount = 5` raises `dataclasses.FrozenInstanceError`, that two equal `Money` collapse to one in a `set`, and `dataclasses.replace(m, amount=Decimal("2"))`.

**Part 2 - `Wallet` as a mutable dataclass**
1. Fields: `owner: str`, `items: list[Money]` (use `default_factory`), and `MAX_ITEMS: ClassVar[int] = 50`.
2. `add(self, m: Money) -> None` raising `ValueError` past `MAX_ITEMS`; `__iter__` as a generator (`-> Iterator[Money]`).
3. `total(self, currency: str) -> Money` summing only that currency (empty -> `Money(0, currency)`).
4. Demo: `Wallet("bogdan")` twice shows they don't share `items`, and `hash(wallet)` raises `TypeError` - add a one-line comment on why.

**Part 3 - quick reflection** (comment at the bottom, 2-3 lines): what did the dataclass version remove compared to your Day 002/004 classes, and what (if anything) did you lose?

Bonus: `@dataclass(order=True)` `Expense` with `sort_key: Decimal = field(init=False, repr=False)` set in `__post_init__` from `money.amount`, plus `money: Money = field(compare=False)` and `label: str = field(compare=False)`, so `sorted(expenses)` orders by amount only.

End with an `if __name__ == "__main__":` demo printing each behaviour (errors via `try/except`).
