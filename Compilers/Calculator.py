from Top import e
from Parsers import parse


s = "19 + 5 / 3 + if 15 <= 16 then 1 + 3 else 19 / 6 end"
t = "if 15 <= 16 then 1 + 3 else 19 / 6 end"
u = """
    if 15 >= 16 
    then 
        if 19 < 7 
        then 4 
        else 3 
        end 
    elseif 2 < 3 
    then 5 
    elseif 2 / 0
    then 7
    else 4
    end"""
v = "(2 > 3) + 4"
w = "( 2 * 5 * 3.3 )"
s2 = parse(s)
print(e(s2))
