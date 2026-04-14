"""N-Queens solver via backtracking."""

from __future__ import annotations


def solve_n_queens(n: int) -> list[list[str]]:
    """
    Return all distinct solutions to the n-queens problem.
    Each solution is a list of n strings of length n with 'Q' and '.'.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return [[]]

    cols: set[int] = set()
    diag1: set[int] = set()  # r - c
    diag2: set[int] = set()  # r + c
    board: list[int] = []  # row -> column
    solutions: list[list[str]] = []

    def place_row(row: int) -> None:
        if row == n:
            solutions.append(
                ["".join("Q" if board[r] == c else "." for c in range(n)) for r in range(n)]
            )
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board.append(col)
            place_row(row + 1)
            board.pop()
            diag2.remove(row + col)
            diag1.remove(row - col)
            cols.remove(col)

    place_row(0)
    return solutions


def count_n_queens_solutions(n: int) -> int:
    """Count solutions without building full boards (same backtracking)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 1

    cols: set[int] = set()
    diag1: set[int] = set()
    diag2: set[int] = set()
    count = 0

    def place_row(row: int) -> None:
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            place_row(row + 1)
            diag2.remove(row + col)
            diag1.remove(row - col)
            cols.remove(col)

    place_row(0)
    return count
