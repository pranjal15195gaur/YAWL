import sys
sys.path.insert(1, '"D:/Sem-2/Compilers"')
from Top import BinOp, UnOp, Float, Int, If, Parentheses, AST
from Lexer import IntToken, FloatToken, OperatorToken, KeywordToken, ParenToken, Token, lex

class ParseError(Exception):
    pass

def parse(s: str) -> AST:
    from more_itertools import peekable
    t = peekable(lex(s))

    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise ParseError


    def parse_if():
        match t.peek(None):
            case KeywordToken("if"):
                next(t)
                cond = parse_cmp()
                expect(KeywordToken("then"))
                then = parse_if()

                elseif_branches = []
                while t.peek(None) == KeywordToken("elseif"):
                    next(t)
                    elseif_cond = parse_cmp()
                    expect(KeywordToken("then"))
                    elseif_then = parse_if()
                    elseif_branches.append((elseif_cond, elseif_then))
            
                if t.peek(None) == KeywordToken("else"):
                    next(t)
                    elsee = parse_cmp()
                else:
                    elsee = None
            
                expect(KeywordToken("end"))
                return If(cond, then, elseif_branches, elsee)
            case _:
                return parse_cmp()


    def parse_cmp():
        l = parse_add_sub()
        match t.peek(None):
            case OperatorToken('lt') | OperatorToken('lte') | OperatorToken('gt') | OperatorToken('gte') | OperatorToken('eq') | OperatorToken('neq'):
                op = t.peek(None).o
                next(t)
                r = parse_add_sub()
                return BinOp(op, l, r) 
            case _:
                return l

    def parse_add_sub():
        ast = parse_mul_div()
        while True:
            match t.peek(None):
                case OperatorToken('add'):
                    next(t)
                    ast = BinOp('add', ast, parse_mul_div())
                case OperatorToken('sub'):
                    next(t)
                    ast = BinOp('sub', ast, parse_mul_div())
                case _:
                    return ast

    def parse_mul_div():
        ast = parse_exp()
        while True:
            match t.peek(None):
                case OperatorToken('mul'):
                    next(t)
                    ast = BinOp("mul", ast, parse_exp())
                case OperatorToken('div'):
                    next(t)
                    ast = BinOp("div", ast, parse_exp())
                case _:
                    return ast

    def parse_exp():
        l = parse_atom()
        match t.peek(None):
            case OperatorToken('exp'):
                next(t)
                r = parse_exp()
                return BinOp("exp", l, r)
            case _:
                return l


    def parse_atom():
        match t.peek(None):
            case IntToken(v):
                next(t)
                return Int(v)
            case FloatToken(v):
                next(t)
                return Float(v)
            case KeywordToken('if'):
                return parse_if
            case ParenToken('('):
                next(t)
                expr = parse_cmp()
                expect(ParenToken(')'))
                return Parentheses(expr)
            case OperatorToken('neg'):
                next(t)
                val = parse_atom()
                return UnOp('neg', val)

    return parse_if()