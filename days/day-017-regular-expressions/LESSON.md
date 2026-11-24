# Day 017: Regular expressions with `re` (~5 min read)

As an SDET you parse logs, scrape IDs out of responses and validate formats all the time. `str.split` and `in` cover the easy cases. When the shape of the text matters ("a timestamp, then a level, then a message"), reach for `re`. The trick is to keep patterns readable and to pick the right function.

## 1. Pick the right function
| Function | Returns | Use when |
|---|---|---|
| `re.fullmatch(p, s)` | `Match` or `None` | **validation**: the whole string must fit |
| `re.match(p, s)` | `Match` or `None` | the pattern must start at position 0 (rarely what you want) |
| `re.search(p, s)` | first `Match` or `None` | find one occurrence anywhere |
| `re.findall(p, s)` | `list[str]` or `list[tuple]` | quick extraction (shape depends on the groups!) |
| `re.finditer(p, s)` | iterator of `Match` | extraction with positions/named groups, large input |
| `re.sub(p, repl, s)` | `str` | replace; `repl` can be a function |

```python
import re

re.match(r"\d+", "id 42")       # None: match only looks at position 0
re.search(r"\d+", "id 42")[0]   # '42'
re.fullmatch(r"\d+", "42abc")   # None: good for validation
```

Always use raw strings (`r"..."`). Without them `"\b"` is a backspace character, not a word boundary.

## 2. Groups: plain, named, non-capturing
```python
LINE = re.compile(
    r"""
    (?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})  # ISO timestamp
    \s+
    (?P<level>DEBUG|INFO|WARN|ERROR)
    \s+
    \[(?P<service>[\w-]+)\]                        # [auth-api]
    \s+
    (?P<msg>.*)
    """,
    re.VERBOSE,
)

m = LINE.fullmatch("2026-11-24T08:01:02 ERROR [auth-api] token expired")
m["level"], m["service"]   # ('ERROR', 'auth-api')
m.groupdict()              # {'ts': ..., 'level': 'ERROR', 'service': 'auth-api', 'msg': 'token expired'}
```

- `(?P<name>...)` gives a named group: `m["name"]`, `m.groupdict()`. Prefer it over `m.group(3)`.
- `(?:...)` groups without capturing. Use it for alternation like `(?:GET|POST)` when you don't need the value.
- `re.VERBOSE` lets you split a pattern over lines with comments. Whitespace in the pattern is then ignored, so write a literal space as `\ ` or `[ ]`.
- `re.compile` at module level names the pattern and skips re-parsing it. (`re` caches recent patterns anyway, so this is mostly about readability.)

## 3. `sub` with a function
```python
def mask(m: re.Match[str]) -> str:
    return m["user"][0] + "***@" + m["domain"]

re.sub(r"(?P<user>[\w.]+)@(?P<domain>[\w.-]+)", mask, "mail bob.smith@acme.io now")
# 'mail b***@acme.io now'
```
Backreferences in a string replacement work too: `re.sub(r"(\w+) (\w+)", r"\2 \1", "hello world")` gives `'world hello'`.

## Common pitfalls
- **Greedy by default.** `<.+>` on `"<a><b>"` matches the whole string. Use the lazy `<.+?>` or, better, a negated class `<[^>]+>`.
- **`findall` changes shape with groups.** No groups gives `list[str]` of whole matches; one group gives just that group; several give tuples. Need the whole match plus groups? Use `finditer`.
- **`.` doesn't match `\n`** unless you pass `re.DOTALL`. `^`/`$` anchor to the whole string unless you pass `re.MULTILINE`.
- **`$` matches before a trailing `\n`**: `re.match(r"\d+$", "42\n")` succeeds. For strict validation, use `fullmatch` (or `\Z`).
- **`\d` and `\w` match Unicode** (`"٣"` is a digit). Use `[0-9]` or pass `re.ASCII` when you mean ASCII.
- **Escape user input** with `re.escape(s)` before putting it in a pattern.
- **Don't regex everything.** Use `json`, `urllib.parse`, `ipaddress` or `datetime.fromisoformat` when a real parser exists.
