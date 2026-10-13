import os
import unittest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-not-real")

from api.main import route_problem
from api.schemas import ClassificationResult


class TestRouteProblem(unittest.TestCase):
    def test_mixed_expression_uses_sympy_solver(self):
        classification = ClassificationResult(
            problem_type="mixed_expression",
            expression="2 + 3 * (4 - 1)",
            confidence=1.0,
            needs_clarification=False,
        )

        result = route_problem(classification)

        self.assertEqual(result.solver_used, "mixed_expression")
        self.assertTrue(result.success)
        self.assertEqual(result.result, 11)
        self.assertIsNone(result.error_message)

    def test_addition_uses_arithmetic_solver(self):
        classification = ClassificationResult(
            problem_type="addition",
            normalized_input=[2, 3],
            confidence=1.0,
            needs_clarification=False,
        )

        result = route_problem(classification)

        self.assertEqual(result.solver_used, "addition")
        self.assertTrue(result.success)
        self.assertEqual(result.result, 5)
        self.assertIsNone(result.error_message)

    def test_subtraction_uses_arithmetic_solver(self):
        classification = ClassificationResult(
            problem_type="subtraction",
            normalized_input=[8, 3],
            confidence=1.0,
            needs_clarification=False,
        )

        result = route_problem(classification)

        self.assertEqual(result.solver_used, "subtraction")
        self.assertTrue(result.success)
        self.assertEqual(result.result, 5)
        self.assertIsNone(result.error_message)

    def test_derivative_uses_calculus_solver(self):
        classification = ClassificationResult(
            problem_type="derivative",
            expression="3x^2 + 2x",
            variable="x",
            confidence=1.0,
            needs_clarification=False,
        )

        result = route_problem(classification)

        self.assertEqual(result.solver_used, "calculus_derivative")
        self.assertTrue(result.success)
        self.assertEqual(result.result, "6*x + 2")
        self.assertIsNotNone(result.steps)
        self.assertIsNone(result.error_message)

    def test_integral_uses_calculus_solver(self):
        classification = ClassificationResult(
            problem_type="integral",
            expression="2x",
            variable="x",
            confidence=1.0,
            needs_clarification=False,
        )

        result = route_problem(classification)

        self.assertEqual(result.solver_used, "calculus_integral")
        self.assertTrue(result.success)
        self.assertEqual(result.result, "x**2 + C")
        self.assertIsNotNone(result.steps)
        self.assertIsNone(result.error_message)

    def test_unsupported_type_returns_error(self):
        classification = ClassificationResult(
            problem_type="matrix_multiplication",
            normalized_input=[],
            confidence=1.0,
            needs_clarification=False,
        )

        result = route_problem(classification)

        self.assertEqual(result.solver_used, "N/A")
        self.assertFalse(result.success)
        self.assertIsNone(result.result)
        self.assertIsNotNone(result.error_message)


if __name__ == "__main__":
    unittest.main()
