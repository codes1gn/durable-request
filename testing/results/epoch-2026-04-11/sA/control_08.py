"""Parse and evaluate simple arithmetic expressions with + - * / and parentheses."""


from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class _TokenKind(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()


@dataclass(frozen=True)
class _Token:
    kind: _TokenKind
    value: float | None = None


class _ParseError(ValueError):
    pass


def _tokenize(s: str) -> list[_Token]:
    tokens: list[_Token] = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c == "+":
            tokens.append(_Token(_TokenKind.PLUS))
            i += 1
            continue
        if c == "-":
            tokens.append(_Token(_TokenKind.MINUS))
            i += 1
            continue
        if c == "*":
            tokens.append(_Token(_TokenKind.MUL))
            i += 1
            continue
        if c == "/":
            tokens.append(_Token(_TokenKind.DIV))
            i += 1
            continue
        if c == "(":
            tokens.append(_Token(_TokenKind.LPAREN))
            i += 1
            continue
        if c == ")":
            tokens.append(_Token(_TokenKind.RPAREN))
            i += 1
            continue
        if c.isdigit() or c == ".":
            j = i + 1
            while j < n and (s[j].isdigit() or s[j] == "."):
                j += 1
            lex = s[i:j]
            try:
                num = float(lex)
            except ValueError as e:
                raise _ParseError(f"invalid number: {lex!r}") from e
            tokens.append(_Token(_TokenKind.NUMBER, num))
            i = j
            continue
        raise _ParseError(f"unexpected character: {c!r} at position {i}")
    tokens.append(_Token(_TokenKind.EOF))
    return tokens


class _Parser:
    def __init__(self, tokens: list[_Token]) -> None:
        self._tokens = tokens
        self._pos = 0

    def _peek(self) -> _Token:
        return self._tokens[self._pos]

    def _eat(self, kind: _TokenKind | None = None) -> _Token:
        tok = self._peek()
        if kind is not None and tok.kind != kind:
            raise _ParseError(f"expected {kind.name}, got {tok.kind.name}")
        self._pos += 1
        return tok

    def parse(self) -> float:
        result = self._expr()
        if self._peek().kind != _TokenKind.EOF:
            raise _ParseError("trailing input after expression")
        return result

    def _expr(self) -> float:
        left = self._term()
        while True:
            t = self._peek().kind
            if t == _TokenKind.PLUS:
                self._eat(_TokenKind.PLUS)
                left = left + self._term()
            elif t == _TokenKind.MINUS:
                self._eat(_TokenKind.MINUS)
                left = left - self._term()
            else:
                break
        return left

    def _term(self) -> float:
        left = self._factor()
        while True:
            t = self._peek().kind
            if t == _TokenKind.MUL:
                self._eat(_TokenKind.MUL)
                left = left * self._factor()
            elif t == _TokenKind.DIV:
                self._eat(_TokenKind.DIV)
                right = self._factor()
                if right == 0:
                    raise _ParseError("division by zero")
                left = left / right
            else:
                break
        return left

    def _factor(self) -> float:
        tok = self._peek()
        if tok.kind == _TokenKind.PLUS:
            self._eat(_TokenKind.PLUS)
            return self._factor()
        if tok.kind == _TokenKind.MINUS:
            self._eat(_TokenKind.MINUS)
            return -self._factor()
        if tok.kind == _TokenKind.LPAREN:
            self._eat(_TokenKind.LPAREN)
            v = self._expr()
            self._eat(_TokenKind.RPAREN)
            return v
        if tok.kind == _TokenKind.NUMBER:
            self._eat(_TokenKind.NUMBER)
            assert tok.value is not None
            return float(tok.value)
        raise _ParseError(f"unexpected token: {tok.kind.name}")


def evaluate_expression(expr: str) -> float:
    """
    Parse and evaluate a string containing a simple arithmetic expression.

    Supports binary + - * / with standard precedence, unary +/-, parentheses,
    floating-point literals, and arbitrary whitespace.

    Raises ValueError on invalid syntax, unknown tokens, or division by zero.
    """
    tokens = _tokenize(expr)
    try:
        return _Parser(tokens).parse()
    except _ParseError as e:
        raise ValueError(str(e)) from e
