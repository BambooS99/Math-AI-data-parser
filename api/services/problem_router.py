from api.solvers import arithmetic, calculus
from api import schemas

def _extract_expression(classification: schemas.ClassificationResult) -> str | None:
    if classification.expression and classification.expression.strip():
        return classification.expression.strip()
    if isinstance(classification.normalized_input, str) and classification.normalized_input.strip():
        return classification.normalized_input.strip()
    return None

"""router function (/router)"""
def route_problem(classification: schemas.ClassificationResult) -> schemas.SolverResult:
    if classification.problem_type == "mixed_expression":
        expr = _extract_expression(classification)
        if not expr:
            return schemas.SolverResult(
                solver_used="mixed_expression",
                success=False,
                error_message="No mathematical expression provided to evaluate.",
            )
        try:
            return schemas.SolverResult(
                solver_used="mixed_expression",
                success=True,
                result=calculus.solve_mixed_expression(expr),
            )
        except ValueError as e:
            return schemas.SolverResult(
                solver_used="mixed_expression",
                success=False,
                error_message=f"Could not evaluate that expression. {e}",
            )

    if classification.problem_type == "addition":
        if not isinstance(classification.normalized_input, list):
            return schemas.SolverResult(
                solver_used="addition",
                success=False,
                error_message="Invalid operands for addition.",
            )
        return schemas.SolverResult(
            solver_used="addition",
            success=True,
            result=arithmetic.add(classification.normalized_input),
        )

    if classification.problem_type == "multiplication":
        if not isinstance(classification.normalized_input, list):
            return schemas.SolverResult(
                solver_used="multiplication",
                success=False,
                error_message="Invalid operands for multiplication.",
            )
        return schemas.SolverResult(
            solver_used="multiplication",
            success=True,
            result=arithmetic.multiplication(classification.normalized_input),
        )

    if classification.problem_type == "subtraction":
        if not isinstance(classification.normalized_input, list):
            return schemas.SolverResult(
                solver_used="subtraction",
                success=False,
                error_message="Invalid operands for subtraction.",
            )
        return schemas.SolverResult(
            solver_used="subtraction",
            success=True,
            result=arithmetic.subtract(classification.normalized_input),
        )

    if classification.problem_type == "division":
        if not isinstance(classification.normalized_input, list):
            return schemas.SolverResult(
                solver_used="division",
                success=False,
                error_message="Invalid operands for division.",
            )
        try:
            return schemas.SolverResult(
                solver_used="division",
                success=True,
                result=arithmetic.divide(classification.normalized_input),
            )
        except ZeroDivisionError:
            return schemas.SolverResult(
                solver_used="division",
                success=False,
                error_message="Division by zero is undefined.",
            )

    if classification.problem_type in ("derivative", "differentiation"):
        expr = _extract_expression(classification)
        if not expr:
            return schemas.SolverResult(
                solver_used="calculus_derivative",
                success=False,
                error_message="No mathematical expression provided to differentiate.",
            )
        try:
            result_str, steps = calculus.solve_derivative(
                expression=expr,
                variable=classification.variable or "x",
            )
            return schemas.SolverResult(
                solver_used="calculus_derivative",
                success=True,
                result=result_str,
                steps=steps,
            )
        except Exception as e:
            return schemas.SolverResult(
                solver_used="calculus_derivative",
                success=False,
                error_message=f"Could not compute that derivative. {e}",
            )

    if classification.problem_type in ("integral", "integration"):
        expr = _extract_expression(classification)
        if not expr:
            return schemas.SolverResult(
                solver_used="calculus_integral",
                success=False,
                error_message="No mathematical expression provided to integrate.",
            )
        try:
            result_val, steps = calculus.solve_integral(
                expression=expr,
                variable=classification.variable or "x",
                lower_bound=classification.lower_bound,
                upper_bound=classification.upper_bound,
            )
            return schemas.SolverResult(
                solver_used="calculus_integral",
                success=True,
                result=result_val,
                steps=steps,
            )
        except Exception as e:
            return schemas.SolverResult(
                solver_used="calculus_integral",
                success=False,
                error_message=f"Could not compute that integral. {e}",
            )

    return schemas.SolverResult(
        solver_used="N/A",
        success=False,
        error_message="Please try again later. This feature is not currently supported",
    )
