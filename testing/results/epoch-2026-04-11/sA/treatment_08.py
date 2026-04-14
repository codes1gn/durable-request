"""Parse and evaluate simple arithmetic expressions (+, -, *, /)."""

from __future__ import annotations


def evaluate_arithmetic(expression: str) -> float:
    """
    Evaluate a string containing only numbers, whitespace, parentheses, and + - * /.

    Unary ``+`` / ``-`` on factors is supported. ``*`` and ``/`` bind tighter than ``+`` and ``-``.
    Division is true division (float). Raises ``ValueError`` if the input is not a valid expression.
    """
    tokens = _tokenize(expression)
    if not tokens:
        raise ValueError("empty expression")

    class ParseState:
        __slots__ = ("i",)

        def __init__(self) -> None:
            self.i = 0

    state = ParseState()

    def peek() -> str | float:
        return tokens[state.i]

    def consume() -> str | float:
        t = tokens[state.i]
        state.i += 1
        return t

    def parse_expr() -> float:
        left = parse_term()
        while state.i < len(tokens) and peek() in ("+", "-"):
            op = consume()
            right = parse_term()
            left = left + right if op == "+" else left - right
        return left

    def parse_term() -> float:
        left = parse_factor()
        while state.i < len(tokens) and peek() in ("*", "/"):
            op = consume()
            right = parse_factor()
            if op == "*":
                left *= right
            else:
                if right == 0:
                    raise ValueError("division by zero")
                left /= right
        return left

    def parse_factor() -> float:
        if state.i >= len(tokens):
            raise ValueError("unexpected end of expression")

        sign = 1.0
        while peek() in ("+", "-"):
            op = consume()
            sign *= 1.0 if op == "+" else -1.0

        t = peek()
        if t == "(":
            consume()
            inner = parse_expr()
            if state.i >= len(tokens) or consume() != ")":
                raise ValueError("unclosed '('")
            return sign * inner
        if isinstance(t, float):
            consume()
            return sign * t
        raise ValueError(f"expected number or '(', got {t!r}")

    result = parse_expr()
    if state.i != len(tokens):
        raise ValueError("unexpected trailing tokens")
    return result


def _tokenize(s: str) -> list[str | float]:
    """Split ``s`` into numbers and single-character operators/parentheses."""
    out: list[str | float] = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c in "+-*/()":
            out.append(c)
            i += 1
            continue
        if c.isdigit() or (c == "." and i + 1 < n and s[i + 1].isdigit()):
            start = i
            if c == ".":
                i += 1
            while i < n and s[i].isdigit():
                i += 1
            if i < n and s[i] == ".":
                i += 1
                while i < n and s[i].isdigit():
                    i += 1
            num_str = s[start:i]
            if num_str == "." or num_str == "":
                raise ValueError(f"invalid number near position {start}")
            out.append(float(num_str))
            continue
        raise ValueError(f"invalid character {c!r} at position {i}")
    return out
