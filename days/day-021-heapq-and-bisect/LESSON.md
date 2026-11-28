# Day 021: `heapq` & `bisect` (~5 min read)

Two small stdlib modules that replace a lot of hand-written loops. Use them when you keep **re-sorting a list** or **scanning it** to find something:

| Need | Naive | Better | Cost |
|---|---|---|---|
| Repeatedly take the smallest item | `items.sort(); items.pop(0)` | `heapq.heappush` / `heappop` | O(log n) each |
| Top-k of a big collection | `sorted(xs)[-k:]` | `heapq.nlargest(k, xs)` | O(n log k) |
| Merge already-sorted streams | `sorted(a + b + c)` | `heapq.merge(a, b, c)` (lazy) | O(n log streams) |
| Find a position in a sorted list | linear scan | `bisect.bisect_left` | O(log n) |
| Keep a list sorted while adding | `append` + `sort` | `bisect.insort` | O(log n) search + O(n) shift |

## 1. `heapq`: a min-heap on top of a plain `list`
```python
import heapq

jobs: list[tuple[int, str]] = []
heapq.heappush(jobs, (2, "smoke"))
heapq.heappush(jobs, (1, "unit"))
heapq.heappush(jobs, (3, "e2e"))
print(heapq.heappop(jobs))   # (1, 'unit')  - smallest first
print(jobs[0])               # (2, 'smoke') - peek, O(1)
```
- The list is a heap only through the `heapq` functions. `jobs` is **not** sorted; only `jobs[0]` is guaranteed to be the smallest.
- `heapq.heapify(xs)` turns an existing list into a heap in place, in O(n).
- There is only a **min**-heap. For "largest first", push `(-priority, ...)`.

### Tie-breaking: the classic bug
Tuples compare item by item. With equal priorities, Python compares the next element:
```python
import heapq

heap = []
heapq.heappush(heap, (1, {"name": "a"}))
heapq.heappush(heap, (1, {"name": "b"}))  # TypeError: '<' not supported between 'dict' and 'dict'
```
The fix is a monotonically increasing counter as the second element. It also makes equal priorities come out **FIFO**:
```python
import itertools
counter = itertools.count()
heapq.heappush(heap, (1, next(counter), {"name": "a"}))
```

## 2. Top-k and lazy merging
```python
import heapq

durations = {"login": 4.2, "checkout": 9.8, "search": 1.1, "cart": 7.5}
print(heapq.nlargest(2, durations.items(), key=lambda kv: kv[1]))
# [('checkout', 9.8), ('cart', 7.5)]

a = [(1, "a1"), (5, "a2")]           # each stream already sorted by timestamp
b = [(2, "b1"), (3, "b2")]
print(list(heapq.merge(a, b, key=lambda e: e[0])))
# [(1, 'a1'), (2, 'b1'), (3, 'b2'), (5, 'a2')]
```
`nlargest`/`nsmallest` take `key=` and are **stable**: equal keys keep their input order. `heapq.merge` is a generator, so you can merge huge log files without loading them into memory. It assumes every input is already sorted and does not check.

## 3. `bisect`: binary search on a sorted list
```python
import bisect

latencies = [12, 15, 15, 20, 31, 48]
bisect.bisect_left(latencies, 15)    # 1 -> index of the first 15
bisect.bisect_right(latencies, 15)   # 3 -> index just after the last 15

# How many values fall in [15, 30]?  Two searches, no loop:
bisect.bisect_right(latencies, 30) - bisect.bisect_left(latencies, 15)   # 3

bisect.insort(latencies, 18)         # [12, 15, 15, 18, 20, 31, 48]
```
Think of the result as an insertion point: `bisect_left` goes before equal items, `bisect_right` after them. That one difference decides whether range ends are inclusive or exclusive.

Grade boundaries, a lookup table without `if/elif`:
```python
import bisect

def grade(score: int) -> str:
    return "FDCBA"[bisect.bisect_right([60, 70, 80, 90], score)]

grade(59), grade(60), grade(95)   # ('F', 'D', 'A')
```
Since Python 3.10, `bisect` functions take `key=` too. The key is applied to the list items, **not** to the value you search for: `bisect_left(records, 42, key=lambda r: r.ts)`.

## Pitfalls
- Indexing a heap: `heap[1]` is **not** the second smallest. Only `heap[0]` means anything.
- Modifying a heap list directly (`heap.append`, `heap.remove`) breaks the heap property. Call `heapify` again, or use lazy deletion (mark entries dead and skip them on pop).
- `bisect` on an unsorted list returns nonsense silently.
- `insort` is O(n) because of the list shift. That's fine for thousands of items; for millions of inserts, look at `sortedcontainers.SortedList`.
- `nlargest(1, xs)` is just `max(xs)`, and with `k` close to `len(xs)` a plain `sorted` is faster. `heapq` shines when `k` is small and the input is large.
