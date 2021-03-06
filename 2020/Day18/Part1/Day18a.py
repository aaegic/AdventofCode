#!/usr/bin/python3

import itertools

fh = open("input.txt")
eq = fh.read()
fh.close()

def rindex(li:list, ch:str, lrange:int, rrange:int) -> int:
    for i in range(rrange, lrange - 1, -1):
        if li[i] == ch:
            return i

def compute(input:list) -> int:
    lft, opr = None, None
    
    for e in input:
        if opr is not None:
            if opr == '+':
                lft = lft + e
            elif opr == '*':
                lft = lft * e
            
            opr = None
        elif lft is not None:
            opr = e
        else:
            lft = e
            
    return lft

eqlst = list()
reslt = list()

for line in eq.split("\n"):
    eq = list()
    for char in line.replace(' ', ''):
        if char == ' ':
            continue
        if char.isdigit():
            eq.append(int(char))
        else:
            eq.append(char)
    
    eqlst.append(eq)

for eq in eqlst:
    while '(' in eq:
        rpi = eq.index(')')
        lpi = rindex(eq, '(', 0, rpi)

        eq = list(itertools.chain(eq[:lpi], [compute(eq[lpi+1:rpi])], \
            eq[rpi+1:]))
    
    reslt.append(compute(eq))

print(reslt)
print(sum(reslt))