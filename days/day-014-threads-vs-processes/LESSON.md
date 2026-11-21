# Day 014: Concurrency with threads vs processes (~5 min)

Day 013 covered `asyncio`: one thread, cooperative, best for **lots of I/O waits**. Today covers the other two tools in the standard library and how to choose between them.

| Workload | Bottleneck | Use |
|---|---|---|
| Waiting on network/disk/subprocess | I/O | threads (or asyncio) |
| Crunching numbers in pure Python | CPU | **processes** |
| C extensions that release the GIL (NumPy, hashlib on big buffers, zlib) | CPU, but in C | threads often work |

## 1. The GIL in one paragraph
CPython's **Global Interpreter Lock** lets only one thread run Python bytecode at a time. A thread gives up the GIL when it blocks on I/O (and during many C calls), so threads speed up **I/O-bound** work. They do **not** speed up a pure-Python CPU loop, and the extra switching can make it slower. Processes each have their own interpreter and their own GIL, so they get real parallelism. The cost is that arguments and results must be **pickled** and sent between processes. (Free-threaded "no-GIL" builds exist since 3.13 but are opt-in. Assume the GIL is on.)

## 2. `concurrent.futures`: one API for both
```python
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def io_task(n: int) -> int:
    time.sleep(0.2)          # stands in for an HTTP call; releases the GIL
    return n

def cpu_task(n: int) -> int:
    return sum(i * i for i in range(n))   # pure Python; holds the GIL

if __name__ == "__main__":   # REQUIRED for processes on macOS/Windows (spawn)
    for Pool, fn, arg in [(ThreadPoolExecutor, io_task, 1), (ThreadPoolExecutor, cpu_task, 2_000_000),
                          (ProcessPoolExecutor, cpu_task, 2_000_000)]:
        t0 = time.perf_counter()
        with Pool(max_workers=4) as pool:
            list(pool.map(fn, [arg] * 4))
        print(f"{Pool.__name__:20} {fn.__name__:8} {time.perf_counter() - t0:.2f}s")
# ThreadPoolExecutor   io_task  0.20s   <- 4 sleeps overlap
# ThreadPoolExecutor   cpu_task ~0.3s   <- about the same as running sequentially (GIL)
# ProcessPoolExecutor  cpu_task ~0.1s   <- real parallelism (on 4 cores)
```
- `pool.map(fn, items)` returns results **in input order** and re-raises the first exception when you reach that item.
- `pool.submit(fn, x)` returns a `Future`. `as_completed(futures)` yields them in **completion order**, and `fut.result()` returns the value or re-raises the exception from the worker.
- The `with` block waits for all work to finish (`shutdown(wait=True)`).

## 3. Shared state: threads share memory, processes don't
```python
import threading
from concurrent.futures import ThreadPoolExecutor

counter = 0
lock = threading.Lock()

def bump(times: int) -> None:
    global counter
    for _ in range(times):
        with lock:            # without it, `counter += 1` (read, add, write) can lose updates
            counter += 1

with ThreadPoolExecutor(8) as pool:
    for _ in range(8):
        pool.submit(bump, 100_000)
print(counter)                # 800000, guaranteed only with the lock
```
In a **process** pool, `global counter` would be a separate copy in each worker, and the parent would still see `0`. Instead, **return** results and combine them in the parent (map/reduce). That is usually the cleanest design for threads too.

## 4. Pitfalls
- **Missing `if __name__ == "__main__":`** with processes: on spawn platforms each worker re-imports your module and starts its own pool. You get a `RuntimeError` or a fork bomb.
- **Unpicklable work**: lambdas, nested functions and open files can't be sent to a process. Use module-level functions.
- **Tiny tasks in processes**: pickling overhead outweighs the work. Batch them (`chunksize=` in `pool.map`) or don't use processes at all.
- **Swallowed exceptions**: a `submit()`ed task that raises fails silently until you call `.result()`.
- **Too many threads**: pools exist so you don't spawn 10,000 threads. Size by workload (I/O: tens; CPU: `os.cpu_count()`).
