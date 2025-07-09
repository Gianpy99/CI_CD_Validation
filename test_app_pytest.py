import pytest
from app import add

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
