def roman_to_int(s: str) -> int:
    """Convert a Roman numeral string to an integer (1–3999 typical range)."""
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(s.upper()):
        v = values.get(ch)
        if v is None:
            raise ValueError(f"Invalid Roman numeral character: {ch!r}")
        if v < prev:
            total -= v
        else:
            total += v
            prev = v
    return total
