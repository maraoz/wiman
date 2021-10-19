# -*- coding: utf-8 -*-

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
    current = change(current)
  return current

def pretty_print(chord, header=False, name=True, min_pitch=-6, max_pitch=8, columns=True):
  if header:
    for pitch in range(min_pitch, max_pitch+1):
      print(note_to_letter(pitch),end='')
    print('')
  for note in range(min_pitch,max_pitch+1):
    back = '|' if (columns and note_to_letter(note)=='C') else ' '
    print('o' if note in chord else back, end = '')

  print('' if not name else (" "+chord_to_letters(chord)))

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

print("change=1 loop")
current = c_chord_0
finished = False
for row in range(30):
  if (finished): break
  if (row != 0):
    current = change_one(current)
    if chord_to_letters(current) == chord_to_letters(c_chord_0):
      finished = True
  pretty_print(current, header=(row%10==0), max_pitch=15)