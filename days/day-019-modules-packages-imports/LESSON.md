# Day 019: Modules, packages & imports (~5 min read)

Every test framework, helper library and CLI you write grows past one file. How Python finds and loads code decides whether `import mylib` works from CI, from your IDE, and from `python -m`. Most "works on my machine" import bugs come from not knowing three things: **what a package is, where `sys.path` starts, and how relative imports resolve.**

## 1. Modules, packages, and what `import` does
- A **module** is a `.py` file. A **package** is a directory with an `__init__.py` (it can hold modules and sub-packages).
- `import x` looks for `x` along `sys.path`, runs its top-level code **once**, and caches it in `sys.modules`. Importing it again just returns the cached object.
- `sys.path[0]` is the directory of the script you ran (`python path/to/script.py`), or the **current directory** for `python -m pkg.mod`. That's why the same import can work one way and fail the other.

```text
qa/
├── __init__.py          # runs on "import qa"
├── __main__.py          # runs on "python -m qa"
├── _util.py             # leading underscore = private by convention
└── report.py
```
```python
# qa/report.py
from ._util import pct          # relative: "_util in MY package"
from . import _util             # also fine
from qa._util import pct        # absolute: equally valid, more explicit

# qa/__init__.py: curate the public API
from .report import render
__all__ = ["render"]            # what "from qa import *" exports, and a signal to readers/tools
__version__ = "0.1.0"
```
Relative imports (`.`, `..`) only work **inside a package**. Running `python qa/report.py` makes `report` a top-level script (`__package__` is empty), so `from ._util import pct` fails with `ImportError: attempted relative import with no known parent package`. Run it as `python -m qa.report` instead.

## 2. `__name__` and `python -m`
```python
# qa/__main__.py
import sys
from . import render

def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    print(render(args))
    return 0

if __name__ == "__main__":       # True when executed, False when imported (e.g. by a test)
    raise SystemExit(main())
```
`python -m qa pass fail` runs `qa/__main__.py` with `__name__ == "__main__"`. Keep the logic in `main(argv)` so it can be called and checked without spawning a process.

## 3. Importing by name: `importlib` and `pkgutil`
Plugin systems (reporters, drivers, fixtures loaded from config) import modules whose names you only know at runtime:
```python
import importlib, pkgutil

mod = importlib.import_module("json")                         # same as "import json"
mod = importlib.import_module(".plugins.csv_out", "qa")       # relative: needs the package as anchor
[m.name for m in pkgutil.iter_modules(qa.plugins.__path__)]   # list modules in a package, without importing them
getattr(mod, "export")                                        # fetch a function from the module
```
`import_module` raises `ModuleNotFoundError` (a subclass of `ImportError`) for missing modules. Catch it and turn it into a helpful error that lists what *is* available.

## Common pitfalls
- **Shadowing the stdlib.** A file called `logging.py`, `random.py` or `test.py` next to your script is found before the real module. Never name files after stdlib modules.
- **Circular imports.** `a` imports `b`, `b` imports `a` at top level → one of them sees a half-initialised module (`ImportError: cannot import name ...`). Fix: move shared code to a third module, or import inside the function that needs it.
- **Heavy work at import time.** Top-level code runs on import, so network calls, file reads or `print`s there slow down and pollute every importer (including pytest collection). Put them in functions.
- **`sys.path.append(...)` hacks.** They hide a layout problem. Run with `-m` from the project root, or install the project (`pip install -e .`).
- **`from x import *`** pulls in everything without `__all__` and hides where names come from. Fine in a package's `__init__` with an explicit `__all__`; avoid elsewhere.
- **`import_module` caches.** Editing a module and re-importing in the same process returns the old one. `importlib.reload(mod)` exists, but restarting is usually saner.
