"""Caesar cipher encrypt and decrypt for ASCII letters."""


def _shift_char(ch: str, shift: int) -> str:
    if "a" <= ch <= "z":
        base = ord("a")
        return chr((ord(ch) - base + shift) % 26 + base)
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr((ord(ch) - base + shift) % 26 + base)
    return ch


def caesar_encrypt(text: str, shift: int) -> str:
    """Encrypt `text` by rotating letters A–Z / a–z by `shift` (mod 26). Non-letters unchanged."""
    s = shift % 26
    return "".join(_shift_char(c, s) for c in text)


def caesar_decrypt(text: str, shift: int) -> str:
    """Decrypt text that was encrypted with the same `shift`."""
    return caesar_encrypt(text, -shift)
