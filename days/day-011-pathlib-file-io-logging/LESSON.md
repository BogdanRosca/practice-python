# Day 011: `pathlib`, file I/O & `logging` (~5 min)

Almost every real script reads files, writes files and needs to say what it is doing. The modern stdlib gives you one object for paths (`Path`), one rule for files (`with open(...)`, always with an explicit `encoding`) and one way to report what happened (`logging`, not `print`).

## 1. `pathlib`: paths are objects, not strings
```python
from pathlib import Path

root = Path("reports")
f = root / "2026" / "nov.csv"           # "/" joins parts, no os.path.join
f.name, f.stem, f.suffix, f.parent      # ('nov.csv', 'nov', '.csv', Path('reports/2026'))
f.with_suffix(".json")                  # Path('reports/2026/nov.json')

f.parent.mkdir(parents=True, exist_ok=True)   # like mkdir -p
f.write_text("day,amount\n2026-11-01,10\n", encoding="utf-8")
f.read_text(encoding="utf-8").splitlines()    # small files: one call
f.exists(), f.is_file(), f.stat().st_size

sorted(root.rglob("*.csv"))             # recursive glob; glob() is one level only
```
- `Path.home()`, `Path.cwd()` and `Path(__file__).resolve().parent` (the folder of the current script) cover most "where am I" questions.
- `rglob`/`iterdir` return **generators** (Day 005). Wrap them in `sorted()` if order matters, because filesystem order is not guaranteed.

## 2. File I/O: `with`, encodings and streaming
```python
import csv, json

with f.open(encoding="utf-8", newline="") as fh:     # newline="" is required by csv
    rows = list(csv.DictReader(fh))                    # [{'day': '2026-11-01', 'amount': '10'}]

out = f.with_suffix(".json")
with out.open("w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=2)

with f.open(encoding="utf-8") as fh:                  # big file? iterate, don't read()
    for lineno, line in enumerate(fh, start=1):
        ...                                            # one line in memory at a time
```
- **Always pass `encoding="utf-8"`.** The default depends on the OS (on Windows it is often cp1252), so the same script behaves differently on a colleague's machine.
- Modes: `"r"` read, `"w"` truncate+write, `"a"` append, `"x"` create but fail if the file exists. Add `"b"` for bytes.
- Every value from `csv` is a **string**. Convert explicitly (`Decimal(row["amount"])`).
- **Atomic write pattern:** write to `tmp = target.with_suffix(".tmp")`, then `tmp.replace(target)`. Readers never see a half-written file.

## 3. `logging`: `print` for grown-ups
```python
import logging

log = logging.getLogger(__name__)        # one logger per module, named after it

def load(path: Path) -> int:
    log.debug("opening %s", path)        # %-style args: only formatted if emitted
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except FileNotFoundError:
        log.exception("cannot read %s", path)   # ERROR level + traceback
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
```
- Levels, from lowest to highest: `DEBUG < INFO < WARNING < ERROR < CRITICAL`. Without configuration, only WARNING and above are shown.
- **Libraries/modules only call `getLogger(__name__)`. Only the entry point (`__main__`) calls `basicConfig`.** Configuring logging inside an imported module takes that choice away from the application that imports it.
- Write `log.info("x=%s", x)`, not `log.info(f"x={x}")`. With `%s` args, the string is only built if the message is actually emitted, and log aggregators can group messages by their template.
- In tests, pytest's built-in `caplog` fixture captures log records, so you can assert on them.

## Pitfalls
| Pitfall | Fix |
|---------|-----|
| `"dir" + "/" + name` | `Path("dir") / name` |
| `open(p)` without encoding | `open(p, encoding="utf-8")` |
| `fh.read()` on a 5 GB log | `for line in fh:` |
| `print` for diagnostics | `log = logging.getLogger(__name__)` |
| `basicConfig` in a library module | Only in `if __name__ == "__main__":` |
| `except Exception: log.error(e)` | `log.exception("context")` keeps the traceback |
