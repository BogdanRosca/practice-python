# Assignment 015: A ticket workflow with enums (~15 min)

Create `solution.py` in this folder, push it to this branch, and merge the PR. Use only the standard library, and type-hint everything.

**Part 1: `Status` with transitions (~8 min)**
1. `class Status(Enum)` with members `OPEN`, `IN_PROGRESS`, `BLOCKED` and `DONE` (use `auto()`), decorated with `@unique`.
2. A method `can_move_to(self, target: "Status") -> bool` implementing these rules:
   - `OPEN -> IN_PROGRESS`
   - `IN_PROGRESS -> BLOCKED | DONE`
   - `BLOCKED -> IN_PROGRESS`
   - `DONE ->` nothing (terminal)

   Keep the rules in **one** mapping, not an `if/elif` chain. Tip: you can't easily reference members inside the class body, so build the dict at module level right after the class, or inside the method.
3. A property `is_terminal`.
4. A classmethod `parse(text: str) -> Status` that accepts `"in progress"`, `" In_Progress "`, `"in-progress"` etc. It raises `ValueError` with a helpful message that lists the valid names, for example `unknown status 'nope'; expected one of OPEN, IN_PROGRESS, BLOCKED, DONE`.

**Part 2: `Ticket` + permissions (~7 min)**
1. `class Role(Flag)` with `VIEW`, `EDIT`, `CLOSE` and a combined alias `ADMIN = VIEW | EDIT | CLOSE`.
2. A small `Ticket` class (a plain class or `@dataclass`) with `title: str` and `status: Status = Status.OPEN`, plus `move(self, target: Status, role: Role) -> None`:
   - Any move needs `Role.EDIT`. Moving to `DONE` additionally needs `Role.CLOSE`. On failure, raise `PermissionError`.
   - An illegal transition raises `ValueError("cannot move OPEN -> DONE")` (use member `.name`s).
3. In an `if __name__ == "__main__":` demo, show: a full happy path `OPEN -> IN_PROGRESS -> BLOCKED -> IN_PROGRESS -> DONE` with `Role.ADMIN`, an illegal jump, a `Role.VIEW | Role.EDIT` user failing to close, `Status.parse` on three spellings plus one bad one, and `list(Role.ADMIN)`. Catch each error and print it.

**Bonus:**
- Make `Status` a `StrEnum` instead and serialise a ticket to JSON with `json.dumps({"title": t.title, "status": t.status})`. Then switch back to a plain `Enum` and explain in a comment why `json.dumps` now fails, and what you'd store instead (`.name`).
- Implement `_missing_` so that `Status("done")` also works, delegating to `parse`.
