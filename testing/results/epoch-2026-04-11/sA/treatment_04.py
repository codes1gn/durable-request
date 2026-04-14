"""N-Queens: all distinct solutions via backtracking."""


def solve_n_queens(n: int) -> list[list[str]]:
    """
    Return every valid n×n board as rows of '.' and 'Q'.

    Uses backtracking: one queen per row, pruning when a column or diagonal
    is attacked. Empty list if n < 1.
    """
    if n < 1:
        return []

    solutions: list[list[str]] = []
    board: list[int] = []  # board[r] = column index of queen on row r
    cols: set[int] = set()
    diag_down: set[int] = set()  # r - c
    diag_up: set[int] = set()  # r + c

    def row_to_str(row: int, col: int) -> str:
        return "." * col + "Q" + "." * (n - col - 1)

    def backtrack(row: int) -> None:
        if row == n:
            solutions.append([row_to_str(r, board[r]) for r in range(n)])
            return
        for col in range(n):
            if col in cols or (row - col) in diag_down or (row + col) in diag_up:
                continue
            board.append(col)
            cols.add(col)
            diag_down.add(row - col)
            diag_up.add(row + col)
            backtrack(row + 1)
            diag_up.remove(row + col)
            diag_down.remove(row - col)
            cols.remove(col)
            board.pop()

    backtrack(0)
    return solutions
