def gcd(a: int, b: int) -> int:
    x, y = abs(a), abs(b)
    while y:
        x, y = y, x % y
    return x
