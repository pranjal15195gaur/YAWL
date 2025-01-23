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
    elseif_branches: list
    elsee: AST


def e(tree: AST) -> int:
    match tree:
        case Int(v): return int(v)
        case Float(v): return float(v)
        case UnOp("-", expp): return -1 * e(expp)
        case BinOp("**", l, r): return e(l) ** e(r)
        case BinOp("*", l, r): return e(l) * e(r)
        case BinOp("/", l, r): return e(l) / e(r)
        case BinOp("+", l, r): return e(l) + e(r)
        case BinOp("-", l, r): return e(l) - e(r)
        case BinOp("<", l, r): return e(l) < e(r)
        case BinOp("<=", l, r): return e(l) <= e(r)
        case BinOp(">", l, r): return e(l) > e(r)
        case BinOp(">=", l, r): return e(l) >= e(r)
        case BinOp("==", l, r): return e(l) == e(r)
        case BinOp("!=", l, r): return e(l) != e(r)
        case Parentheses(expp): return e(expp)
        case If(cond, then, elseif_branches, elsee):
            if e(cond): 
                return e(then)
            for elseif_cond, elseif_then in elseif_branches:
                if e(elseif_cond):
                    return e(elseif_then)
            if elsee is not None:
                return e(elsee)
            return None
        case _: raise ValueError("Unsupported node type")