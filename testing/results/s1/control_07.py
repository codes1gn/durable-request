"""Roman numeral ↔ integer conversion."""

from __future__ import annotations

_ROMAN_PAIRS: list[tuple[str, int]] = [
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
]


def int_to_roman(n: int) -> str:
    if n <= 0 or n > 3999:
        raise ValueError("integer must be in 1..3999 for standard Roman numerals")
    parts: list[str] = []
    remaining = n
    for sym, val in _ROMAN_PAIRS:
        while remaining >= val:
            parts.append(sym)
            remaining -= val
    return "".join(parts)


def roman_to_int(s: str) -> int:
    s = s.upper().strip()
    if not s:
        raise ValueError("empty Roman numeral")
    i = 0
    total = 0
    while i < len(s):
        matched = False
        for sym, val in _ROMAN_PAIRS:
            if s.startswith(sym, i):
                total += val
                i += len(sym)
                matched = True
                break
        if not matched:
            raise ValueError(f"invalid Roman numeral at position {i}: {s!r}")
    if total < 1 or total > 3999:
        raise ValueError("result out of 1..3999")
    return total
