# test.py
from top import e
from parser import parse, ParseError

# Successful test cases
tests_ok = [
    "x = 10; y = 20;z =5; x + y*z;",              # Should evaluate to 30
    "a = 5; b = (a = a + 3) + a; a + b;",    # a becomes 8, then b becomes (8 + 8) = 16, so result = 8 + 16 = 24
    "5 + 3*7;",                              # Single expression: 8
    "if 1 == 1 { 10 } else { 20 };",        # Conditional: 10
]

# Failing test cases
tests_error = [
    "if 1 == 1 { 5",                      # missing closing brace
    "if 2 < 3 { 4 } else if { 5 }",         # missing condition after 'else if'
    "y + 2;",                              # undefined variable 'y'
    "x =3 y=4"
]

def run_tests():
    print("=== Successful Tests ===")
    for code in tests_ok:
        try:
            ast = parse(code)
            result = e(ast)
            print(f"Code: {code}")
            print(f"AST:  {ast}")
            print(f"Result: {result}\n")
        except Exception as ex:
            print(f"Failed to parse or evaluate '{code}': {ex}\n")

    print("=== Failing Tests ===")
    for code in tests_error:
        try:
            ast = parse(code)
            result = e(ast)
            print(f"Code: {code}")
            print(f"AST:  {ast}")
            print(f"Result: {result} (Unexpected success)\n")
        except ParseError as perr:
            print(f"ParseError for '{code}': {perr}\n")
        except Exception as ex:
            print(f"Error for '{code}': {ex}\n")

if __name__ == "__main__":
    run_tests()
