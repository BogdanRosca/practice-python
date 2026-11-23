# Assignment 016: Speed up a legacy helper module (~15 min)

Create `solution.py` in this folder, push it to this branch, and merge the PR. Use only the standard library, and type-hint everything.

Here's a "legacy" helper module that works, but is too slow on real test data. Paste it into `solution.py` as-is. These are your **oracles**: don't change them.

```python
def has_duplicates_slow(items: list[str]) -> bool:
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False


def dedupe_slow(items: list[str]) -> list[str]:
    """Remove duplicates, keep first-seen order."""
    out: list[str] = []
    for x in items:
        if x not in out:
            out.append(x)
    return out


def top_words_slow(text: str, n: int) -> list[tuple[str, int]]:
    """The n most frequent lowercase words; ties broken alphabetically."""
    words = text.lower().split()
    counts = [(w, words.count(w)) for w in set(words)]
    counts.sort(key=lambda pair: (-pair[1], pair[0]))
    return counts[:n]
```

**Part 1: Rewrite (~8 min)**
1. Write `has_duplicates`, `dedupe` and `top_words` with the same signatures and the same behaviour, each in O(n) (or O(n + u log u) for `top_words`, where u is the number of unique words).
2. Above each function, add a one-line comment giving the old and the new complexity and the reason, e.g. `# O(n^2) -> O(n): set membership instead of nested scan`.
3. Write `check_equivalence() -> None`. It builds random input (`random.choices` from a small vocabulary such as `["a", "b", "c", "dog", "cat"]`, so ties actually happen), and `assert`s that every slow/fast pair gives the same result over ~200 random cases. Include the edge cases `[]`, `""`, `n=0` and `n` greater than the number of unique words.

**Part 2: Measure (~7 min)**
1. Write `bench(fn: Callable[[], object], repeat: int = 5, number: int = 3) -> float` that returns the best per-call time in seconds, using `timeit.repeat`.
2. In an `if __name__ == "__main__":` block: run `check_equivalence()`, then print a small table for `dedupe_slow` vs `dedupe` at n = 1 000, 2 000 and 4 000 unique-ish strings (e.g. `[str(i % (n // 2)) for i in range(n)]`). Print the slow/fast ratio for each n too.
3. In a comment under the table, answer: when n doubles, by roughly how much does `dedupe_slow`'s time grow, and what does that tell you?
4. Run `python -m cProfile -s tottime solution.py` once, and note in a comment which line or function dominated `top_words_slow` on a big input, and why.

**Bonus:**
- Write `fib(n)` the naive recursive way, time `fib(30)`, then add `@functools.cache` and time it again. Print `fib.cache_info()` and explain the hits/misses in a comment.
- Why would `Counter(words).most_common(n)` on its own fail `check_equivalence()`? Prove it with one concrete input in a comment.
