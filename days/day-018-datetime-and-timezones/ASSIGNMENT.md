# Assignment 018: Test-run timing & the nightly scheduler (~15 min)

Create `solution.py` in this folder, push it to this branch, and merge the PR. Use only the standard library (`datetime`, `zoneinfo`), and type-hint everything. Define `LOCAL = ZoneInfo("Europe/Bucharest")` at module level.

**Part 1: Normalise timestamps (~6 min)**

Your test runners report times in three formats:
```text
2026-11-25T07:59:58Z            # CI runner, UTC
2026-11-25T10:00:03+02:00       # API, with offset
25/11/2026 10:01:15             # legacy runner, local Bucharest time, no zone
```
1. Write `to_utc(stamp: str) -> datetime` that returns an **aware datetime in UTC** for all three formats. Try `fromisoformat` first. If that fails, fall back to `strptime` and attach `LOCAL`. Raise `ValueError` with a clear message if neither works.
2. Write `elapsed(start: str, end: str) -> timedelta`, the real time between two stamps in any of the formats above. Raise `ValueError` if `end` is before `start`.
3. Write `fmt_duration(d: timedelta) -> str` that gives `"1h 02m 05s"`, or `"2m 05s"` / `"5s"` when the leading parts are zero. Round to whole seconds. (Remember the `.seconds` trap.)

**Part 2: The nightly job (~9 min)**

Regression runs nightly at **02:00 Bucharest time**.

4. Write `next_nightly(now: datetime, hour: int = 2) -> datetime`. `now` is any **aware** datetime, in any zone. Return the next run as an aware datetime in `LOCAL`, strictly after `now`. Raise `ValueError` if `now` is naive. Don't call `datetime.now()` inside it.
5. Write `runs_between(start: datetime, end: datetime, hour: int = 2) -> list[datetime]`, all nightly runs in `(start, end]`, built on `next_nightly`.
6. In an `if __name__ == "__main__":` block, `assert`:
   - `to_utc` gives the same instant for `"2026-11-25T08:00:00Z"`, `"2026-11-25T10:00:00+02:00"` and `"25/11/2026 10:00:00"`.
   - `fmt_duration(elapsed("2026-11-25T07:59:58Z", "25/11/2026 10:01:15")) == "1m 17s"`.
   - `next_nightly(datetime(2026, 11, 25, 1, 0, tzinfo=timezone.utc))` is 26 Nov 02:00 local (01:00 UTC is already 03:00 in Bucharest).
   - Across the spring DST change (`2026-03-29`, 03:00 -> 04:00), the runs on 28, 29 and 30 March are all at 02:00 local, but the **real** gap between the 29th and the 30th run is 23 hours. Assert both: the local `.hour` of every run and the UTC difference. Add a comment saying which gap stays 24h and why.

**Bonus:**
- An overnight run starts at `2026-10-24T23:30:00Z` and ends at `2026-10-25T01:30:00Z`. Print its duration and the start and end in local time. Explain in a comment why local end minus local start "looks" wrong but `elapsed` is right (autumn DST change, `fold`).
- Make `hour` accept `datetime.time` too (e.g. `time(2, 30)`), without breaking existing calls.
