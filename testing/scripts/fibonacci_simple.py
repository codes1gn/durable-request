"""Small Fibonacci helper for durable-request checkpoint format testing."""


def fibonacci(n: int) -> int:
    """Return F(n) with F(0)=0, F(1)=1, F(k)=F(k-1)+F(k-2)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
