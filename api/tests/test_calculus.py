import unittest

from api.solvers.calculus import solve_derivative, solve_integral, clean_expression, parse_math_expression


class TestCalculus(unittest.TestCase):
    def test_clean_expression(self):
        self.assertEqual(clean_expression("f(x) = 3x^2 + 2"), "3x^2 + 2")
        self.assertEqual(clean_expression("y = sin(x)"), "sin(x)")
        self.assertEqual(clean_expression("d/dx 4x"), "4x")

    def test_solve_derivative_polynomial(self):
        result, steps = solve_derivative("3x^2 + 2x - 5", variable="x")
        self.assertEqual(result, "6*x + 2")
        self.assertTrue(len(steps) >= 2)

    def test_solve_derivative_trigonometric(self):
        result, steps = solve_derivative("sin(x)", variable="x")
        self.assertEqual(result, "cos(x)")

    def test_solve_derivative_custom_variable(self):
        result, steps = solve_derivative("4t^3 - t", variable="t")
        self.assertEqual(result, "12*t**2 - 1")

    def test_solve_integral_indefinite(self):
        result, steps = solve_integral("3x^2 + 2x", variable="x")
        self.assertEqual(result, "x**3 + x**2 + C")
        self.assertTrue(any("+ C" in s for s in steps))

    def test_solve_integral_definite(self):
        result, steps = solve_integral("2x", variable="x", lower_bound=0, upper_bound=3)
        self.assertEqual(result, 9)
        self.assertTrue(len(steps) >= 3)

    def test_solve_integral_definite_fractional(self):
        result, steps = solve_integral("x", variable="x", lower_bound=0, upper_bound=1)
        self.assertIn(str(result), ["1/2", "0.5"])

    def test_invalid_expression_raises_error(self):
        with self.assertRaises(Exception):
            solve_derivative("+++---", variable="x")


if __name__ == "__main__":
    unittest.main()
