# -*- coding: utf-8 -*-
from collections import OrderedDict


def unique(x, t=list):
    return t(OrderedDict.fromkeys(x))


def permutations(x):
    if len(x) <= 1:
        return x
    head = x[0]
    rest = x[1:]
    recursive = permutations(rest)
    ret = []
    for i in range(len(rest)+1):
        for sub in recursive:
            ret.append(sub[:i] + head + sub[i:])
    return ret


sigma = u'_-‾'

# system A
A = permutations(sigma)
print('A = '+' | '.join(A))
print('|A| = ' + str(len(A)))
print('')

# system B
B = []
for design in A:
    for i in range(3):
        for j in range(2):
            B.append(str(i+1)+design[0]+str(j+1)+design[1]+"1"+design[2])
print('B = '+' | '.join(B))
print('|B| = ' + str(len(B)))
print('')

# system C

C = []
for note in sigma:
    C += unique(permutations(sigma + note))
print('C = '+' | '.join(C))
print('|C| = ' + str(len(C)))
print('')

def reduce(design):
    return unique(design, t=lambda x: "".join(x))
for design in C:
    print(design +' -> '+ reduce(design))

# system D