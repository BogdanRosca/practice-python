# Assignment 014: Benchmark threads vs processes, then fix a race (~15 min)

Create `solution.py` in this folder, push it to this branch, and merge the PR. Use only the standard library and type-hint everything. All pool code must live under `if __name__ == "__main__":` (or a `main()` called from it).

**Part 1: a tiny benchmark harness (~7 min)**
1. Write two module-level work functions:
   - `def io_bound(n: int) -> int`, which does `time.sleep(0.1)` and returns `n`.
   - `def cpu_bound(n: int) -> int`, which counts the primes below `n` by trial division in pure Python. Pick `n` so that one call takes roughly 0.1–0.3s (somewhere around `150_000`, depending on your machine).
2. Write `def run(executor_cls: type[Executor] | None, fn: Callable[[int], int], args: list[int], workers: int = 4) -> tuple[list[int], float]`. It returns `(results, seconds)`, and `executor_cls=None` means plain sequential execution. Results must be in **input order**. Reuse a `@contextmanager` timer like the one from Day 007 if you want.
3. Run all 6 combinations ({sequential, threads, processes} × {io_bound, cpu_bound}) with 8 tasks each and print a small table:
   ```
   mode        io_bound  cpu_bound
   sequential     0.80s      2.10s
   threads        0.20s      2.20s
   processes      0.25s      0.60s
   ```
4. `assert` that every mode returns identical results for the same function.
5. In a 2–3 line comment, explain each cell of the table that surprised you, in terms of the GIL and pickling/startup cost.

**Part 2: the race (~5 min)**
1. Write a class `BankAccount` with `balance: int` and `deposit(self, amount: int) -> None`. Make it racy on purpose: read `balance` into a local, call `time.sleep(0)` to force a thread switch, then write `local + amount` back.
2. Run 10 threads that each deposit `1` 1,000 times. Print the final balance, which should be well under 10,000.
3. Fix it with a `threading.Lock` held as an instance attribute, and show that it now always ends at 10,000.
4. In one comment: why would the racy version still be broken in a `ProcessPoolExecutor`, but for a **different** reason?

**Part 3: failures (~3 min)**
Use `submit` + `as_completed` on a thread pool with `cpu_bound` for `[10, 20, -1, 30]`, where your `cpu_bound` raises `ValueError` for negative `n`. Print each result as it completes, and catch and report the failure **without** losing the other three results.

**Bonus:**
- Pass `chunksize=` to the process pool's `map` with 1,000 tiny tasks (`cpu_bound(100)`), and show the timing difference between `chunksize=1` and `chunksize=100`.
- Try submitting a `lambda` to a `ProcessPoolExecutor`, then catch and print the pickling error.
- Put `cpu_bound` through `asyncio`: call it from a coroutine via `loop.run_in_executor(process_pool, cpu_bound, n)`. This connects to Day 013.
