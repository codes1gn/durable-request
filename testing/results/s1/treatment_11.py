"""
Simple arithmetic expression parser and evaluator.

Supports +, -, *, /, parentheses, unary minus, and floating-point literals.
Whitespace is ignored.
"""

from __future__ import annotations

import re
from typing import Union

Number = Union[int, float]


class _ParseError(ValueError):
    pass


def _tokenize(expr: str) -> list[str]:
    s = expr.replace(" ", "")
    if not s:
        return []
    # Split into numbers and single-char operators/parens
    parts = re.findall(r"\d+\.?\d*|[+\-*/()]", s)
    return parts


def _to_number(tok: str) -> Number:
    if "." in tok:
        return float(tok)
    return int(tok)


def evaluate_expression(expr: str) -> Number:
    """
    Parse and evaluate a simple arithmetic expression.

    Args:
        expr: Expression using digits, + - * / ( ), optional decimal point.

    Returns:
        Numeric result (int if the value is whole, else float in practice
        we return float when division or float literals appear).

    Raises:
        ValueError: On invalid syntax or division by zero.
    """
    tokens = _tokenize(expr)
    if not tokens:
        raise ValueError("empty expression")

    pos = 0

    def peek() -> str | None:
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected: str | None = None) -> str:
        nonlocal pos
        t = peek()
        if t is None:
            raise _ParseError("unexpected end of expression")
        if expected is not None and t != expected:
            raise _ParseError(f"expected {expected!r}, got {t!r}")
        pos += 1
        return t

    def parse_factor() -> Number:
        t = peek()
        if t is None:
            raise _ParseError("expected value")
        if t == "(":
            consume("(")
            v = parse_expr()
            consume(")")
            return v
        if t == "-":
            consume("-")
            return -parse_factor()
        if t == "+":
            consume("+")
            return parse_factor()
        if t and (t[0].isdigit() or t == "."):
            consume()
            return _to_number(t)
        raise _ParseError(f"unexpected token {t!r}")

    def parse_term() -> Number:
        left = parse_factor()
        while True:
            op = peek()
            if op in ("*", "/"):
                consume()
                right = parse_factor()
                if op == "*":
                    left = left * right
                else:
                    if right == 0:
                        raise ValueError("division by zero")
                    left = left / right
            else:
                break
        return left

    def parse_expr() -> Number:
        left = parse_term()
        while True:
            op = peek()
            if op in ("+", "-"):
                consume()
                right = parse_term()
                if op == "+":
                    left = left + right
                else:
                    left = left - right
            else:
                break
        return left

    try:
        result = parse_expr()
    except _ParseError as e:
        raise ValueError(str(e)) from e

    if pos != len(tokens):
        raise ValueError(f"trailing garbage at position {pos}")
    return result


if __name__ == "__main__":
    assert evaluate_expression("1 + 2 * 3") == 7
    assert evaluate_expression("(1 + 2) * 3") == 9
    assert abs(evaluate_expression("3.5 * 2") - 7.0) < 1e-9
