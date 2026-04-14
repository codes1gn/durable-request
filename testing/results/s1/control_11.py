"""Parse and evaluate simple arithmetic expressions (+, -, *, /, parentheses, unary minus)."""

from __future__ import annotations

import re
from typing import Union

Number = Union[int, float]


class _Parser:
    def __init__(self, text: str) -> None:
        self._tokens = re.findall(r"\d+\.?\d*|[+\-*/()]|\s+", text)
        self._i = 0

    def _peek(self) -> str | None:
        while self._i < len(self._tokens) and self._tokens[self._i].isspace():
            self._i += 1
        if self._i >= len(self._tokens):
            return None
        t = self._tokens[self._i]
        return None if t.isspace() else t

    def _consume(self, expected: str | None = None) -> str:
        while self._i < len(self._tokens) and self._tokens[self._i].isspace():
            self._i += 1
        if self._i >= len(self._tokens):
            raise ValueError("unexpected end of expression")
        t = self._tokens[self._i]
        self._i += 1
        if expected is not None and t != expected:
            raise ValueError(f"expected {expected!r}, got {t!r}")
        return t

    def parse(self) -> Number:
        result = self._expr()
        while self._i < len(self._tokens) and self._tokens[self._i].isspace():
            self._i += 1
        if self._i < len(self._tokens):
            raise ValueError("trailing garbage in expression")
        return result

    def _expr(self) -> Number:
        left = self._term()
        while True:
            op = self._peek()
            if op in ("+", "-"):
                self._consume()
                right = self._term()
                left = left + right if op == "+" else left - right
            else:
                break
        return left

    def _term(self) -> Number:
        left = self._factor()
        while True:
            op = self._peek()
            if op in ("*", "/"):
                self._consume()
                right = self._factor()
                if op == "*":
                    left = left * right
                else:
                    if right == 0:
                        raise ZeroDivisionError("division by zero")
                    left = left / right
            else:
                break
        return left

    def _factor(self) -> Number:
        tok = self._peek()
        if tok == "-":
            self._consume()
            return -self._factor()  # type: ignore[operator]
        if tok == "+":
            self._consume()
            return self._factor()
        if tok == "(":
            self._consume("(")
            inner = self._expr()
            self._consume(")")
            return inner
        if tok is None:
            raise ValueError("unexpected end of expression")
        if re.fullmatch(r"\d+\.?\d*", tok):
            self._consume()
            return float(tok) if "." in tok else int(tok)
        raise ValueError(f"unexpected token: {tok!r}")


def evaluate_expression(expr: str) -> Number:
    """
    Parse and evaluate a simple arithmetic expression.

    Supports +, -, *, /, parentheses, unary +/-, and integer or decimal literals.
    Whitespace is ignored.
    """
    cleaned = expr.strip()
    if not cleaned:
        raise ValueError("empty expression")
    return _Parser(cleaned).parse()
