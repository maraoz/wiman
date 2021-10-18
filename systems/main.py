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
#raw_input()

# system B
B = []
for design in A:
    for i in range(3):
        for j in range(2):
            B.append(str(i+1)+design[0]+str(j+1)+design[1]+"1"+design[2])
print('B = '+' | '.join(B))
print('|B| = ' + str(len(B)))
print('')

#raw_input()
def density_pattern(d):
    ret = ''
    remaining = {}
    for note in [d[i:i+2] for i in range(0, len(d), 2)]:
        for k in remaining:
            if remaining[k] > 0:
                remaining[k] -= 1
        duration = int(note[0])
        height = note[1]
        # simultaneous note with the same height
        if remaining.get(height) > 0:
            #print('simul '+d)
            return None

        remaining[height] = duration
        ret += str(len([k for k in remaining if remaining[k] > 0]))
    return ret

count = {}
print('B density patterns:')
for design in B:
    density = density_pattern(design)
    print(design + ' -> ' + density)
    count[density] = count.get(density, 0) + 1

for k in count:
    print(k + ' -> '+str(count[k])+' times.')

#raw_input()
# system C

C = []
for note in sigma:
    C += unique(permutations(sigma + note))
print('C = '+' | '.join(C))
print('|C| = ' + str(len(C)))
print('')
#raw_input()

print('C reduction to A')
def reduce(design):
    return unique(design, t=lambda x: "".join(x))
for design in C:
    print(design + ' -> ' + reduce(design))

#raw_input()
# system D

D = []

def check_d(d):
    return density_pattern(d) is not None   

candidates = []
for i in range(4):
    for j in range(3):
        for k in range(2):
            count = 0
            for design in C:
                candidate = str(i+1)+design[0]+str(j+1)+design[1]+str(k+1)+design[2]+"1"+design[3]
                candidates.append(candidate)
                if check_d(candidate):
                    count += 1
                    print(candidate)
            print(i+1, j+1, k+1, 1, "count", count)
s = 0
for candidate in candidates:
    if check_d(candidate):
        s += 1
        D.append(candidate)
#print('d '+design+'    > ' + str(s) + ' out of '+str(len(candidates)))
#raw_input()
print('D = '+' | '.join(D))
print('|D| = ' + str(len(D)))
print('')

#raw_input()
count = {}
print('D density patterns:')
for design in D:
    density = density_pattern(design)
    if density is None:
        print('DENSITY NONE FOR '+design)
        continue
    print(design + ' -> ' + density)
    count[density] = count.get(density, 0) + 1

for k in count:
    print(k + ' -> '+str(count[k])+' times.')

#raw_input()
