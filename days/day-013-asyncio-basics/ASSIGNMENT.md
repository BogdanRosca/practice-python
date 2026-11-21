# Assignment 013: An async "crawler" with limits, timeouts & retries (~15 min)

Create `solution.py` in this folder, push it to this branch, and merge the PR. Standard library only, everything type-hinted. Fake the network with `asyncio.sleep`, because no real HTTP is needed.

**Setup (given; copy it in):**
```python
import asyncio, random

class FetchError(Exception): ...

async def fake_fetch(url: str) -> str:
    """Simulates a request: 0.05–0.3s latency, ~20% transient failures, 'slow' URLs hang."""
    if "slow" in url:
        await asyncio.sleep(10)
    await asyncio.sleep(random.uniform(0.05, 0.3))
    if random.random() < 0.2:
        raise FetchError(f"transient failure for {url}")
    return f"<html>{url}</html>"
```

**Part 1: sequential vs concurrent (~3 min)**
1. `async def fetch_all_sequential(urls: list[str]) -> list[str]` and `async def fetch_all_concurrent(urls: list[str]) -> list[str]` (use `gather`). Use `random.seed(0)` and 10 non-slow URLs, and print the elapsed time of each with `time.perf_counter()`. Results must stay in **input order**.
2. In one comment: why does `gather` preserve order even though requests finish in a different order?

**Part 2: a robust `fetch` (~6 min)**
Write `async def fetch_with_retry(url: str, *, retries: int = 3, timeout: float = 1.0, backoff: float = 0.05) -> str`:
1. Each attempt is wrapped in a timeout (`asyncio.timeout` or `wait_for`).
2. On `FetchError` **or** `TimeoutError`, retry up to `retries` total attempts, sleeping `backoff * 2**attempt` between them (exponential backoff).
3. After the last failure raise `FetchError(f"{url} failed after {retries} attempts")` **chained** (`raise ... from last_exc`), as in Day 008.
4. Do **not** catch `asyncio.CancelledError` (think about why).

**Part 3: bounded crawler (~6 min)**
Write `async def crawl(urls: list[str], *, max_concurrency: int = 3) -> dict[str, str | Exception]`:
1. At most `max_concurrency` fetches in flight at once (`asyncio.Semaphore`). **Prove it**: track a `current`/`peak` in-flight counter and assert `peak <= max_concurrency` at the end.
2. One failing URL must not kill the others: either `gather(..., return_exceptions=True)` or catch per task. The result maps each URL to its HTML **or** the exception.
3. Demo with ~12 URLs including one `"https://example.com/slow"`: print a summary such as `11 ok, 1 failed, peak=3, 3.2s` (the slow URL should fail via timeouts, not hang the run).

**Bonus:**
- Rewrite `crawl` as a producer/consumer with `asyncio.Queue` and exactly `max_concurrency` worker tasks, shut down cleanly (`await q.join()`, then cancel the workers).
- Print results in **completion order** as they arrive using `asyncio.as_completed`.
- Add a 4-line demo showing that `time.sleep(0.5)` inside one coroutine delays *all* the others, then fix it with `asyncio.to_thread`.

End with an `if __name__ == "__main__":` that runs every part via `asyncio.run(main())`.
