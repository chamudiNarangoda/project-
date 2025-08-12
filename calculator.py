"""Simple, safe CLI calculator.

Supports: +, -, *, /, //, %, **, parentheses, unary +/-. Uses Python's AST to safely
evaluate expressions without executing arbitrary code.

Usage:
  - One-shot: python3 calculator.py "1 + 2*3 - (4/5)"
  - REPL:     python3 calculator.py

Exit REPL with Ctrl-D, Ctrl-C, or by typing: exit, quit
"""
from __future__ import annotations

import argparse
import ast
import math
import sys
from typing import Union, Any


Number = Union[int, float]


class SafeEvaluator(ast.NodeVisitor):
    """Evaluate a restricted subset of Python expressions representing arithmetic.

    Allowed constructs:
      - Numbers: int and float literals
      - Binary ops: +, -, *, /, //, %, **
      - Unary ops: +, -
      - Parentheses (by virtue of AST structure)

    Disallowed: names, attribute access, calls, comprehensions, bool ops, comparisons, etc.
    """

    def visit(self, node: ast.AST) -> Number:  # type: ignore[override]
        return super().visit(node)  # type: ignore[return-value]

    def visit_Expression(self, node: ast.Expression) -> Number:  # type: ignore[override]
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> Number:  # type: ignore[override]
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op

        if isinstance(op, ast.Add):
            return left + right
        if isinstance(op, ast.Sub):
            return left - right
        if isinstance(op, ast.Mult):
            return left * right
        if isinstance(op, ast.Div):
            return left / right
        if isinstance(op, ast.FloorDiv):
            # Ensure Python's floor division behavior for negative numbers
            return left // right
        if isinstance(op, ast.Mod):
            return left % right
        if isinstance(op, ast.Pow):
            # Prevent extremely large exponentiations from hanging
            return self._safe_pow(left, right)

        raise ValueError(f"Unsupported binary operator: {type(op).__name__}")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Number:  # type: ignore[override]
        operand = self.visit(node.operand)
        op = node.op
        if isinstance(op, ast.UAdd):
            return +operand
        if isinstance(op, ast.USub):
            return -operand
        raise ValueError(f"Unsupported unary operator: {type(op).__name__}")

    def visit_Constant(self, node: ast.Constant) -> Number:  # type: ignore[override]
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only int and float literals are allowed")

    # For Python <3.8 compatibility where numbers were ast.Num; safe to include
    def visit_Num(self, node: ast.Num) -> Number:  # type: ignore[override]
        return node.n  # type: ignore[return-value]

    def generic_visit(self, node: ast.AST) -> Any:  # type: ignore[override]
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    @staticmethod
    def _safe_pow(base: Number, exponent: Number) -> Number:
        # Disallow non-integer exponents for negative bases when resulting in complex numbers
        if isinstance(base, (int, float)) and isinstance(exponent, (int, float)):
            # Soft limits to avoid pathological computations
            max_abs_base = 1e6
            max_abs_exponent = 1e4
            if abs(base) > max_abs_base:
                raise ValueError("Base too large for exponentiation")
            if abs(exponent) > max_abs_exponent:
                raise ValueError("Exponent too large for exponentiation")

            # If base is negative and exponent is fractional, result would be complex
            if base < 0 and not float(exponent).is_integer():
                raise ValueError("Negative base to a fractional power is not supported")

        return base ** exponent


def evaluate_expression(expression: str) -> Number:
    """Parse and evaluate an arithmetic expression safely.

    Raises ValueError on invalid expressions or disallowed constructs.
    """
    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc.msg}") from exc

    evaluator = SafeEvaluator()
    try:
        result = evaluator.visit(parsed)
    except ZeroDivisionError as exc:
        raise ValueError("Division by zero") from exc

    # Normalize int-like floats to ints for cleaner output
    if isinstance(result, float) and math.isfinite(result) and float(result).is_integer():
        return int(result)
    return result


def run_repl() -> int:
    prompt = "calc> "
    try:
        while True:
            try:
                line = input(prompt).strip()
            except EOFError:
                print()  # newline on Ctrl-D
                return 0

            if line.lower() in {"exit", "quit"}:
                return 0
            if not line:
                continue

            try:
                value = evaluate_expression(line)
                print(value)
            except ValueError as exc:
                print(f"Error: {exc}")
    except KeyboardInterrupt:
        print()  # newline on Ctrl-C
        return 130


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Simple safe calculator")
    parser.add_argument(
        "expression",
        nargs="?",
        help="Arithmetic expression to evaluate. If omitted, starts interactive REPL.",
    )
    args = parser.parse_args(argv)

    if args.expression is None:
        return run_repl()

    try:
        value = evaluate_expression(args.expression)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    # Print plain result for easy piping
    print(value)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))