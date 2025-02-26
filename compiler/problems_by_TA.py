from top import e
from parser import parse, ParseError

def problem_by_TA():
    # Problem statement: Write the multiplication table of 17 till 15 terms
    code = """
            def table(x) {
                var i = 1;
                while(i <= 15) {
                    print(x * i);
                    i = i + 1;
                }
            }
            table(121);
           """
    try:
        ast = parse(code)
        e(ast)
    except ParseError as pe:
        print("Parse Error:", pe)
    except Exception as ex:
        print("Error:", ex)

if __name__ == "__main__":
    problem_by_TA()
