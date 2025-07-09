def add(a, b):
    """Add two numbers together"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

def calculate_percentage(value, total):
    """Calculate percentage of value from total"""
    if total == 0:
        raise ValueError("Total cannot be zero!")
    return (value / total) * 100

class Calculator:
    """A simple calculator class"""
    
    def __init__(self):
        self.history = []
    
    def add_to_history(self, operation, result):
        """Add operation to calculation history"""
        self.history.append(f"{operation} = {result}")
    
    def get_history(self):
        """Get calculation history"""
        return self.history
    
    def clear_history(self):
        """Clear calculation history"""
        self.history = []

if __name__ == "__main__":
    print("=== Calculator Demo ===")
    print("2 + 3 =", add(2, 3))
    print("10 - 4 =", subtract(10, 4))
    print("3 * 7 =", multiply(3, 7))
    print("15 / 3 =", divide(15, 3))
    print("25% of 200 =", calculate_percentage(25, 100) * 200 / 100)
    
    # Test calculator class
    calc = Calculator()
    result = add(5, 10)
    calc.add_to_history("5 + 10", result)
    print("\nCalculation history:", calc.get_history())
