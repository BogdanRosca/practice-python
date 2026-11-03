class Money:
    def __init__(self, amount, currency):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        if currency == "":
            raise ValueError("Currency was not provided")
        self.amount = int(amount)
        self.currency = currency.upper()

    @classmethod
    def from_decimal(cls, value: float, currency: str):
        return cls(amount= round(value * 100), currency=currency)

    def __repr__(self):
        return f"Money({self.amount!r}, {self.currency!r})"

    def __str__(self):
        return f"{self.amount / 100:.2f} {self.currency}"

    def __eq__(self, other):
       if not isinstance(other, Money): return NotImplemented
       return self.amount == other.amount and self.currency == other.currency

    def __hash__(self):
        return hash((self.amount, self.currency)) 

    @staticmethod
    def is_valid_currency(code: str)-> bool:
        return len(code) == 3 and code.isalpha()


if __name__ == "__main__":
    m1 = Money(1234, "usd")
    m2 = Money.from_decimal(12.34, "USD")
    print(repr(m1), str(m1))
    print(m1 == m2, m1 == 5)
    print({m1, m2}, {m1: "price"}[m2])
    print(Money.is_valid_currency("eur"), Money.is_valid_currency("12!"))
    try:
        Money(-1, "usd")
    except ValueError as e:
        print("ValueError:", e)