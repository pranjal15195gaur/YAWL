from top import e
from parser import parse, ParseError

# Successful test cases
tests_ok = [
    "5 + 3",
    "if 1 == 1 { 10 } else { 20 }",
    "(10 - 3) * 2",
    "if 2 < 3 { 2 + 2 } else { 9 / 3 }",
    "if 2 < 3 { if 1 == 1 { 100 } else { 0 } } else { 42 }",
    "5 + if 2 < 3 { 4 } else { 20 }",
    # New tests for variables:
    "x = 10",
    "(x = 5 + 3) + x",  # Should assign x to 8 then add x: result 16.
]

# Failing test cases
tests_error = [
    "if 1 == 1 { 5 ",             # missing closing brace
    "if 2 < 3 { 4 } else if { 5 }",  # missing condition
    "y + 2",                     # 'y' is undefined
]

def run_tests():
    print("=== Successful Tests ===")
    for code in tests_ok:
        try:
            ast = parse(code)
            result = e(ast)  # each evaluation gets a fresh environment
            print(f"Code: {code}")
            print(f"AST:  {ast}")
            print(f"Result: {result}\n")
        except Exception as ex:
            print(f"Failed to parse or evaluate '{code}':", ex)

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
