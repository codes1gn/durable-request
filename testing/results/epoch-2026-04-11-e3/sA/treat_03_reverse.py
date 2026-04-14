"""Reverse the character order within each word; whitespace and word order preserved."""


def reverse_words(text: str) -> str:
    def rev_word(word: str) -> str:
        return word[::-1]

    parts: list[str] = []
    buf: list[str] = []
    for ch in text:
        if ch.isspace():
            if buf:
                parts.append(rev_word("".join(buf)))
                buf = []
            parts.append(ch)
        else:
            buf.append(ch)
    if buf:
        parts.append(rev_word("".join(buf)))
    return "".join(parts)


if __name__ == "__main__":
    sample = "Hello, world!\nSecond line."
    print(reverse_words(sample))
