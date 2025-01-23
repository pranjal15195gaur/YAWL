from top import BinOp, UnOp, Float, Int, If, Parentheses, AST
from lexer import IntToken, FloatToken, OperatorToken, KeywordToken, ParenToken, Token, lex

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
        # expect an "if"
        next(t)  # consume KeywordToken("if")
        cond = parse_cmp()
        expect(OperatorToken('{'))
        then_expr = parse_cmp()
        expect(OperatorToken('}'))

        elseif_branches = []
        # handle chained "else if"
        while True:
            if t.peek(None) == KeywordToken("else"):
                next(t)  # consume "else"
                if t.peek(None) == KeywordToken("if"):
                    next(t)  # consume "if"
                    elseif_cond = parse_cmp()
                    expect(OperatorToken('{'))
                    elseif_then = parse_cmp()
                    expect(OperatorToken('}'))
                    elseif_branches.append((elseif_cond, elseif_then))
                else:
                    expect(OperatorToken('{'))
                    else_expr = parse_cmp()
                    expect(OperatorToken('}'))
                    return If(cond, then_expr, elseif_branches, else_expr)
            else:
                return If(cond, then_expr, elseif_branches, None)


    def parse_cmp():
        l = parse_add_sub()
        match t.peek(None):
            case OperatorToken('<') | OperatorToken('<=') | OperatorToken('>') | OperatorToken('>=') | OperatorToken('==') | OperatorToken('!='):
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
                case OperatorToken('+'):
                    next(t)
                    ast = BinOp('+', ast, parse_mul_div())
                case OperatorToken('-'):
                    next(t)
                    ast = BinOp('-', ast, parse_mul_div())
                case _:
                    return ast

    def parse_mul_div():
        ast = parse_exp()
        while True:
            match t.peek(None):
                case OperatorToken('*'):
                    next(t)
                    ast = BinOp("*", ast, parse_exp())
                case OperatorToken('/'):
                    next(t)
                    ast = BinOp("/", ast, parse_exp())
                case _:
                    return ast

    def parse_exp():
        l = parse_atom()
        match t.peek(None):
            case OperatorToken('**'):
                next(t)
                r = parse_exp()
                return BinOp("**", l, r)
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

            case ParenToken('('):
                next(t)
                expr = parse_cmp()
                expect(ParenToken(')'))
                return Parentheses(expr)
            case OperatorToken('-'):
                next(t)
                val = parse_atom()
                return UnOp('-', val)
            case KeywordToken("if"):
                return parse_if()

    return parse_if()