from mido import MidiFile
import sys
import time
import struct
import math
import math


import numpy
from PIL import Image


mid = MidiFile('bach-invention-01.mid')

NAMES=['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_name(note):
    chroma = note % 12
    return NAMES[chroma] + str(note//12-1)

def frequency(note):
    return 2**((note-69)/12)*440

def simplify(note):
    chroma = note % 12
    if chroma == 1: chroma = 0 # C#->C
    if chroma == 3: chroma = 2 # D# ->D
    if chroma == 6: chroma = 5 # F# -> F
    if chroma == 8: chroma = 7 # G# -> G
    if chroma == 10: chroma = 11 # Bb -> B
    return (note//12)*12 + chroma

def chromatic_to_tonal(note):
    chroma = note % 12
    octave = note // 12
    tone = None
    if chroma <= 1: tone = 0 # C, C#
    elif chroma <= 3: tone = 1 # D, D#
    elif chroma == 4: tone = 2 # E
    elif chroma <= 6: tone = 3 # F, F#
    elif chroma <= 8: tone = 4 # G, G#
    elif chroma == 9: tone = 5 # A
    elif chroma <= 11: tone = 6 # Bb, B
    return octave*7+tone

n = 0
#colors = [[255, 50, 50], [50, 50, 255], [255,255,255]]
colors = [[255, 150, 150], [150, 150, 255], [255,255,255]]
alt_colors = [[255, 150, 220], [150, 255, 220], [255, 255, 255]]
QUANTA = 48 #smallest note duration
OFF_VALUE = 250
OFF_COLOR = [OFF_VALUE, OFF_VALUE, OFF_VALUE]
scale = 16
NOTES = 7*8+5 # 127 for chromatic
HEIGHT = NOTES*scale
BORDER = 1
BORDER_COLOR = [255,255,255]
length = int(mid.length*1000//(QUANTA)/2)
print(length, "total duration)")
padding = 32
WIDTH = (length+padding)*scale
data = numpy.zeros((HEIGHT, WIDTH, 3), dtype=numpy.uint8) + OFF_VALUE

GRID_COLOR = [220,220,220]
STRONG_COLOR = [180,180, 180]
for x in range(length+padding):
    data[0:HEIGHT, x*scale] = GRID_COLOR if x%32!=0 else STRONG_COLOR
for y in range(NOTES):
    data[y*scale, 0:WIDTH] = GRID_COLOR if (y-6)%7!=0 else STRONG_COLOR

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    x = 0
    color = colors[i-1]
    border_color = [int(color[0]*2/4 + 2*BORDER_COLOR[0]/4), int(color[1]*2/4 + 2*BORDER_COLOR[1]/4), int(color[2]*2/4 + 2*BORDER_COLOR[2]/4)]
    alt_color = color
    for msg in track:
        #time.sleep(msg.time/1000.0)
        if not msg.is_meta:
            n += 1
            if (msg.type=='note_off'):
                pass
                print(track.name, msg.type, note_name(msg.note), note_name(simplify(msg.note)), msg.time/QUANTA)
            if msg.time % QUANTA != 0:
                print("weird note time")
                sys.exit(1)
            duration = msg.time//QUANTA
            if msg.type == 'note_off':
                converted_note = chromatic_to_tonal(msg.note)
                paint = border_color
                if (simplify(msg.note) != msg.note):
                    # alteration
                    paint = alt_color
                y = (NOTES-converted_note)
                data[y*scale:(y+1)*scale, x*scale:(x+duration)*scale] = paint
                if BORDER:
                    data[y*scale:y*scale+BORDER, x*scale:(x+duration)*scale] = color
                    data[(y+1)*scale-BORDER:(y+1)*scale, x*scale:(x+duration)*scale] = color
                    for t in range(duration+1):
                        data[y*scale:(y+1)*scale, (x+t)*scale:(x+t)*scale+BORDER] = color
                        #data[y*scale:(y+1)*scale, (x+t+1)*scale-BORDER:(x+t+1)*scale] = color
                    pass
            x += duration
            #image = Image.fromarray(data)
            #image.save("image-"+str(n)+".png")
image = Image.fromarray(data)
image.save("image-"+str(n)+".png")


midi_file = './bach-invention-01.mid'
def play_music(music_file):
    import pygame
    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.set_volume(0.8)
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)
    pygame.mixer.music.unload()

try:
    pass
    play_music(midi_file)
except KeyboardInterrupt:
    # if user hits Ctrl/C then exit
    # (works only in console mode)
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    raise SystemExit
