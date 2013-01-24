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
RATE = 44100 # bitrate to rcord
FPS = 30
MP3 = "monkey_island_theme.mp3"

t = None
t = scipy.linspace(0, 120, 4000)
clock = pygame.time.Clock()

def simulate():
    acc = lambda t: 10*scipy.sin(2*pi*2.0*t) + 5*scipy.sin(2*pi*8.0*t) + 2*scipy.random.random(len(t))
    # acc = lambda t: 10*scipy.sin(2*pi*2.0*t) + 5*scipy.sin(2*pi*8.0*t)
    return(acc(t))

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
zero_fft = int(surface.get_height() / 3)
zero_signal = int(2 * surface.get_height() / 3)

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

while True:
    for event in pygame.event.get(): #check if we need to exit
        if event.type == pygame.QUIT:
            in_stream.close()
            out_stream.close()
            p.terminate()
            pygame.quit()
            sys.exit()
    surface.fill((0, 0, 0))
    t1 = time.time()
    # pcm signal
    pcm = in_stream.read(BUFFER * 2)
    signal = numpy.fromstring(pcm, dtype=numpy.int16)
    out_stream.write(pcm)
    duration = time.time() - t1
    # fft
    fft = abs(scipy.fft(signal))
    # frequencies
    freqs = scipy.fftpack.fftfreq(signal.size, duration)
    # print freqs
    faktor = 500
    # print fft
    # t = scipy.linspace(0, time.time(), WIDTH)
    points_fft = numpy.column_stack((xrange(len(fft)), zero_fft - fft / faktor))
    # points_freqs = numpy.column_stack((xrange(len(freqs)), middle + freqs / faktor))
    points_signal = numpy.column_stack((xrange(len(freqs)), zero_signal + signal / 100))
    #for x in range(surface.get_width()):
    #    points.append((x, fft[x]))
    # print points
    pygame.draw.aalines(surface, (255, 0, 0), False, points_fft, 1)
    pygame.draw.aalines(surface, (0, 255, 0), False, points_signal, 1)
    pygame.display.update()
    clock.tick(FPS)
