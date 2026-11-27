# Assignment 020: Generic test-utility toolkit (~15 min)

Write everything in `solution.py` in this folder. Standard library only (plus `mypy` to check it: `pip install mypy`). Your goal is code that **runs** and also passes:

```bash
mypy --strict --warn-unused-ignores solution.py
```

No `Any` in your public signatures, except inside the `SupportsLessThan` protocol.

**Part 1: Generic functions & classes (~6 min)**

1. `first(items: Iterable[T], default: D) -> T | D`: the first item, or `default` if `items` is empty. Must work with generators.
2. `Stack(Generic[T])`:
   - `__init__(self, items: Iterable[T] = ())`, `push(item: T) -> None`, `pop() -> T`, `peek() -> T | None`, `__len__`, and a `__repr__` like `Stack([1, 2])`.
   - `pop()` on an empty stack raises `IndexError("pop from empty Stack")`.
3. `largest(items: Iterable[CT]) -> CT`, where `CT` is bound to a `SupportsLessThan` Protocol you define. Don't call the built-in `max`. An empty input raises `ValueError`.

**Part 2: A signature-preserving decorator (~5 min)**

4. `retry(times: int, exceptions: tuple[type[Exception], ...] = (Exception,))`, a decorator factory typed with `ParamSpec`:
   - It calls the function up to `times` times while it raises one of `exceptions`, then re-raises the last error.
   - Any other exception is raised immediately, with no retry.
   - `times < 1` raises `ValueError` when the decorator is created.
   - Use `functools.wraps`, so `__name__` is kept.

**Part 3: Prove the types (~4 min)**

5. Write `_type_errors() -> None`, which must **never be called**. Put these three lines in it, each ending with `# type: ignore[<code>]` (use the error code mypy gives you):
   - pushing a `str` onto a `Stack[int]`
   - `largest([object(), object()])`
   - calling a `@retry(3)`-decorated `add(a: int, b: int) -> int` as `add(1, "2")`

   Because of `--warn-unused-ignores`, mypy only passes if all three lines really are type errors. If your typing were too loose (for example `Callable[..., Any]`), mypy would report an unused ignore.
6. Under `if __name__ == "__main__":`, `assert`:
   - Stack: push, pop, peek, `len`, `peek()` returning `None` when empty, and `IndexError` from an empty `pop()`.
   - `first([], 0) == 0`, `first(iter([5]), -1) == 5`, and `largest(["b", "c", "a"]) == "c"`.
   - A function decorated with `@retry(3, (ConnectionError,))` that fails twice and then succeeds returns its value after exactly 3 calls.
   - A `KeyError` is not retried.
   - `flaky.__name__ == "flaky"`.

**Bonus:**
- Add `setting(key: str)` / `setting(key: str, default: D)` with `@overload`, reading from a module-level `dict[str, str]`, so that `setting("X")` is `str | None` and `setting("X", 0)` is `str | int`. Check both with `reveal_type` (remove those calls once you've seen the output).
- Rewrite `Stack` and `first` in PEP 695 syntax (`class Stack[T]:`), if you have Python 3.12+. Which `TypeVar` declarations can you delete?
