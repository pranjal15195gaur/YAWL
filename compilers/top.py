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

def e(tree: AST) -> int:
    match tree:
        case Int(v): return int(v)
        case Float(v): return float(v)
        case UnOp("-", expp): return -1 * e(expp)
        case BinOp(op, l, r):
            left_val = e(l)
            right_val = e(r)
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
                case _: raise ValueError(f"Unsupported binary operator: {op}")
        case Parentheses(expp): return e(expp)
        case If(cond, then, elseif_branches, elsee):
            if cond is None:
                raise ValueError("Condition missing in 'if' statement")
            for elseif_cond, elseif_then in elseif_branches:
                if elseif_cond is None:
                    raise ValueError("Condition missing in 'elseif' statement")
            if e(cond): 
                return e(then)
            for elseif_cond, elseif_then in elseif_branches:
                if e(elseif_cond):
                    return e(elseif_then)
            if elsee is not None:
                return e(elsee)
            return None
        case _: raise ValueError("Unsupported node type")