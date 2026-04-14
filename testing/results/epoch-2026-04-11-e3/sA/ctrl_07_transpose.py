"""Matrix transpose for a list-of-lists representation."""


def transpose(matrix: list[list]) -> list[list]:
    """
    Return the transpose of `matrix` (rows become columns).

    Empty matrix returns []. For ragged rows, ``zip`` stops at the shortest
    row, so the result width is the minimum row length in the input.
    """
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix)]
