import unittest
from app import add

class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-3, 3), 0)
        self.assertEqual(add(-3, 4), 1)
        self.assertEqual(add(-3, 5), 2)
        self.assertEqual(add(-3, 6), 2)

if __name__ == "__main__":
    unittest.main()
