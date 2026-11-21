# Assignment 011: A tiny log-file analyser (~15 min)

Create `solution.py` in this folder, push it to this branch, and merge the PR. **Rules of the day:** no `os.path`, no string-concatenated paths, no `print` except in the final demo, and every `open`/`read_text`/`write_text` passes `encoding="utf-8"`. Type-hint everything.

**Setup:** `make_sample(dir: Path) -> None` creates `dir/logs/app-1.log`, `dir/logs/sub/app-2.log` and `dir/logs/notes.txt` (the last one is a decoy). Each `.log` file has a few lines in this format:
```
2026-11-18 09:00:01 INFO  user=alice action=login
2026-11-18 09:00:07 ERROR user=bob action=pay msg=card declined
this line is garbage
```

**Part 1: `pathlib`**
1. `find_logs(root: Path) -> list[Path]`: all `*.log` files under `root`, recursively, sorted.

**Part 2: file I/O**
1. `parse_file(path: Path) -> Iterator[dict[str, str]]`: a **generator** that streams the file line by line (no `read()`/`readlines()`) and yields `{"ts": ..., "level": ..., "user": ..., "action": ...}` for each valid line. Hint: `line.split(maxsplit=3)` and then split the `key=value` pairs.
2. Malformed lines are skipped and logged with `log.warning("%s:%d malformed line", path.name, lineno)`.
3. `write_summary(records, target: Path) -> None`: writes `{"total": N, "by_level": {...}, "errors_by_user": {...}}` as JSON (`Counter` from Day 010 is welcome). Use the **atomic write** pattern: write to a temporary file, then `replace()`.

**Part 3: `logging`**
1. A module-level `log = logging.getLogger(__name__)`. `find_logs` logs at DEBUG how many files it found, and `write_summary` logs at INFO where it wrote the summary.
2. In `__main__`: `basicConfig(level=logging.INFO, format=...)`, then build a sample in a `tempfile.TemporaryDirectory()`, parse every log, write `summary.json` next to the logs, and print the JSON. Run it once at `INFO` and once at `DEBUG`, and notice what changes.

**Bonus:** wrap `parse_file` so that a missing file is logged with `log.exception(...)` and re-raised. In a comment, explain the difference between `log.error(e)` and `log.exception("...")`. Finally, write one pytest test for Part 2 using the `tmp_path` and `caplog` fixtures that asserts the malformed line produced a WARNING.
