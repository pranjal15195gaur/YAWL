from dataclasses import dataclass

class AST:
    pass

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

# NEW: AST node for a variable reference
@dataclass
class Var(AST):
    name: str

# NEW: AST node for an assignment expression
@dataclass
class Assign(AST):
    name: str
    value: AST

# The evaluator now takes an optional environment dictionary.
def e(tree: AST, env=None):
    if env is None:
        env = {}
    match tree:
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
            return -1 * e(expp, env)
        case BinOp(op, l, r):
            left_val = e(l, env)
            right_val = e(r, env)
            match op:
                case "**": return left_val ** right_val
                case "*": return left_val * right_val
                case "/": return left_val / right_val
                case "+": return left_val + right_val
                case "-": return left_val - right_val
                case "<": return left_val < right_val
                case "<=": return left_val <= right_val
                case ">": return left_val > right_val
                case ">=": return left_val >= right_val
                case "==": return left_val == right_val
                case "!=": return left_val != right_val
                case "=":  # Should not occur because assignment is handled by the Assign node.
                    raise ValueError("Assignment operator should be handled by an Assign node")
                case _:
                    raise ValueError(f"Unsupported binary operator: {op}")
        case Parentheses(expp):
            return e(expp, env)
        case If(cond, then, elseif_branches, elsee):
            if cond is None:
                raise ValueError("Condition missing in 'if' statement")
            for elseif_cond, elseif_then in elseif_branches:
                if elseif_cond is None:
                    raise ValueError("Condition missing in 'elseif' statement")
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
