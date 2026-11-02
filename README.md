# practice-python

Daily ~20-minute Python practice, prepared automatically each morning.

## How it works
1. A new branch `day-NNN-<topic>` and a pull request appear each day.
2. Check out the branch and read `days/day-NNN-*/LESSON.md` (~5 min).
3. Implement the stubs in `exercise.py` (~15 min).
4. Run `pip install -r requirements.txt && pytest days/day-NNN-<topic>`.
5. Commit your solution, then merge the PR.
6. The next morning's run reviews merged days (`REVIEW.md`) and updates `PROGRESS.md`.

Unmerged days are marked "skipped" - no pressure.
