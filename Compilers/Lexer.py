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



def lex(s: str) -> Iterator[Token]:
    i = 0
    while True:
        while i < len(s) and s[i].isspace():
            i = i + 1

        if i == len(s):
            return

        if s[i].isdigit():
            t = s[i]
            i = i + 1
            flag = False
            while i < len(s) and (s[i].isdigit() or s[i]=='.'):
                if s[i] == '.': flag = not flag
                t = t + s[i]
                i = i + 1
            if flag: yield FloatToken(t)
            else: yield IntToken(t)
        
        elif s[i].isalpha():
            t = s[i]
            i = i + 1
            while i < len(s) and s[i].isalpha():
                t = t + s[i]
                i = i + 1
            match t:
                case 'if' | 'then' | 'end' | 'else' | 'elseif':
                    yield KeywordToken(t)
                case 'add' | 'sub' | 'mul' | 'div' | 'lt' | 'lte' | 'gt' | 'gte' | 'eq' |'neq' |'neg' |'exp':
                    yield OperatorToken(t)
        elif s[i] == '(':
            yield ParenToken('(')
        elif s[i] == ')':
            yield ParenToken(')')


