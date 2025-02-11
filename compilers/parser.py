from top import BinOp, UnOp, Float, Int, If, Parentheses, Program, VarDecl, VarReference, Assignment, AST
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
                    break
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
                    break
        return ast

    def parse_exp():
        l = parse_if()
        match t.peek(None):
            case OperatorToken('**'):
                next(t)
                r = parse_if()
                return BinOp("**", l, r)
            case _:
                return l

    def parse_if():
        if t.peek(None) != KeywordToken("if"):
            return parse_atom()
        next(t)  # consume "if"
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
        while t.peek(None) == KeywordToken("else"):
            next(t)  # consume "else"
            if t.peek(None) == KeywordToken("if"):
                next(t)  # consume "if"
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
        return If(cond, then_expr, elseif_branches, None)
    
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
                return UnOp('-', parse_atom())
            case KeywordToken(x) if x not in ["if", "else", "var"]:
                next(t)
                return VarReference(x)
        raise ParseError("Unexpected token in atom")

    def parse_statement():
        if t.peek(None) == KeywordToken("var"):
            next(t)  # consume "var"
            token = t.peek(None)
            if not (isinstance(token, KeywordToken) and token.w not in ["if", "else", "var"]):
                raise ParseError("Expected variable name after 'var'")
            var_name = token.w
            next(t)
            try:
                expect(OperatorToken('='))
            except ParseError:
                raise ParseError("Expected '=' after variable name in declaration")
            expr = parse_cmp()
            return VarDecl(var_name, expr)
        else:
            expr = parse_cmp()
            # Check for assignment if left-hand side is a variable reference.
            if isinstance(expr, VarReference) and t.peek(None) == OperatorToken('='):
                next(t)  # consume '='
                rhs = parse_cmp()
                return Assignment(expr.name, rhs)
            return expr

    def parse_program():
        statements = []
        while t.peek(None) is not None:
            statements.append(parse_statement())
            if t.peek(None) is not None:
                # Enforce semicolon between statements
                if t.peek(None) == OperatorToken(';'):
                    next(t)
                else:
                    raise ParseError("Missing semicolon between statements")
        return statements[0] if len(statements) == 1 else Program(statements)

    result = parse_program()
    return result
