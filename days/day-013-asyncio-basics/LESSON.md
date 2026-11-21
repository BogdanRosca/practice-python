# Day 013: `asyncio` basics (~5 min)

`asyncio` gives you **concurrency on one thread**: while one task waits for I/O (network, sleep, a subprocess), the event loop runs another. It doesn't make CPU-bound code faster (that's Day 014). What it does do is let one process hold thousands of slow I/O operations open at the same time.

## 1. Coroutines, `await` and the event loop
```python
import asyncio

async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)        # yields control to the loop while "waiting"
    return f"{name} done"

async def main() -> None:
    result = await fetch("a", 0.1)    # runs it and waits: sequential
    print(result)

asyncio.run(main())                   # creates the loop, runs main(), closes the loop
```
Calling `fetch("a", 1)` **does not run anything**. It returns a *coroutine object*. Only `await`, a Task, or `asyncio.run` actually drives it. Forget the `await` and you get `RuntimeWarning: coroutine ... was never awaited`.

## 2. Running things *concurrently*
Two `await`s in a row are still sequential. To overlap them, schedule them as **Tasks**:
```python
import asyncio, time

async def main() -> None:
    t0 = time.perf_counter()
    # gather: run all, return results in *argument order*
    results = await asyncio.gather(fetch("a", 0.3), fetch("b", 0.1), fetch("c", 0.2))
    print(results, f"{time.perf_counter() - t0:.2f}s")   # ['a done', 'b done', 'c done'] 0.30s

    # TaskGroup (3.11+): structured concurrency; if one task fails, the others are cancelled
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch("x", 0.1))
        t2 = tg.create_task(fetch("y", 0.2))
    print(t1.result(), t2.result())

asyncio.run(main())
```
Handy tools:
- `asyncio.as_completed(aws)` gives results in **completion order**.
- `asyncio.gather(..., return_exceptions=True)` puts exceptions in the result list instead of raising the first one.
- `asyncio.wait_for(aw, timeout)` (or `async with asyncio.timeout(s):` on 3.11+) raises `TimeoutError` and **cancels** the inner task.

## 3. Limiting concurrency & sharing state
```python
sem = asyncio.Semaphore(3)            # at most 3 "requests" in flight

async def limited(i: int) -> int:
    async with sem:
        await asyncio.sleep(0.1)
        return i * i

async def main() -> None:
    print(await asyncio.gather(*(limited(i) for i in range(10))))   # ~0.4s, not 0.1s or 1.0s

asyncio.run(main())
```
`asyncio.Queue` is the standard producer/consumer tool: `await q.put(x)`, `await q.get()`, `q.task_done()`, `await q.join()`.

## 4. Cancellation
`task.cancel()` raises `asyncio.CancelledError` **inside** the task at its next `await`. Catch it only to clean up, then **re-raise**:
```python
async def worker() -> None:
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("cleaning up")
        raise                          # swallowing it breaks TaskGroup/timeout semantics
```

## Common pitfalls
- **Blocking the loop**: `time.sleep(1)`, `requests.get(...)` or a heavy loop inside `async def` freezes *every* task. Use `await asyncio.sleep`, an async client, or `await asyncio.to_thread(blocking_fn, *args)`.
- **Fire-and-forget tasks** from `asyncio.create_task(...)` can be garbage-collected mid-flight. Keep a reference (or use a `TaskGroup`).
- **`asyncio.run` inside a running loop** (e.g. Jupyter) raises `RuntimeError`. There, just `await main()`.
- `async def` is "contagious": only coroutines can `await`. Keep sync helpers sync, and keep the async layer thin, at the I/O edges.
