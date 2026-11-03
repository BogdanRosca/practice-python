class Bounded:
    def __init__(self, minimum:int , maximum: int):
        self.minimum = minimum
        self.maximum = maximum

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self     
        return getattr(obj, self.name)   

    def __set__(self, obj,value):
        if type(value) is not int:
            raise TypeError(f"Wrong value type. Expected {type(1)} got {type(value)}")
        if value < self.minimum or value > self.maximum:
            raise ValueError("Provided value is out of ranges")
        setattr(obj, self.name, value)

class Discount:
    percent = Bounded(0, 100)


class Money:
    __slots__ = ("_amount", "_currency")

    def __init__(self, amount, currency):
        if type(amount) is not int:
            raise TypeError(f"amount must be int cents, got {type(amount).__name__}")
        if amount < 0:
            raise ValueError("amount cannot be negative")
        if not isinstance(currency, str):
            raise TypeError(f"currency must be str, got {type(currency).__name__}")
        currency = currency.strip()
        if not Money.is_valid_currency(currency):
            raise ValueError(f"invalid currency code: {currency!r}")
        self._amount = amount
        self._currency = currency.upper()

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    @property
    def dollars(self):
        return self._amount / 100

    def with_amount(self, amount):
        return Money(amount, self._currency)

    def __repr__(self):
        return f"Money({self._amount!r}, {self._currency!r})"

    def __str__(self):
        return f"{self._amount / 100:.2f} {self._currency}"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self._amount == other._amount and self._currency == other._currency

    def __hash__(self):
        return hash((self._amount, self._currency))

    @staticmethod
    def is_valid_currency(code: str) -> bool:
        return len(code) == 3 and code.isalpha()


if __name__ == "__main__":
    a, b = Discount(), Discount()
    a.percent, b.percent = 10, 90
    print(a.percent, b.percent)        
    print(Discount.percent)  
    c = Discount()
    d = Discount()
    try: 
        c.percent = 101
    except ValueError as raised_exception:
        print(raised_exception)
    try: 
        d.percent = -1
    except ValueError as raised_exception:
        print(raised_exception)
    e = Discount()
    try: 
        d.percent = "23"
    except TypeError as raised_exception:
        print(raised_exception) 

    # --- Part 2: immutable Money ---
    m = Money(1234, " usd ")
    print(repr(m), str(m), m.dollars)

    # 1. read-only properties
    for attr in ("amount", "currency", "dollars"):
        try:
            setattr(m, attr, 1)
        except AttributeError as err:
            print(f"{attr} is read-only -> AttributeError: {err}")

    # 2. constructor validation
    for bad_args in ((12.9, "usd"), (-1, "usd"), (100, " "), (100, "12!")):
        try:
            Money(*bad_args)
        except (TypeError, ValueError) as err:
            print(f"Money{bad_args!r} -> {type(err).__name__}: {err}")

    # 3. hashing is safe: the object can't change after it's put in a set
    s = {m}
    try:
        m.amount = 1
    except AttributeError:
        pass
    print("still in set:", m in s, "| equal copy in set:", Money(1234, "USD") in s)

    # 5. with_amount returns a new object
    m2 = m.with_amount(500)
    print(m, "->", m2, "| same object?", m is m2)

    # 6. __slots__ blocks new attributes
    try:
        m.foo = 1
    except AttributeError as err:
        print(f"m.foo = 1 -> AttributeError: {err}")
