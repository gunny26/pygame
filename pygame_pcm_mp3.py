#!/usr/bin/python
import scipy
import mad
import scipy.fftpack
from scipy import pi
import pyaudio
import numpy
import time
import pygame
import random
import sys
import mad

WIDTH = 640
HEIGHT = 400
BUFFER = 640 # length of sample
X_ARRAY = xrange(BUFFER)
RATE = 44100 # bitrate to rcord
FPS = 120
MP3 = "monkey_island_theme.mp3"

clock = pygame.time.Clock()
pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
zero_signal = int(surface.get_height() / 2)

# initialize pyaudio and open device
p = pyaudio.PyAudio()
# open mp3 input file, reading pcm data
in_stream = mad.MadFile(MP3)
# open output stream to playback something
out_stream = p.open(format =
    p.get_format_from_width(pyaudio.paInt32),
    channels = 2,
    rate = RATE,
    output = True)

np = [None, None, None, None, None]
colors = (
    (0, 255, 0),
    (0, 205, 50),
    (0, 155, 100),
    (0, 105, 150),
    (0, 55, 200),
    )

    
while True:
    for event in pygame.event.get(): #check if we need to exit
        if event.type == pygame.QUIT:
            out_stream.close()
            p.terminate()
            pygame.quit()
            sys.exit()
    surface.fill((0, 0, 0))
    t1 = time.time()
    # pcm signal
    pcm = in_stream.read(BUFFER)
    signal = numpy.fromstring(pcm, dtype=numpy.int16)[0:BUFFER]
    out_stream.write(pcm)
    points_signal = numpy.column_stack((X_ARRAY, zero_signal + signal / 200))
    np.append(points_signal)
    np.pop(0)
    counter = 0
    for points in np:
        if points is None:
            continue
        pygame.draw.lines(surface, colors[counter], False, points, 1)
        counter += 1
    pygame.display.update()
    clock.tick(FPS)
