def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("factorial undefined for negative integers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
