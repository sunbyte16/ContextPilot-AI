import ast
import operator
import math
from typing import Dict, Any, Optional
from app.tools.base import BaseTool

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

ALLOWED_FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "ceil": math.ceil,
    "floor": math.floor,
    "pi": math.pi,
    "e": math.e,
}


class SafeEvaluator(ast.NodeVisitor):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise ValueError(f"Unsupported syntax: expression type {node.__class__.__name__} is not allowed")

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Constant of type {type(node.value)} is not allowed")

    def visit_Num(self, node):  # For python < 3.8 backwards compatibility
        return node.n

    def visit_UnaryOp(self, node):
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](self.visit(node.operand))
        raise ValueError(f"Unary operator {op_type} not allowed")

    def visit_BinOp(self, node):
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if op_type == ast.Pow and (right > 1000 or (isinstance(left, (int, float)) and abs(left) > 1e10)):
                raise ValueError("Exponentiation exceeds maximum safe limit")
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                raise ZeroDivisionError("Division by zero")
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Binary operator {op_type} not allowed")

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        func_name = node.func.id
        if func_name not in ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not in the allowed math functions list")
        func = ALLOWED_FUNCTIONS[func_name]
        args = [self.visit(arg) for arg in node.args]
        return func(*args)

    def visit_Name(self, node):
        if node.id in ALLOWED_FUNCTIONS and isinstance(ALLOWED_FUNCTIONS[node.id], (int, float)):
            return ALLOWED_FUNCTIONS[node.id]
        raise ValueError(f"Identifier '{node.id}' is not recognized")


class SafeCalculatorTool(BaseTool):
    tool_id = "safe_calculator"
    name = "Safe Mathematical Calculator"
    description = "Evaluates mathematical expressions safely using an AST parser without unrestricted execution."
    version = "1.0.0"
    risk_level = "LOW"
    requires_approval = False
    implementation_type = "local"

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate, e.g. '(1500 * 1.18) + sqrt(144)'"
                }
            },
            "required": ["expression"]
        }

    def get_output_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "expression": {"type": "string"},
                "result": {"type": "number"},
                "formatted": {"type": "string"}
            }
        }

    def execute(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        expr = params.get("expression", "").strip()
        if not expr:
            raise ValueError("Expression parameter cannot be empty.")
        if len(expr) > 500:
            raise ValueError("Expression length exceeds 500 characters limit.")

        parsed = ast.parse(expr, mode='eval')
        evaluator = SafeEvaluator()
        result = evaluator.visit(parsed)

        return {
            "success": True,
            "expression": expr,
            "result": result,
            "formatted": f"{result:,.4f}".rstrip('0').rstrip('.') if isinstance(result, float) else f"{result:,}"
        }
