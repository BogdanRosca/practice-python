# Assignment 009: Pluggable payment & export for `Wallet` (~15 min)

Create `solution.py` in this folder, push to this branch, merge the PR. Reuse a minimal frozen `Money(amount: Decimal, currency: str)` and a `Wallet` holding `items: list[Money]` (copy them from earlier days). Type-hint everything.

**Part 1 - ABC**
1. `class PaymentMethod(ABC)` with an abstract `charge(self, amount: Money) -> str` and an abstract **property** `name -> str`.
2. A concrete method `pay_all(self, wallet: Wallet) -> list[str]` that charges every item (a template method that uses the abstract `charge`).
3. Two subclasses: `Card(last4: str)` and `BankTransfer(iban: str)`. Demo: `PaymentMethod()` raises `TypeError`. A subclass missing `name` also raises `TypeError` (catch it and print the message).

**Part 2 - Protocol**
1. `@runtime_checkable class Exporter(Protocol)` with `def export(self, items: Sequence[Money]) -> str: ...`.
2. Two **unrelated** classes, neither inheriting from `Exporter`: `CsvExporter` (`"amount,currency\n10,USD\n..."`) and `JsonExporter` (use `json.dumps`, amounts as strings).
3. `def export_wallet(wallet: Wallet, exporter: Exporter) -> str`. Demo both, and print `isinstance(CsvExporter(), Exporter)`.
4. Show the pitfall: a class with `export = "nope"` still passes `isinstance(..., Exporter)`. Explain in a comment why.

**Part 3 - `collections.abc`**
Make `Wallet` subclass `collections.abc.Sequence` by implementing only `__getitem__` and `__len__`. Demo `in`, `.index()`, `.count()`, `reversed()` and slicing (`wallet[1:]`), without writing those methods yourself.

Bonus: a `FakePayment` test double that satisfies a `Chargeable` Protocol (defined by you) **without** inheriting from `PaymentMethod`, and records every call in a `calls: list[Money]`. In a comment, say which one (ABC or Protocol) you'd pick for the payment API of a real service, and why.

End with an `if __name__ == "__main__":` demo printing each behaviour.
