# Day 016: Performance, big-O & profiling (~5 min read)

Most slow Python code isn't slow because "Python is slow". It's slow because it does a hidden O(n) operation inside a loop. As an SDET you see this in test helpers, log parsers and data fixtures. They're fine with 100 rows and painful with 100k. Today: spot the hidden costs, measure instead of guessing, and fix with the right data structure.

## 1. Know the cost of the built-ins
| Operation | `list` | `set` / `dict` |
|---|---|---|
| `x in c` | **O(n)** (linear scan) | O(1) average (hash lookup) |
| `c.append(x)` / `c.add(x)` | O(1) amortised | O(1) average |
| `c.insert(0, x)` / `c.pop(0)` | **O(n)** (shifts everything) | — (use `collections.deque`: O(1) at both ends) |
| `c.count(x)` / `c.index(x)` | **O(n)** | — |
| `sorted(c)` | O(n log n) | O(n log n) |

So a loop that does `if x not in some_list` is O(n²) overall. Swap the list for a set and it becomes O(n). For data that has to keep its order, use a set for "seen" and a list for the output, or `dict.fromkeys(items)`. Dicts keep insertion order.

```python
def dedupe_slow(items):
    out = []
    for x in items:
        if x not in out:        # O(n) scan each time, so O(n^2) total
            out.append(x)
    return out

def dedupe_fast(items):
    return list(dict.fromkeys(items))   # O(n), keeps first-seen order
```

## 2. Measure with `timeit`, not with your gut
`timeit` runs code many times and turns off the garbage collector while it does, so timings are stable. Take the **minimum** of several repeats. Noise only ever makes a run slower, never faster.

```python
import timeit

data = list(range(5_000)) * 2
for fn in (dedupe_slow, dedupe_fast):
    best = min(timeit.repeat(lambda: fn(data), number=3, repeat=5)) / 3
    print(f"{fn.__name__:12} {best * 1000:8.2f} ms")
# dedupe_slow    ~120 ms
# dedupe_fast    ~0.2 ms
```
Scaling tells you the complexity. If you multiply n by 10 and the time goes up about 10×, it's linear. If it goes up about 100×, it's quadratic. That check is more reliable than reading the code when calls are nested.

## 3. Find the hotspot with `cProfile`
When a whole function is slow and you don't know why, profile it:

```python
import cProfile, pstats

cProfile.run("dedupe_slow(data)", "out.prof")
pstats.Stats("out.prof").sort_stats("cumulative").print_stats(5)
```
Or from the shell: `python -m cProfile -s cumulative solution.py`. Read the `ncalls` and `cumtime` columns. A built-in like `list.count` with 10 000 calls is usually the culprit. Note that `x in list` doesn't appear as a separate call. It's an operator, so its cost shows up as `tottime` of the function containing it.

## 4. Cheap wins that come up again and again
- **Membership / lookup:** build a `set` or `dict` once, outside the loop.
- **Counting:** `collections.Counter(items)` is a single O(n) pass. Calling `items.count(x)` for every x is O(n²).
- **String building:** `"".join(parts)`, not `s += part` in a loop.
- **Queues:** `deque.popleft()`, not `list.pop(0)`.
- **Repeated pure calls:** `functools.cache` / `lru_cache` (memoisation).
- **Sorted data:** `bisect` gives O(log n) search.

## Common pitfalls
- **Optimising without measuring.** Profile first. The slow part is rarely where you expect it.
- **Micro-benchmarks that lie.** If you time `fn(data)` where `data` is a generator, it's exhausted after the first run and every later run times nothing. Time the code with realistic sizes, too: at n=10, everything is fast.
- **Changing behaviour while optimising.** `Counter.most_common()` breaks ties by *first-seen order*, not alphabetically. If the old code sorted ties by name, your "fast" version is now a different function. Keep the slow version as an oracle and `assert slow(x) == fast(x)` on random input.
- **Big-O isn't everything.** For n < ~50, a list scan can beat building a set. Constant factors matter for small inputs.
