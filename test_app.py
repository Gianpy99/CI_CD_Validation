import unittest
from app import add, subtract, multiply, divide, calculate_percentage, Calculator

class TestMathFunctions(unittest.TestCase):
    """Test cases for mathematical functions"""
    
    def test_add(self):
        """Test addition function"""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-3, 3), 0)
        self.assertEqual(add(-3, 4), 1)
        self.assertEqual(add(-3, 5), 2)
        
    def test_subtract(self):
        """Test subtraction function"""
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(-5, -3), -2)
        
    def test_multiply(self):
        """Test multiplication function"""
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 5), -10)
        self.assertEqual(multiply(0, 100), 0)
        
    def test_divide(self):
        """Test division function"""
        self.assertEqual(divide(15, 3), 5)
        self.assertEqual(divide(-10, 2), -5)
        self.assertAlmostEqual(divide(1, 3), 0.333333, places=6)
        
    def test_divide_by_zero(self):
        """Test division by zero raises exception"""
        with self.assertRaises(ValueError) as context:
            divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero!")
        
    def test_calculate_percentage(self):
        """Test percentage calculation"""
        self.assertEqual(calculate_percentage(25, 100), 25.0)
        self.assertEqual(calculate_percentage(50, 200), 25.0)
        self.assertEqual(calculate_percentage(0, 100), 0.0)
        
    def test_calculate_percentage_zero_total(self):
        """Test percentage calculation with zero total"""
        with self.assertRaises(ValueError) as context:
            calculate_percentage(10, 0)
        self.assertEqual(str(context.exception), "Total cannot be zero!")

class TestCalculator(unittest.TestCase):
    """Test cases for Calculator class"""
    
    def setUp(self):
        """Set up test calculator instance"""
        self.calc = Calculator()
        
    def test_add_to_history(self):
        """Test adding operations to history"""
        self.calc.add_to_history("2 + 3", 5)
        self.assertEqual(len(self.calc.get_history()), 1)
        self.assertEqual(self.calc.get_history()[0], "2 + 3 = 5")
        
    def test_get_history(self):
        """Test getting calculation history"""
        self.calc.add_to_history("5 * 4", 20)
        self.calc.add_to_history("10 / 2", 5)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertIn("5 * 4 = 20", history)
        self.assertIn("10 / 2 = 5", history)
        
    def test_clear_history(self):
        """Test clearing calculation history"""
        self.calc.add_to_history("1 + 1", 2)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)

if __name__ == "__main__":
    unittest.main()
