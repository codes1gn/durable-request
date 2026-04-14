"""IPv4 string validation."""


def is_valid_ipv4(s: str) -> bool:
    """Return True if *s* is a dotted-decimal IPv4 address (four octets 0–255)."""
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p or not p.isdigit():
            return False
        n = int(p)
        if n < 0 or n > 255:
            return False
    return True
