"""Check whether an integer reads the same forwards and backwards."""


def is_palindrome_number(n: int) -> bool:
    if n < 0:
        return False
    s = str(n)
    return s == s[::-1]


if __name__ == "__main__":
    for n in (0, 1, 121, 12321, 12345, -121):
        print(f"is_palindrome_number({n}) = {is_palindrome_number(n)}")
