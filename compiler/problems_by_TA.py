from top import e
from parser import parse, ParseError

def problem_by_TA():
    # Problem statement: Write the multiplication table of 17 till 15 terms
    code = """
            def f(){
                return 1;
            };

            def foo(){
                print(f());
            };

            def bar(){
                def f(){
                    return 10;
                };

                foo();
            };

            bar();
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
