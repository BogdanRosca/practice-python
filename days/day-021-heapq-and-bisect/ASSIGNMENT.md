# Assignment 021: Test-run scheduler & latency stats (~15 min)

Write everything in `solution.py` in this folder. Standard library only (`heapq`, `bisect`, `itertools`). Don't call `sort`/`sorted` except where a task allows it.

**Part 1: `TestQueue`, a priority queue (~6 min)**

1. `TestQueue` keeps test names with an integer priority. A **lower number runs first**.
   - `push(name: str, priority: int) -> None`
   - `pop() -> str`: returns the next test. **Equal priorities come out in the order they were pushed (FIFO).** An empty queue raises `IndexError("pop from empty TestQueue")`.
   - `peek() -> str | None`: the next test without removing it, `None` if empty.
   - `__len__`
   - Your heap must never compare two names to break a tie (use a counter).

**Part 2: Top-k and merging (~4 min)**

2. `slowest(durations: dict[str, float], k: int) -> list[str]`: the names of the `k` slowest tests, slowest first. Equal durations keep the dict's order. `k <= 0` returns `[]`; `k` larger than the dict returns all of them. Use `heapq.nlargest`.
3. `merge_logs(*logs: list[tuple[float, str]]) -> list[tuple[float, str]]`: each log is already sorted by timestamp; return one list sorted by timestamp. Use `heapq.merge` with `key=`, so equal timestamps keep the order of the logs as passed.

**Part 3: `LatencyStats` with `bisect` (~5 min)**

4. `LatencyStats` keeps a sorted list of latencies in ms.
   - `__init__(self, values: Iterable[float] = ())`: you may sort once here.
   - `add(ms: float) -> None`, using `bisect.insort`.
   - `count_between(lo: float, hi: float) -> int`: the number of values with `lo <= v <= hi` (both ends **inclusive**), in O(log n). `lo > hi` returns `0`.
   - `percentile(p: float) -> float`: **nearest-rank** percentile: the value at 1-based rank `ceil(p / 100 * n)`, with `p == 0` returning the minimum. Raise `ValueError` if there is no data or `p` is not in `0..100`.

5. Under `if __name__ == "__main__":`, `assert`:
   - Pushing `("e2e", 3)`, `("unit_a", 1)`, `("smoke", 2)`, `("unit_b", 1)` pops `unit_a, unit_b, smoke, e2e`; `peek()` on an empty queue is `None`; an empty `pop()` raises `IndexError`.
   - Pushing two tests with the same priority does not raise, even if you change the name type to something non-comparable like a `dict` (try it once).
   - `slowest({"a": 1.0, "b": 5.0, "c": 5.0, "d": 3.0}, 2) == ["b", "c"]`, plus the `k = 0` and `k = 10` cases.
   - `merge_logs([(1, "a"), (4, "a")], [(2, "b"), (4, "b")]) == [(1, "a"), (2, "b"), (4, "a"), (4, "b")]`.
   - For `LatencyStats([12, 15, 15, 20, 31, 48])`: `count_between(15, 31) == 4`, `count_between(16, 19) == 0`, `percentile(50) == 15`, `percentile(90) == 48`, `percentile(0) == 12`; after `add(18)`, `count_between(15, 20) == 4`.

**Bonus:**
- Add `TestQueue.cancel(name)` using **lazy deletion**: don't search the heap; remember the cancelled name and skip it in `pop`/`peek`. Make sure `len()` stays correct.
- Add `LatencyStats.buckets(bounds: list[float]) -> list[int]`, which counts values per bucket using only `bisect` (e.g. bounds `[15, 30]` gives three buckets: `< 15`, `15..30`, `> 30`). Decide which side each boundary belongs to, and say why in a comment.
