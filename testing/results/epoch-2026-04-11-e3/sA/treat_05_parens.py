"""Validate balanced parentheses in a string."""


def is_balanced_parentheses(text: str) -> bool:
    """
    Return True if '(' and ')' in `text` are properly nested and matched.
    """
    balance = 0
    for ch in text:
        if ch == "(":
            balance += 1
        elif ch == ")":
            balance -= 1
            if balance < 0:
                return False
    return balance == 0
