def is_valid_ipv4(s: str) -> bool:
    """Return True if s is a dotted-decimal IPv4 address (strict octet rules)."""
    if not isinstance(s, str):
        return False
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        if len(part) > 1 and part[0] == "0":
            return False
        value = int(part)
        if value < 0 or value > 255:
            return False
    return True
