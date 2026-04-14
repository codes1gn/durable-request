"""Transpose a matrix (list of rows) in O(rows * cols) time and space."""


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix)]


if __name__ == "__main__":
    m = [[1, 2, 3], [4, 5, 6]]
    print(transpose(m))
