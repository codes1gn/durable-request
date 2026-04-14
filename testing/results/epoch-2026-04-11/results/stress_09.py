import importlib.util
import sys
import unittest
from pathlib import Path

_DIR = Path(__file__).resolve().parent


def _load(stem: str):
    path = _DIR / f"{stem}.py"
    if stem in sys.modules:
        return sys.modules[stem]
    spec = importlib.util.spec_from_file_location(stem, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[stem] = mod
    spec.loader.exec_module(mod)
    return mod


# stress_04 imports stress_03 at module load time
_load("stress_03")
_load("stress_04")

m01 = _load("stress_01")
m02 = _load("stress_02")
m03 = _load("stress_03")
m04 = _load("stress_04")
m05 = _load("stress_05")
m06 = _load("stress_06")
m07 = _load("stress_07")
m08 = _load("stress_08")


class TestStressFunctions(unittest.TestCase):
    def test_is_prime(self):
        self.assertFalse(m01.is_prime(0))
        self.assertFalse(m01.is_prime(1))
        self.assertTrue(m01.is_prime(2))
        self.assertTrue(m01.is_prime(17))
        self.assertFalse(m01.is_prime(18))

    def test_factorial(self):
        self.assertEqual(m02.factorial(0), 1)
        self.assertEqual(m02.factorial(5), 120)
        with self.assertRaises(ValueError):
            m02.factorial(-1)

    def test_gcd(self):
        self.assertEqual(m03.gcd(48, 18), 6)
        self.assertEqual(m03.gcd(-48, 18), 6)

    def test_lcm(self):
        self.assertEqual(m04.lcm(4, 6), 12)
        self.assertEqual(m04.lcm(0, 5), 0)

    def test_fibonacci(self):
        self.assertEqual(m05.fibonacci(0), 0)
        self.assertEqual(m05.fibonacci(1), 1)
        self.assertEqual(m05.fibonacci(10), 55)
        with self.assertRaises(ValueError):
            m05.fibonacci(-1)

    def test_is_palindrome(self):
        self.assertTrue(m06.is_palindrome("racecar"))
        self.assertFalse(m06.is_palindrome("hello"))

    def test_reverse_string(self):
        self.assertEqual(m07.reverse_string("abc"), "cba")

    def test_count_vowels(self):
        self.assertEqual(m08.count_vowels("hello"), 2)
        self.assertEqual(m08.count_vowels("Rhythm"), 0)


if __name__ == "__main__":
    unittest.main()
