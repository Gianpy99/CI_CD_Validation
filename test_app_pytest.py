import pytest
from app import add, subtract, multiply, divide, calculate_percentage, Calculator

class TestAdd:
    """Test class for the add function"""
    
    def test_add_positive_numbers(self):
        """Test addition of positive numbers"""
        assert add(2, 3) == 5
        assert add(10, 15) == 25
        
    def test_add_negative_numbers(self):
        """Test addition of negative numbers"""
        assert add(-1, -1) == -2
        assert add(-5, -3) == -8
        
    def test_add_mixed_numbers(self):
        """Test addition of positive and negative numbers"""
        assert add(-1, 1) == 0
        assert add(-3, 3) == 0
        assert add(-3, 4) == 1
        assert add(-3, 5) == 2
        
    def test_add_zero(self):
        """Test addition with zero"""
        assert add(0, 0) == 0
        assert add(5, 0) == 5
        assert add(0, -5) == -5
        
    def test_add_large_numbers(self):
        """Test addition of large numbers"""
        assert add(1000000, 2000000) == 3000000
        assert add(-1000000, 1000000) == 0

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, -50, 50),
        (2.5, 3.5, 6.0),
    ])
    def test_add_parametrized(self, a, b, expected):
        """Parametrized test for various input combinations"""
        assert add(a, b) == expected

class TestMultiply:
    """Test class for the multiply function - this will catch the bug!"""
    
    def test_multiply_positive(self):
        """Test multiplication of positive numbers"""
        assert multiply(3, 4) == 12  # This will fail! (7 != 12)
        assert multiply(5, 6) == 30  # This will fail! (11 != 30)
        
    def test_multiply_with_zero(self):
        """Test multiplication with zero"""
        assert multiply(5, 0) == 0   # This will fail! (5 != 0)
        assert multiply(0, 10) == 0  # This will fail! (10 != 0)
        
    def test_multiply_negative(self):
        """Test multiplication with negative numbers"""
        assert multiply(-2, 3) == -6  # This will fail! (1 != -6)
        assert multiply(-4, -5) == 20 # This will fail! (-9 != 20)

class TestAllFunctions:
    """Integration tests for all calculator functions"""
    
    def test_basic_operations(self):
        """Test basic mathematical operations"""
        assert add(2, 3) == 5
        assert subtract(10, 4) == 6
        assert multiply(3, 7) == 21  # This will fail! (10 != 21)
        assert divide(15, 3) == 5
        
    def test_calculator_class(self):
        """Test Calculator class functionality"""
        calc = Calculator()
        calc.add_to_history("test", 42)
        assert len(calc.get_history()) == 1
        assert "test = 42" in calc.get_history()[0]
