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

def density_pattern(d):
    l1 = int(d[0])
    l2 = int(d[2])
    d1 = 1
    d2 = 1 if l1 == 1 else 2
    d3 = 1 + (1 if l1 == 3 else 0) + (1 if l2 == 2 else 0)
    return str(d1)+str(d2)+str(d3)

count = {}
print('Density patterns:')
for design in B:
    density = density_pattern(design)
    print(design + ' -> ' + density)
    count[density] = count.get(density, 0) + 1

for k in count:
    print(k + ' -> '+str(count[k])+' times.')

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
    print(design + ' -> ' + reduce(design))

# system D
