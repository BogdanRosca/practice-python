# Assignment 017: A tiny test-log analyser (~15 min)

Create `solution.py` in this folder, push it to this branch, and merge the PR. Use only the standard library, and type-hint everything.

You get the raw output of a test run like this one. Paste it into `solution.py` as a module-level constant `SAMPLE_LOG`:

```text
2026-11-24T08:00:01 INFO  [runner] session start build=1.4.2-rc1
2026-11-24T08:00:03 INFO  [auth-api] test_login PASSED (0.84s)
2026-11-24T08:00:05 ERROR [auth-api] test_refresh FAILED (2.10s) user=alice@example.com
2026-11-24T08:00:06 WARN  [cart] retrying request id=REQ-00042
2026-11-24T08:00:09 INFO  [cart] test_add_item PASSED (1.05s)
garbage line that should be ignored
2026-11-24T08:00:12 ERROR [cart] test_checkout FAILED (3.50s) user=bob.smith@acme.io
2026-11-24T08:00:13 INFO  [cart] test_empty_cart SKIPPED (0.00s)
2026-11-24T08:00:15 INFO  [runner] session end
```

**Part 1: Parse (~8 min)**
1. Write a module-level compiled pattern `LINE_RE` with **named groups** `ts`, `level`, `service`, `msg`. Use `re.VERBOSE` with a comment per part. Levels are `DEBUG|INFO|WARN|ERROR`, and the amount of spaces after the level varies.
2. Write a frozen dataclass `TestResult(service: str, name: str, outcome: str, seconds: float)`.
3. Write `parse_results(log: str) -> list[TestResult]`. Use `finditer` or a per-line `fullmatch`, plus a second pattern for the message part: `test_<name> PASSED|FAILED|SKIPPED (<float>s)`. Skip garbage lines and non-test lines silently. On the sample you should get 5 results.
4. Write `slowest(results: list[TestResult], n: int = 3) -> list[TestResult]` and `failures_by_service(results) -> dict[str, list[str]]` (service -> failing test names, in log order).

**Part 2: Scrub & validate (~7 min)**
1. Write `redact(log: str) -> str`. It masks every email as `a***@example.com` (first character of the user, then `***`, domain kept), using `re.sub` with a **function**.
2. Write `is_valid_build(version: str) -> bool` for strings like `1.4.2` or `1.4.2-rc1` (three numeric parts, optional `-rc<N>`). Leading zeros are fine. It must reject `1.4`, `1.4.2-rc`, `1.4.2-beta1`, `"1.4.2\n"` and `" 1.4.2"`. Pick the function from the lesson that makes the `"1.4.2\n"` case come out right, and say in a comment why.
3. In an `if __name__ == "__main__":` block, `assert` your results on `SAMPLE_LOG`: 5 results, 2 failures, the slowest is `test_checkout`, `failures_by_service` equals `{"auth-api": ["test_refresh"], "cart": ["test_checkout"]}`, and no `@` address in `redact(SAMPLE_LOG)` keeps its full user part. Print the redacted log.

**Bonus:**
- Extract the request ids (`REQ-\d+`) with `re.findall`, then change the pattern to `(REQ)-(\d+)` and show in a comment how the return type changes.
- Write `grep(log: str, word: str) -> list[str]`, returning lines containing `word` as a whole word (`\b`). Make sure `grep(log, "c++")` doesn't crash or match wrongly. (Hint: `re.escape`, and think about what `\b` means next to `+`.)
