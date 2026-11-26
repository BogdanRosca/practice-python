# Assignment 019: A tiny test-report package (~15 min)

Build a small package `qa_report/` **in this folder**, plus a `solution.py` next to it that checks it. Standard library only, type-hint everything. Run every command from this folder (`days/day-019-modules-packages-imports/`).

```text
day-019-modules-packages-imports/
├── solution.py
└── qa_report/
    ├── __init__.py
    ├── __main__.py
    ├── _format.py
    ├── summary.py
    └── exporters/
        ├── __init__.py
        ├── text.py
        └── csv.py      # yes, the same name as the stdlib module. See Part 2, step 6
```

**Part 1: The package (~8 min)**

1. `qa_report/_format.py`: `pct(part: int, whole: int) -> str` gives `"66.7%"` (one decimal), and `"0.0%"` when `whole` is 0.
2. `qa_report/summary.py`: `summarise(outcomes: list[str]) -> dict[str, int]` counts `"pass"`, `"fail"` and `"skip"`. The result always has all three keys, in that order. Raise `ValueError` naming the bad value for anything else. Use a **relative** import of `pct` and add `pass_rate(outcomes: list[str]) -> str` (passes / all outcomes).
3. `qa_report/__init__.py`: re-export `summarise` and `pass_rate`, set `__all__` to those two names, and `__version__ = "0.1.0"`. Do **not** re-export `pct`.
4. `qa_report/__main__.py`: a `main(argv: list[str] | None = None) -> int` that prints e.g. `pass=2 fail=1 skip=0 (66.7%)` for the outcomes given on the command line, and returns `0` if nothing failed, `1` otherwise. `python -m qa_report pass fail pass` must print that line and exit with code 1. A bad outcome should print the error to stderr and return `2`.

**Part 2: Exporters loaded by name (~7 min)**

5. Each module in `qa_report/exporters/` defines `export(summary: dict[str, int]) -> str`:
   - `text.py` → `"pass: 2\nfail: 1\nskip: 0"`
   - `csv.py` → `"pass,fail,skip\n2,1,0"`, built with the **standard library** `csv` module (`csv.writer` on an `io.StringIO`, with `lineterminator="\n"`).
6. Inside `exporters/csv.py`, `import csv` must give you the stdlib module, not the file itself. Check it works, then add a comment explaining **why** it does (hint: absolute imports and `sys.path`), and when the same file name *would* shadow the stdlib.
7. In `qa_report/exporters/__init__.py`, write:
   - `available() -> list[str]`: sorted exporter names, found with `pkgutil.iter_modules(__path__)` (no hard-coded list).
   - `get_exporter(name: str) -> Callable[[dict[str, int]], str]`: loads the module with `importlib.import_module` (relative to this package) and returns its `export`. For an unknown name, raise `LookupError` whose message lists the available names. Make sure a name like `"..summary"` or `"text.foo"` can't sneak through either.
8. In `solution.py`, under `if __name__ == "__main__":`, `assert`:
   - `summarise(["pass", "fail", "pass"]) == {"pass": 2, "fail": 1, "skip": 0}` and `pass_rate([]) == "0.0%"`.
   - `qa_report.__all__` doesn't contain `"pct"`, and `from qa_report import *` in a fresh namespace (`exec("from qa_report import *", ns := {})`) gives you `summarise` but not `pct`.
   - `available() == ["csv", "text"]`, and both exporters produce the strings from step 5.
   - `get_exporter("xml")` raises `LookupError` with `"csv"` in its message.
   - `main(["pass", "skip"]) == 0`, `main(["pass", "fail"]) == 1`, `main(["oops"]) == 2`.

**Bonus:**
- Run `python qa_report/__main__.py pass` (not `-m`). Paste the error into a comment in `solution.py` and explain it in one sentence.
- Make `import qa_report` cheap: `exporters` should not be imported until someone uses it. Prove it with `sys.modules` in an assert (start a fresh interpreter with `subprocess.run([sys.executable, "-c", ...])`).
