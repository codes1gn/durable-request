"""Greatest common divisor (Euclidean algorithm, iterative)."""


def gcd(a: int, b: int) -> int:
    if a == 0 and b == 0:
        raise ValueError("gcd(0, 0) is undefined")
    x, y = abs(a), abs(b)
    while y:
        x, y = y, x % y
    return x


if __name__ == "__main__":
    pairs = [(48, 18), (100, 35), (17, 13), (0, 7), (12, 0)]
    for p, q in pairs:
        print(f"gcd({p}, {q}) = {gcd(p, q)}")
