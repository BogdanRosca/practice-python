# Day 018: `datetime` & time zones (~5 min read)

Timestamps show up everywhere in test work: log lines, API payloads, "the job runs nightly at 02:00", "the token expires in 15 minutes". Most time bugs come from mixing **naive** and **aware** datetimes, or from doing calendar maths in local time across a DST change. The rule that prevents almost all of them is: **parse into aware datetimes, store and compute in UTC, convert to local time only for display or for "wall clock" rules.**

## 1. Naive vs aware
```python
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo          # stdlib since 3.9, uses the IANA tz database

naive = datetime(2026, 11, 25, 9, 0)                                # tzinfo is None
aware = datetime(2026, 11, 25, 9, 0, tzinfo=ZoneInfo("Europe/Bucharest"))
aware.utcoffset()                       # timedelta(seconds=7200)
naive < aware                           # TypeError: can't compare offset-naive and offset-aware

datetime.now(timezone.utc)              # aware "now". Never use datetime.utcnow(): it returns a NAIVE value
aware.astimezone(timezone.utc)          # 2026-11-25 07:00:00+00:00: same instant, different view
aware.astimezone(ZoneInfo("America/New_York"))   # 2026-11-25 02:00:00-05:00
naive.replace(tzinfo=ZoneInfo("Europe/Bucharest"))  # *attach* a zone (no conversion)
```
`astimezone` **converts** (same instant, new wall time). `replace(tzinfo=...)` **labels** (same wall time, a different instant). Use `replace` only on naive values whose zone you know.

## 2. Parsing and formatting
```python
datetime.fromisoformat("2026-11-25T09:00:00+02:00")   # aware
datetime.fromisoformat("2026-11-25T07:00:00Z")        # aware UTC ('Z' accepted since 3.11)
datetime.strptime("25/11/2026 09:00", "%d/%m/%Y %H:%M")  # NAIVE: the string has no zone

aware.isoformat(timespec="seconds")     # '2026-11-25T09:00:00+02:00': use this on the wire
aware.strftime("%a %d %b %H:%M %Z")     # 'Wed 25 Nov 09:00 EET': for humans
```
Prefer `fromisoformat` for ISO 8601. Use `strptime` for anything else, and decide straight away which zone a naive result belongs to.

## 3. Arithmetic and DST
`timedelta` is a fixed duration. Adding one to an aware datetime in a real zone does **wall clock** maths: the time of day stays the same, and the offset is recalculated.
```python
tz = ZoneInfo("Europe/Bucharest")       # DST starts 2026-03-29 03:00 -> 04:00
sat = datetime(2026, 3, 28, 12, 0, tzinfo=tz)
sun = sat + timedelta(days=1)           # 2026-03-29 12:00+03:00: "same time tomorrow"
sun - sat                               # 1 day, 0:00:00   <- wall clock difference!
sun.astimezone(timezone.utc) - sat.astimezone(timezone.utc)   # 23:00:00 <- real elapsed time

d = timedelta(hours=26, minutes=30)
d.days, d.seconds                       # (1, 9000): .seconds is NOT the total
d.total_seconds()                       # 95400.0: use this
```
- "Run every day at 02:00 local" is a **wall clock** rule, so compute it in the local zone.
- "Timeout after 15 minutes", "how long did the test take" are **elapsed** durations, so compute them in UTC.

## Common pitfalls
- **`datetime.utcnow()` / `utcfromtimestamp()`** return naive values and are deprecated in 3.12. Use `datetime.now(timezone.utc)` and `fromtimestamp(ts, timezone.utc)`.
- **Subtracting two datetimes in the same `ZoneInfo`** ignores the DST jump (see above). Convert to UTC first when you mean elapsed time.
- **Non-existent and ambiguous local times.** `03:30` on 29 March doesn't exist in Bucharest, and `03:30` on 25 October happens twice (`fold=0` is the first, `fold=1` the second). `ZoneInfo` won't raise. It quietly picks an offset, so validate if it matters.
- **`timedelta.seconds`** is only the remainder after whole days. Use `total_seconds()`.
- **Hard-coded offsets** (`timezone(timedelta(hours=2))`) don't know about DST. Use `ZoneInfo("Europe/Bucharest")` for real places, and keep `timezone.utc` for UTC.
- **Calling `datetime.now()` inside logic** makes code untestable. Pass `now` in as a parameter (clock injection). You'll do exactly that in today's assignment.
