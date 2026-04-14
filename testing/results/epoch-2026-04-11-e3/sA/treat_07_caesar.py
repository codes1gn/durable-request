"""Caesar cipher: shift letters A–Z / a–z by k positions; non-letters unchanged."""


def caesar_shift(text: str, k: int) -> str:
    k %= 26
    out: list[str] = []
    for ch in text:
        if "A" <= ch <= "Z":
            base = ord("A")
            out.append(chr(base + (ord(ch) - base + k) % 26))
        elif "a" <= ch <= "z":
            base = ord("a")
            out.append(chr(base + (ord(ch) - base + k) % 26))
        else:
            out.append(ch)
    return "".join(out)


if __name__ == "__main__":
    print(caesar_shift("Hello, World!", 3))
