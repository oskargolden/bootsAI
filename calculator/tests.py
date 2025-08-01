
import unittest

class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.assertEqual(self.calculator.add(2, 3), 5)
        self.assertEqual(self.calculator.add(-1, 1), 0)
        self.assertEqual(self.calculator.add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(self.calculator.subtract(5, 2), 3)
        self.assertEqual(self.calculator.subtract(1, -1), 2)
        self.assertEqual(self.calculator.subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(self.calculator.multiply(2, 3), 6)
        self.assertEqual(self.calculator.multiply(-1, 1), -1)
        self.assertEqual(self.calculator.multiply(-1, -1), 1)

    def test_divide(self):
        self.assertEqual(self.calculator.divide(6, 3), 2)
        self.assertEqual(self.calculator.divide(1, 2), 0.5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.divide(1, 0)
    def test_add_negative_numbers(self):
        self.assertEqual(self.calculator.add(-5, -3), -8)

    def test_subtract_negative_result(self):
        self.assertEqual(self.calculator.subtract(3, 5), -2)

    def test_multiply_by_zero(self):
        self.assertEqual(self.calculator.multiply(5, 0), 0)

    def test_divide_negative_numbers(self):
        self.assertEqual(self.calculator.divide(-6, -2), 3)

if __name__ == '__main__':
    unittest.main(verbosity=2)
