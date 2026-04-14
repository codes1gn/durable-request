"""Email address validation using a regular expression."""

from __future__ import annotations

import re

# Practical pattern: local@domain with common label rules (not full RFC 5322).
_EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@"
    r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,}$"
)


def is_valid_email(address: str) -> bool:
    """Return True if *address* matches the supported email pattern."""
    if not address or len(address) > 254:
        return False
    return bool(_EMAIL_RE.fullmatch(address.strip()))
