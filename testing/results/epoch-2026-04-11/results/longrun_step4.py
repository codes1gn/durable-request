from longrun_step1 import add
from longrun_step2 import multiply
from longrun_step3 import power


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_multiply():
    assert multiply(4, 5) == 20
    assert multiply(0, 100) == 0


def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1


if __name__ == "__main__":
    test_add()
    test_multiply()
    test_power()
    print("all tests passed")
