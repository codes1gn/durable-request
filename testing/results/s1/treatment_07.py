"""Convert between Roman numerals and integers (typical range 1–3999)."""

from __future__ import annotations

_ROMAN_PAIRS = (
    ("M", 1000),
    ("CM", 900),
    ("D", 500),
    ("CD", 400),
    ("C", 100),
    ("XC", 90),
    ("L", 50),
    ("XL", 40),
    ("X", 10),
    ("IX", 9),
    ("V", 5),
    ("IV", 4),
    ("I", 1),
)


def int_to_roman(n: int) -> str:
    """Convert a positive integer to a Roman numeral string."""
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if not 1 <= n <= 3999:
        raise ValueError("n must be in 1..3999 for standard Roman numerals")
    parts: list[str] = []
    remaining = n
    for sym, value in _ROMAN_PAIRS:
        while remaining >= value:
            parts.append(sym)
            remaining -= value
    return "".join(parts)


def roman_to_int(s: str) -> int:
    """Parse a Roman numeral string to an integer."""
    if not isinstance(s, str) or not s:
        raise ValueError("non-empty string required")
    s = s.upper().strip()
    i = 0
    total = 0
    for sym, value in _ROMAN_PAIRS:
        slen = len(sym)
        while s.startswith(sym, i):
            total += value
            i += slen
    if i != len(s):
        raise ValueError(f"invalid Roman numeral: {s!r}")
    if not 1 <= total <= 3999:
        raise ValueError("result out of 1..3999")
    return total
