from collections.abc import Iterator
from dataclasses import dataclass

# ...existing code...

def parse_expression(tokens: Iterator[Token]) -> AST:
    token = next(tokens, None)
    if isinstance(token, IntToken):
        return Int(token.v)
    elif isinstance(token, FloatToken):
        return Float(token.v)
    elif isinstance(token, OperatorToken):
        # Handle unary operators
        if token.o in '+-':
            return UnOp(token.o, parse_expression(tokens))
        # Handle binary operators
        left = parse_expression(tokens)
        right = parse_expression(tokens)
        return BinOp(token.o, left, right)
    elif isinstance(token, KeywordToken) and token.w == 'if':
        cond = parse_expression(tokens)
        then = parse_expression(tokens)
        elseif_branches = []
        elsee = None
        while True:
            token = next(tokens, None)
            if token is None:
                break
            if isinstance(token, KeywordToken) and token.w == 'else':
                token = next(tokens, None)
                if token is not None and token.w == 'if':
                    cond = parse_expression(tokens)
                    then = parse_expression(tokens)
                    elseif_branches.append((cond, then))
                else:
                    elsee = parse_expression(tokens)
                    break
        return If(cond, then, elseif_branches, elsee)
    elif isinstance(token, ParenToken):
        if token.w == '(':
            expr = parse_expression(tokens)
            next(tokens)  # Consume the closing parenthesis
            return Parentheses(expr)
    raise ValueError(f"Unexpected token: {token}")
# ...existing code...
