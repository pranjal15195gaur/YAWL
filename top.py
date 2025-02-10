# top.py
from dataclasses import dataclass

class AST:
    pass

# Top-level program node: holds a list of statements.
@dataclass
class Program(AST):
    statements: list[AST]

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST

@dataclass
class UnOp(AST):
    op: str
    num: AST

@dataclass
class Float(AST):
    val: str

@dataclass
class Int(AST):
    val: str

@dataclass
class Parentheses(AST):
    val: AST

@dataclass
class If(AST):
    cond: AST
    then: AST
    elseif_branches: list[tuple[AST, AST]]
    elsee: AST

# Variable reference node
@dataclass
class Var(AST):
    name: str

# Assignment node (only allowed when the left side is a variable)
@dataclass
class Assign(AST):
    name: str
    value: AST

# Evaluator: evaluates the AST in an environment (a dictionary)
def e(tree: AST, env=None):
    if env is None:
        env = {}
    match tree:
        case Program(statements):
            result = None
            for stmt in statements:
                result = e(stmt, env)
            return result
        case Int(v):
            return int(v)
        case Float(v):
            return float(v)
        case Var(name):
            if name in env:
                return env[name]
            else:
                raise ValueError(f"Undefined variable: {name}")
        case Assign(name, value):
            val = e(value, env)
            env[name] = val
            return val
        case UnOp("-", expp):
            return -e(expp, env)
        case BinOp(op, l, r):
            left_val = e(l, env)
            right_val = e(r, env)
            match op:
                case "**": return left_val ** right_val
                case "*":  return left_val * right_val
                case "/":  return left_val / right_val
                case "+":  return left_val + right_val
                case "-":  return left_val - right_val
                case "<":  return left_val < right_val
                case "<=": return left_val <= right_val
                case ">":  return left_val > right_val
                case ">=": return left_val >= right_val
                case "==": return left_val == right_val
                case "!=": return left_val != right_val
                case _:
                    raise ValueError(f"Unsupported binary operator: {op}")
        case Parentheses(expp):
            return e(expp, env)
        case If(cond, then, elseif_branches, elsee):
            if e(cond, env):
                return e(then, env)
            for elseif_cond, elseif_then in elseif_branches:
                if e(elseif_cond, env):
                    return e(elseif_then, env)
            if elsee is not None:
                return e(elsee, env)
            return None
        case _:
            raise ValueError("Unsupported node type")
