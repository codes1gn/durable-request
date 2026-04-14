"""Longest common subsequence of two strings."""

from __future__ import annotations


def longest_common_subsequence(a: str, b: str) -> str:
    """
    Return one longest common subsequence of ``a`` and ``b`` (as a string).

    Uses dynamic programming; time O(len(a) * len(b)), space O(len(a) * len(b)).
    """
    na, nb = len(a), len(b)
    # dp[i][j] = LCS length of a[:i] and b[:j]
    dp = [[0] * (nb + 1) for _ in range(na + 1)]
    for i in range(1, na + 1):
        for j in range(1, nb + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # backtrack
    out: list[str] = []
    i, j = na, nb
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))
