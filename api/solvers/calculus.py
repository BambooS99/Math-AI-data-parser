import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication,
    convert_xor,
)

# No symbol splitting, so words are never turned into products of letters. Allows implicit multiplication (e.g. 2x -> 2*x) and ^ as exponentiation (e.g. x^2 -> x**2)
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication,
    convert_xor,
)


def clean_expression(raw: str) -> str:
    """Strip common equation prefixes like 'y =', 'f(x) =', etc."""
    cleaned = raw.strip()
    prefixes = [
        "y =", "y=", 
        "f(x) =", "f(x)=", 
        "f(t) =", "f(t)=",
        "g(x) =", "g(x)=",
        "d/dx", "d/dt"
    ]
    for prefix in prefixes:
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
    return cleaned


def parse_math_expression(expr_str: str) -> sp.Expr:
    """Parse a mathematical expression string into a SymPy expression."""
    cleaned = clean_expression(expr_str)
    if not cleaned:
        raise ValueError("Expression cannot be empty.")
    try:
        parsed = parse_expr(
            cleaned, transformations=TRANSFORMATIONS, local_dict={"e": sp.E}
        )
    except Exception as exc:
        raise ValueError(f"Could not parse expression: {cleaned!r}") from None
    # Multi-letter symbols mean prose or an unsupported problem leaked in
    bad = sorted(s.name for s in parsed.free_symbols if len(s.name) > 1)
    if bad:
        raise ValueError(
            "That doesn't look like a single-variable expression I can "
            f"differentiate or integrate (unrecognized: {', '.join(bad)})."
        )
    return parsed


def solve_mixed_expression(expression: str) -> int | float:
    """Evaluate a numeric expression that may combine arithmetic operations."""
    expr = parse_math_expression(expression)
    if expr.free_symbols:
        raise ValueError("Mixed arithmetic expressions must not contain variables.")

    result = sp.simplify(expr)
    if result.is_finite is not True or result.is_real is not True:
        raise ValueError("Expression must evaluate to a finite real number.")
    if result.is_integer is True:
        return int(result)
    return float(result)


def solve_derivative(expression: str, variable: str = "x") -> tuple[str, list[str]]:
    """
    Compute the symbolic derivative of an expression with respect to a variable.
    Returns (result_string, steps).
    """
    expr = parse_math_expression(expression)
    var_symbol = sp.Symbol(variable)
    derivative = sp.diff(expr, var_symbol)
    result_str = str(derivative)

    steps = [
        f"Identify the function to differentiate: f({variable}) = {expr}",
        f"Apply differentiation with respect to {variable}: d/d{variable} [{expr}]",
        f"Derivative: {result_str}",
    ]

    return result_str, steps


def solve_integral(
    expression: str,
    variable: str = "x",
    lower_bound: float | int | None = None,
    upper_bound: float | int | None = None,
) -> tuple[str | int | float, list[str]]:
    """
    Compute the integral (definite or indefinite) of an expression with respect to a variable.
    Returns (result, steps).
    """
    expr = parse_math_expression(expression)
    var_symbol = sp.Symbol(variable)

    if lower_bound is not None and upper_bound is not None:
        definite_result = sp.integrate(expr, (var_symbol, lower_bound, upper_bound))
        
        # If the result is a clean number, format accordingly
        if hasattr(definite_result, "is_integer") and definite_result.is_integer:
            final_val: str | int | float = int(definite_result)
        elif hasattr(definite_result, "is_real") and definite_result.is_real and definite_result.is_number:
            final_val = float(definite_result)
        else:
            final_val = str(definite_result)

        antiderivative = sp.integrate(expr, var_symbol)
        steps = [
            f"Identify the integrand: f({variable}) = {expr}",
            f"Find the antiderivative: F({variable}) = {antiderivative}",
            f"Apply the Fundamental Theorem of Calculus: F({upper_bound}) - F({lower_bound})",
            f"Definite integral value: {final_val}",
        ]
        return final_val, steps

    # Indefinite integral
    antiderivative = sp.integrate(expr, var_symbol)
    result_str = f"{antiderivative} + C"
    steps = [
        f"Identify the integrand: f({variable}) = {expr}",
        f"Compute the indefinite integral: ∫ ({expr}) d{variable}",
        f"Antiderivative: {result_str} (where C is the constant of integration)",
    ]
    return result_str, steps
