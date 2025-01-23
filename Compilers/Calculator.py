import sys
sys.path.insert(1, '"D:/Sem-2/Compilers"')
from Top import e
from Parsers import parse


s = "19 add 5 div 3 add if 15 lte 16 then 1 add 3 else 19 div 6 end"
t = "if 15 lte 16 then 1 add 3 else 19 div 6 end"
u = """
    if 15 gte 16 
    then 
        if 19 lt 7 
        then 4 
        else 3 
        end 
    elseif 2 lt 3 
    then 5 
    elseif 2 div 0
    then 7
    else 4
    end"""
v = "(2 gt 3) add 4"
w = "( 2 mul 5 mul 3.3 )"
s2 = parse(s)
print(e(s2))
