# -*- coding: utf-8 -*-

import sys

def state(chord):
  if len(chord)!=3:
    raise Exception("Chords must have 3 notes")

def canonical(chord):
  while any(note > 7 for note in chord):
    chord = [note-7 for note in chord]
  return chord

NAMES=['C', 'D', 'E', 'F', 'G', 'A', 'B']
def note_to_letter(note):
  while note < 1:
    note += 7
  note = note % 7
  return NAMES[note-1]

def chord_to_letters(chord): 
  return '-'.join([note_to_letter(note) for note in chord])

def chord_fundamental(chord):
  chord_state = state(chord)
  low, mid, high = canonical(chord)
  if chord_state == 0:
    return low
  if chord_state == 1:
    return high
  if chord_state == 2:
    return mid

STATE_NAME=['fnd', '1st', '2nd']
def chord_to_name(chord):
  chord_state = state(chord)
  fundamental = chord_fundamental(chord)
  return "("+note_to_letter(fundamental)+ ',' +STATE_NAME[chord_state]+')'

GRADE_NAMES=['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
GRADE_NAMES_VISUAL = [('o'*(i+1)) for i in range(7)]
def chord_to_grade(chord, visual=True):
  fundamental = chord_fundamental(chord)
  names = GRADE_NAMES_VISUAL if visual else GRADE_NAMES
  return names[fundamental-1]

# returns 0 for fundamental, 1 for first inversion, 2 for second inversion
def state(chord):
  low, mid, high = chord
  if (mid-low+1) == 4:
    return 2
  if (high-mid+1) == 3:
    return 0
  return 1

# changes 1 note by 1 tone in chord, making sure result is valid
def change_one(chord):
  chord_state = state(chord)
  low, mid, high = chord
  if chord_state == 0:
    return [low, mid, high+1] # fundamental -> 1st inv
  if chord_state == 1:
    return [low, mid+1, high] # 1st inv -> 2nd inv
  if chord_state == 2:
    return [low+1, mid, high] # 2nd inv -> fundamental

# changes N notes by 1 in chord
def change(chord, n):
  if not (-4 < n < 4):
    raise Exception("can't apply change greater than 3")
  
  current = chord
  for _ in range(n):
    current = change_one(current)
  return current

def pretty_print(chord, line=None, header=False, info=True, min_pitch=-6, max_pitch=8, columns=True, extra=''):
  if header:
    if line is not None:
      print('\t', end='')
    for pitch in range(min_pitch, max_pitch+1):
      print(note_to_letter(pitch),end='')
    print('')
  if line is not None:
    print(str(line)+":", end='\t')
  for note in range(min_pitch,max_pitch+1):
    back = '|' if (columns and note_to_letter(note)=='C') else ' '
    print('o' if note in chord else back, end = '')

  print('' if not info else ("|\t"+ chord_to_grade(chord)+"\t"+chord_to_letters(chord)+"\t"+chord_to_name(chord)+" \t"+extra))

c_chord_0 = canonical([1, 3, 5])
print("fundamental C chord", c_chord_0, chord_to_letters(c_chord_0))
c_chord_1 = canonical([3, 5, 8])
print("first inversion of C", c_chord_1, chord_to_letters(c_chord_1))
c_chord_2 = canonical([5, 8, 10])
print("second inversion of C", c_chord_2, chord_to_letters(c_chord_2))
print(state(c_chord_0), state(c_chord_1), state(c_chord_2))

pretty_print(c_chord_0, header=True)
pretty_print(c_chord_1)
pretty_print(c_chord_2)

c_changed_one = change_one(c_chord_0)
print(c_changed_one, state(c_changed_one))

print("="*80)
print("1 change loop")
current = c_chord_0
finished = False
for row in range(30):
  if (finished): break
  if (row != 0):
    current = change_one(current)
    if chord_to_letters(current) == chord_to_letters(c_chord_0):
      finished = True
  pretty_print(current, header=(row%7==0), max_pitch=15)

print("="*80)
print("2+3 change sequence loop")
current = c_chord_0
finished = False
for row in range(500):
  if (finished): break

  current_change = 2 if (row%2==1) else 3
  next_change = 2 if ((row+1)%2==1) else 3
  
  if (row != 0):
    current = change(current, current_change)
    if chord_to_letters(current) == chord_to_letters(c_chord_0) and next_change == 2:
      finished = True
  
  pretty_print(current, line=row, header=(row%1000==0), min_pitch=1, max_pitch=15+7*4, extra=('+'+str(next_change)))

sys.exit(0)

print("="*80)
print("1+2+3 change sequence loop")
current = c_chord_0
finished = False
for row in range(30):
  if (finished): break

  current_change = 1+((row-1)%3)
  next_change = 1+((row)%3)
  
  if (row != 0):
    current = change(current, current_change)
    if chord_to_letters(current) == chord_to_letters(c_chord_0) and next_change == 1:
      finished = True
  
  pretty_print(current, line=row, header=(row%1000==0), min_pitch=1, max_pitch=15+7*4, extra=('+'+str(next_change)))
