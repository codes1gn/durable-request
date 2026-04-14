"""N-Queens via backtracking: place queens row-by-row, prune on columns and diagonals."""


def solve_n_queens(n: int) -> list[list[int]]:
    """
    Return every valid placement as a list of length n where index r is the column
    of the queen in row r (0-based). Empty list if n < 1.
    """
    if n < 1:
        return []

    solutions: list[list[int]] = []
    cols: set[int] = set()
    diag_down: set[int] = set()  # r - c
    diag_up: set[int] = set()  # r + c

    def backtrack(row: int, placement: list[int]) -> None:
        if row == n:
            solutions.append(placement.copy())
            return
        for c in range(n):
            if c in cols or (row - c) in diag_down or (row + c) in diag_up:
                continue
            cols.add(c)
            diag_down.add(row - c)
            diag_up.add(row + c)
            placement.append(c)
            backtrack(row + 1, placement)
            placement.pop()
            cols.remove(c)
            diag_down.remove(row - c)
            diag_up.remove(row + c)

    backtrack(0, [])
    return solutions


def n_queens_count(n: int) -> int:
    """Number of distinct solutions for board size n."""
    return len(solve_n_queens(n))
