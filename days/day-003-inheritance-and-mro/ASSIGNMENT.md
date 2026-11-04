# Assignment 003: Money family + a mixin (~15 min)

Create `solution.py` in this folder, push it to this branch, merge the PR.

Start from your Day 002 `Money` (copy it in; also apply the review fixes: `type(self)(...)` in `with_amount`, `Money.apply(discount)`).

1. **Subclass.** `class TaxedMoney(Money)` with an extra read-only `tax_rate` (float, 0 <= rate <= 1, validate with `ValueError`/`TypeError`). Constructor `TaxedMoney(amount, currency, tax_rate)` must call `super().__init__`. Remember `__slots__` (add only the new slot). Add `total` property: amount plus tax, rounded to int cents (`round`).
2. Override `__repr__` using `super()` or `type(self).__name__` so it prints e.g. `TaxedMoney(1000, 'USD', 0.2)`. Override `__eq__` so a `TaxedMoney` equals another only if `tax_rate` also matches, while `__hash__` stays consistent. Return `NotImplemented` for foreign types.
3. Check that `TaxedMoney(1000,'usd',0.2).with_amount(500)` is a `TaxedMoney` (hint: `with_amount` must be overridden or made generic, since the constructor signature differs).
4. **Mixin.** Write `class JsonMixin` with `to_json(self) -> str` returning `json.dumps` of a dict built from a class attribute `json_fields` (a tuple of attribute names the host class declares). Make `class JsonTaxedMoney(JsonMixin, TaxedMoney)` with `json_fields = ("amount", "currency", "tax_rate")`.
5. Print `JsonTaxedMoney.__mro__` (names only) and explain in a one-line comment why `JsonMixin` is listed before `TaxedMoney`.
6. **Composition.** Write `class Wallet` that *has* a `dict[str, Money]` (one per currency) rather than subclassing `dict`. Methods: `add(money)` (sums into the same currency), `balance(currency) -> Money` (zero `Money` if absent), `__len__`.

Bonus: show the diamond problem: two mixins both defining `describe()` that call `super().describe()`, and print the call order.

End the file with an `if __name__ == "__main__":` demo printing each behaviour (including errors via `try/except`).
