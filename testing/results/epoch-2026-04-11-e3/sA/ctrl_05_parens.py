def is_balanced_parentheses(text: str) -> bool:
    """Return True if every '(' in `text` has a matching ')' in order."""
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0
