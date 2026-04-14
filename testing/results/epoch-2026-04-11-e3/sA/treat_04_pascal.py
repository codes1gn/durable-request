"""Pascal's triangle up to n rows (0 rows -> [], 1 row -> [[1]], etc.)."""


def pascals_triangle(n: int) -> list[list[int]]:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []
    rows: list[list[int]] = [[1]]
    for r in range(1, n):
        prev = rows[r - 1]
        row = [1]
        for i in range(1, r):
            row.append(prev[i - 1] + prev[i])
        row.append(1)
        rows.append(row)
    return rows
