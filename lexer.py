# lexer.py
from collections.abc import Iterator
from dataclasses import dataclass

class Token:
    pass

@dataclass
class IntToken(Token):
    v: str

@dataclass
class FloatToken(Token):
    v: str

@dataclass
class OperatorToken(Token):
    o: str

@dataclass
class KeywordToken(Token):
    w: str

@dataclass
class ParenToken(Token):
    w: str

# NEW: Token for identifiers (variable names)
@dataclass
class IdentifierToken(Token):
    name: str

def lex(s: str) -> Iterator[Token]:
    i = 0
    while True:
        # Skip whitespace
        while i < len(s) and s[i].isspace():
            i += 1

        if i == len(s):
            return

        # Numbers (integer or float)
        if s[i].isdigit():
            t = s[i]
            i += 1
            isFloat = False
            isValid = True
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                if s[i] == '.':
                    if isFloat:
                        isValid = False
                    isFloat = True
                t += s[i]
                i += 1

            if not isValid:
                raise ValueError(f"Invalid number token found: {t}")

            if isFloat:
                yield FloatToken(t)
            else:
                yield IntToken(t)

        # Identifiers (variable names) and keywords
        elif s[i].isalpha() or s[i] == '_':
            t = s[i]
            i += 1
            while i < len(s) and (s[i].isalnum() or s[i] == '_'):
                t += s[i]
                i += 1
            if t in ['if', 'else']:
                yield KeywordToken(t)
            else:
                yield IdentifierToken(t)

        elif s[i] == '(':
            i += 1
            yield ParenToken('(')

        elif s[i] == ')':
            i += 1
            yield ParenToken(')')

        elif s[i] == '{':
            i += 1
            yield OperatorToken('{')

        elif s[i] == '}':
            i += 1
            yield OperatorToken('}')

        # NEW: Semicolon for statement separation
        elif s[i] == ';':
            i += 1
            yield OperatorToken(';')

        # Operators (including two-character operators)
        elif s[i] in '+-*/<>=!':
            if s[i:i+2] in ['<=', '>=', '==', '!=', '**']:
                yield OperatorToken(s[i:i+2])
                i += 2
            else:
                yield OperatorToken(s[i])
                i += 1

        else:
            raise ValueError(f"Unexpected character: {s[i]}")
