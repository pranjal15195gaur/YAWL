from top import e
from parser import parse, ParseError

def problem_by_TA():
    # Problem statement : Write the multiplication table of 17 till 15 terms
    code = """
            var a = [10, [20,10,50] , 30, 40];
            print(a[1]);  
            print(a[2][3]);  
           """

    ast = parse(code)
    e(ast)


if __name__ == "__main__":
    problem_by_TA()