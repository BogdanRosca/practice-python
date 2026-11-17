# Day 008: Exceptions & Custom Exception Hierarchies (~5 min)

So far your `Money`/`Wallet` raise bare `ValueError`s. Callers can't tell "wrong currency" from "wallet full" without parsing the message, and that is fragile. A small **exception hierarchy** makes errors part of your API: callers catch exactly what they can handle, and the exception carries the data they need.

## 1. Design a hierarchy: one base, specific leaves, data as attributes
```python
class WalletError(Exception):
    """Base for everything this module raises: `except WalletError` catches all of it."""

class CurrencyMismatchError(WalletError, ValueError):   # still a ValueError for old callers
    def __init__(self, left: str, right: str) -> None:
        super().__init__(f"cannot combine {left} with {right}")
        self.left, self.right = left, right

class WalletFullError(WalletError):
    def __init__(self, limit: int) -> None:
        super().__init__(f"wallet is full ({limit} items)")
        self.limit = limit

try:
    raise CurrencyMismatchError("USD", "EUR")
except WalletError as e:
    print(type(e).__name__, e, e.left)     # CurrencyMismatchError cannot combine USD with EUR USD
```
- Inherit from `Exception`, **never** `BaseException` (that's for `KeyboardInterrupt`/`SystemExit`).
- Mixing in a builtin (`ValueError`, `LookupError`) keeps existing `except ValueError` callers working. That's the MRO from Day 003 at work.
- Call `super().__init__(message)` so `str(e)` and tracebacks show the message.

## 2. `try / except / else / finally` and chaining
```python
from decimal import Decimal, InvalidOperation

def parse_amount(raw: str) -> Decimal:
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise ValueError(f"not a number: {raw!r}") from exc   # keeps the cause
    else:
        return value          # runs only if no exception: keeps the try block minimal
    finally:
        print("parsed", raw)  # always runs
```
- `raise New(...) from exc` sets `__cause__`, and the traceback says *"The above exception was the direct cause..."*.
- Raising inside `except` **without** `from` still chains implicitly (*"During handling... another exception occurred"*), which looks like a bug in your handler.
- `raise New(...) from None` hides the cause when it's pure noise (e.g. translating a `KeyError` from a dict lookup).
- A bare `raise` re-raises the current exception with its original traceback.

## 3. Python 3.11+: notes and groups
```python
try:
    Decimal("abc")
except InvalidOperation as e:
    e.add_note("while importing row 17 of expenses.csv")   # extra context, shown in traceback
    raise

errors = [ValueError("bad amount"), KeyError("currency")]
try:
    raise ExceptionGroup("import failed", errors)            # report many failures at once
except* ValueError as eg:                                    # matches the ValueErrors only
    print("values:", eg.exceptions)
except* KeyError as eg:
    print("keys:", eg.exceptions)
```
Use `ExceptionGroup` when you validate a batch and want *all* errors, not just the first.

## Pitfalls
- `except Exception: pass` (or logging and continuing) silently corrupts state. Catch the narrowest type you can actually handle.
- Huge `try` blocks: you end up catching errors from lines you didn't mean to guard. Put the follow-up code in `else`.
- An exception per call site (`AddFailedError`, `AddFailedAgainError`). Model *what went wrong*, not *where*.
- Overriding `__init__` with extra args but not calling `super().__init__(msg)`: `str(e)` becomes `''` and pickling/copying can break.
- Using exceptions for normal control flow in hot loops is fine in Python (EAFP: `try: d[k] except KeyError`), but using them to *return values* is not.
