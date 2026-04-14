"""N-Queens solver via backtracking."""

from __future__ import annotations


def solve_n_queens(n: int) -> list[list[str]]:
    """
    Return all distinct solutions to the N-Queens problem as boards of ``'Q'`` and ``'.'``.
    Each solution is an ``n``-row list of strings of length ``n``.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return [[]]

    solutions: list[list[str]] = []
    board = [["."] * n for _ in range(n)]

    def safe(row: int, col: int) -> bool:
        for r in range(row):
            if board[r][col] == "Q":
                return False
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] == "Q":
                return False
            r -= 1
            c -= 1
        r, c = row - 1, col + 1
        while r >= 0 and c < n:
            if board[r][c] == "Q":
                return False
            r -= 1
            c += 1
        return True

    def backtrack(row: int) -> None:
        if row == n:
            solutions.append(["".join(r) for r in board])
            return
        for col in range(n):
            if safe(row, col):
                board[row][col] = "Q"
                backtrack(row + 1)
                board[row][col] = "."

    backtrack(0)
    return solutions
