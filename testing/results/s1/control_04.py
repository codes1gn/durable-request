"""Email address validation using a regular expression."""

import re

# Practical RFC 5322–inspired pattern: local@domain with common labels and TLD.
_EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,}$"
)


def is_valid_email(address: str) -> bool:
    """Return True if *address* looks like a valid email."""
    if not address or len(address) > 254:
        return False
    return bool(_EMAIL_RE.fullmatch(address.strip()))
