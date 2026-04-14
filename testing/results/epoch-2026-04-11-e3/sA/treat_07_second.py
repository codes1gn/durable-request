"""Return the second-largest distinct value in a non-empty sequence of ints."""


def second_largest(nums: list[int]) -> int | None:
    if len(nums) < 2:
        return None
    first = second = None
    for n in nums:
        if first is None or n > first:
            second, first = first, n
        elif n != first and (second is None or n > second):
            second = n
    return second


if __name__ == "__main__":
    print(second_largest([3, 1, 4, 1, 5, 9, 2, 6]))
