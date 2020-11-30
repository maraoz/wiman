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
    ret = ''
    remaining = []
    for note in [d[i:i+2] for i in range(0, len(d), 2)]:
        for i in range(len(remaining)):
            if remaining[i] > 0:
                remaining[i] -= 1
        di = note[0]
        remaining.append(int(di))
        ret += str(len([x for x in remaining if x > 0]))
    return ret

count = {}
print('B density patterns:')
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

D = []

for design in C:
    for i in range(4):
        for j in range(3):
            for k in range(2):
                D.append(str(i+1)+design[0]+str(j+1)+design[1]+str(k+1)+design[2]+"1"+design[3])
print('D = '+' | '.join(D))
print('|D| = ' + str(len(D)))
print('')

count = {}
print('D density patterns:')
for design in D:
    density = density_pattern(design)
    if density is None:
        continue
    print(design + ' -> ' + density)
    count[density] = count.get(density, 0) + 1

for k in count:
    print(k + ' -> '+str(count[k])+' times.')

