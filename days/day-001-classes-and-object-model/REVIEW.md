# Review: Day 001 - Classes & the object model

**Tests:** none (assignment is self-checked via the `__main__` demo). I ran your demo and extra probes by hand.

## Done well
- All 6 required features work; `__repr__`/`__str__` match the spec exactly.
- `__eq__` returns `NotImplemented` for non-`Money` (the correct protocol, not `False`), and `__hash__` uses the same fields as `__eq__`.
- `from_decimal` as a `@classmethod` using `cls(...)` so subclasses work; `is_valid_currency` correctly a `@staticmethod`.

## Improvements
1. **Mutable + hashable = trap.** `m = Money(1,'usd'); s = {m}; m.amount = 2; m in s` -> `False`. The bonus (immutability) fixes this; Day 002 covers exactly how (properties / `__slots__`).
2. **Validation gaps.** `Money(5, ' ')` is accepted (whitespace isn't "empty"), `Money(12.9, 'usd')` silently truncates to 12 cents, and `is_valid_currency` isn't used by the constructor. Validate with `currency.strip()` / `is_valid_currency`, and reject non-integers instead of `int()`-ing them.
3. **Float rounding in `from_decimal`.** `round(value * 100)` gives `1.005 -> 1.00`. Safer: `Decimal(str(value))`.

```python
from decimal import Decimal, ROUND_HALF_UP

@classmethod
def from_decimal(cls, value, currency):
    cents = (Decimal(str(value)) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return cls(int(cents), currency)
```

Also style: PEP 8 spacing (`amount=round(...)`, 4-space indents in `__eq__`, trailing whitespace).
