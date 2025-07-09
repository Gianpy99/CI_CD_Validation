import pytest
from app import add, subtract, multiply, divide, calculate_percentage, Calculator

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(-3, 3) == 0
    assert add(-3, 4) == 1
    assert add(-3, 5) == 2

def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(0, 5) == -5
    assert subtract(-5, -3) == -2

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 5) == -10
    assert multiply(0, 100) == 0

def test_divide():
    assert divide(15, 3) == 5
    assert divide(-10, 2) == -5
    assert round(divide(1, 3), 6) == 0.333333

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero!"):
        divide(10, 0)

def test_calculate_percentage():
    assert calculate_percentage(25, 100) == 25.0
    assert calculate_percentage(50, 200) == 25.0
    assert calculate_percentage(0, 100) == 0.0

def test_calculate_percentage_zero_total():
    with pytest.raises(ValueError, match="Total cannot be zero!"):
        calculate_percentage(10, 0)

def test_calculator_add_to_history():
    calc = Calculator()
    calc.add_to_history("2 + 3", 5)
    assert len(calc.get_history()) == 1
    assert calc.get_history()[0] == "2 + 3 = 5"

def test_calculator_get_history():
    calc = Calculator()
    calc.add_to_history("5 * 4", 20)
    calc.add_to_history("10 / 2", 5)
    history = calc.get_history()
    assert len(history) == 2
    assert "5 * 4 = 20" in history
    assert "10 / 2 = 5" in history

def test_calculator_clear_history():
    calc = Calculator()
    calc.add_to_history("1 + 1", 2)
    calc.clear_history()
    assert len(calc.get_history()) == 0
