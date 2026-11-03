# Assignment 001: Money (~15 min)

Create `solution.py` in this folder and push it to this branch.

Implement a class `Money` representing an amount in a currency.

Requirements:
1. `Money(amount, currency)` stores `amount` as an integer number of **cents** and `currency` as an upper-case string (`"usd"` -> `"USD"`). Raise `ValueError` if the amount is negative or the currency is empty.
2. `@classmethod from_decimal(cls, value: float, currency: str)` builds a `Money` from e.g. `12.34` (hint: avoid float rounding errors with `round`).
3. `__repr__` that looks like `Money(1234, 'USD')`.
4. `__eq__` and `__hash__` so two `Money` objects with the same cents and currency are equal and usable as dict keys / set members. Return `NotImplemented` for non-`Money` comparisons.
5. `__str__` that prints `12.34 USD`.
6. `@staticmethod is_valid_currency(code: str) -> bool` returning True for exactly 3 letters.
7. Bonus: make instances effectively immutable (think: `__slots__` or properties without setters).

At the bottom, add a short `if __name__ == "__main__":` block demonstrating each feature with `print`.
