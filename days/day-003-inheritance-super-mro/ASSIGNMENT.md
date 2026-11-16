# Assignment 003: Shapes, a cooperative mixin chain & composition (~15 min)

Create `solution.py` in this folder, push to this branch, merge the PR.

**Part 1 - inheritance.** Write a base `Shape` with `name` (str) and an `area()` method raising `NotImplementedError`. Add `describe()` returning `"<name> with area <area:.2f>"`. Subclass it with `Rectangle(width, height)` and `Circle(radius)` (use `math.pi`), each calling `super().__init__` with its name and overriding `area()`. Add `Square(Rectangle)` taking one `side` and reusing `Rectangle`'s logic via `super()`. Override `describe()` in `Square` to append `" (square)"` using `super().describe()`.

**Part 2 - MRO.** Build this diamond, where each `trace()` returns a list and is **cooperative** (`super().trace()`):
`Base` (returns `["Base"]`), `Left(Base)`, `Right(Base)`, `Bottom(Left, Right)`, each prepending its own name. Print `Bottom().trace()` and `[c.__name__ for c in Bottom.__mro__]`; add a comment explaining why `Base` appears only once.

**Part 3 - mixin.** Write `ComparableByAreaMixin` implementing `__eq__` and `__lt__` using `self.area()` (return `NotImplemented` for objects without `area`), and use `functools.total_ordering` so `<=`, `>`, `>=` work. Create `ComparableRectangle(ComparableByAreaMixin, Rectangle)` and show `sorted([...])` and `max(...)` work. Explain in a comment why the mixin must come *before* `Rectangle`. (Hint: if you define `__eq__`, think about `__hash__`.)

**Part 4 - composition.** Write `class Canvas` that *has* a list of shapes (don't inherit from `list`): `add(shape)` (raise `TypeError` if not a `Shape`), `total_area()`, `largest()` (return `None` if empty) and `__len__`. Add a one-line comment on why this beats `class Canvas(list)`.

Bonus: give `Shape` a `__repr__` that works for all subclasses without each one overriding it (hint: `type(self).__name__` and `vars(self)`).

End with an `if __name__ == "__main__":` demo printing each behaviour (including the errors, via `try/except`).
