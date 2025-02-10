# parser.py
from top import BinOp, UnOp, Float, Int, If, Parentheses, AST, Var, Assign, Program
from lexer import IntToken, FloatToken, OperatorToken, KeywordToken, ParenToken, IdentifierToken, Token, lex

class ParseError(Exception):
    pass

def parse(s: str) -> AST:
    from more_itertools import peekable
    tokens = peekable(lex(s))

    def expect(what: Token):
        if tokens.peek(None) == what:
            next(tokens)
            return
        raise ParseError(f"Expected {what}, but got {tokens.peek(None)}")

    def parse_cmp():
        l = parse_add_sub()
        match tokens.peek(None):
            case OperatorToken('<') | OperatorToken('<=') | OperatorToken('>') | OperatorToken('>=') | OperatorToken('==') | OperatorToken('!='):
                op = tokens.peek(None).o
                next(tokens)
                r = parse_add_sub()
                return BinOp(op, l, r)
            case _:
                return l

    def parse_add_sub():
        ast = parse_mul_div()
        while True:
            match tokens.peek(None):
                case OperatorToken('+'):
                    next(tokens)
                    ast = BinOp('+', ast, parse_mul_div())
                case OperatorToken('-'):
                    next(tokens)
                    ast = BinOp('-', ast, parse_mul_div())
                case _:
                    return ast

    def parse_mul_div():
        ast = parse_exp()
        while True:
            match tokens.peek(None):
                case OperatorToken('*'):
                    next(tokens)
                    ast = BinOp('*', ast, parse_exp())
                case OperatorToken('/'):
                    next(tokens)
                    ast = BinOp('/', ast, parse_exp())
                case _:
                    return ast

    def parse_exp():
        l = parse_if()
        match tokens.peek(None):
            case OperatorToken('**'):
                next(tokens)
                r = parse_if()
                return BinOp("**", l, r)
            case _:
                return l

    def parse_if():
        if tokens.peek(None) != KeywordToken("if"):
            return parse_atom()
        next(tokens)  # consume "if"
        cond = parse_cmp()
        if cond is None:
            raise ParseError("Missing condition after 'if'")
        try:
            expect(OperatorToken('{'))
        except ParseError:
            raise ParseError("Expected '{' after 'if' condition")
        then_expr = parse_cmp()
        try:
            expect(OperatorToken('}'))
        except ParseError:
            raise ParseError("Missing closing '}' after 'if' block")

        elseif_branches = []
        while True:
            if tokens.peek(None) == KeywordToken("else"):
                next(tokens)  # consume "else"
                if tokens.peek(None) == KeywordToken("if"):
                    next(tokens)  # consume "if"
                    elseif_cond = parse_cmp()
                    if elseif_cond is None:
                        raise ParseError("Missing condition after 'else if'")
                    try:
                        expect(OperatorToken('{'))
                    except ParseError:
                        raise ParseError("Expected '{' after 'else if' condition")
                    elseif_then = parse_cmp()
                    try:
                        expect(OperatorToken('}'))
                    except ParseError:
                        raise ParseError("Missing closing '}' after 'else if' block")
                    elseif_branches.append((elseif_cond, elseif_then))
                else:
                    try:
                        expect(OperatorToken('{'))
                    except ParseError:
                        raise ParseError("Expected '{' after 'else'")
                    else_expr = parse_cmp()
                    try:
                        expect(OperatorToken('}'))
                    except ParseError:
                        raise ParseError("Missing closing '}' after 'else' block")
                    return If(cond, then_expr, elseif_branches, else_expr)
            else:
                return If(cond, then_expr, elseif_branches, None)

    def parse_atom():
        match tokens.peek(None):
            case IntToken(v):
                next(tokens)
                return Int(v)
            case FloatToken(v):
                next(tokens)
                return Float(v)
            case IdentifierToken(name):
                next(tokens)
                return Var(name)
            case ParenToken('('):
                next(tokens)
                # Allow assignments inside parentheses
                expr = parse_assignment()
                expect(ParenToken(')'))
                return Parentheses(expr)
            case OperatorToken('-'):
                next(tokens)
                val = parse_atom()
                return UnOp('-', val)
            case KeywordToken("if"):
                return parse_if()
            case _:
                raise ParseError(f"Unexpected token: {tokens.peek(None)}")

    # Assignment production (right-associative)
    def parse_assignment():
        left = parse_cmp()
        if isinstance(left, Var) and tokens.peek(None) == OperatorToken('='):
            next(tokens)  # consume '='
            right = parse_assignment()
            return Assign(left.name, right)
        return left

    # Top-level production: a program is a sequence of statements
    def parse_program():
        statements = []
        while tokens.peek(None) is not None:
            stmt = parse_assignment()
            statements.append(stmt)
            # Consume a semicolon if one is present (as a statement separator)
            if tokens.peek(None) and isinstance(tokens.peek(None), OperatorToken) and tokens.peek(None).o == ';':
                next(tokens)
            else:
                raise ParseError("Missing semicolon after expression or statement")
        return Program(statements)

    return parse_program()
