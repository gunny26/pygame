from math import sqrt
import time
# non std modules
import pygame
import pyaudio
import numpy as np


class Spectrum:
    """ audio spectrograph effect for background """

    def __init__(self, dim, rate=44100):
        self.surface = pygame.Surface(dim)
        self.height = dim[1]
        self.chunk = dim[0]  # width of spectogram
        self.format = pyaudio.paInt16
        audio = pyaudio.PyAudio()
        self.stream = audio.open(format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            frames_per_buffer=self.chunk)

    def update(self):
        """ update every frame """
        buff = self.stream.read(self.chunk)  # read chunk paInt16
        data = np.frombuffer(buff, dtype=np.int16)  # to numpy array
        fft_complex = np.fft.fft(data, n=self.chunk)  # fft analysis
        # find total maximum to calculate scale
        lengths = [value.real * value.real + value.imag * value.imag for value in fft_complex[:len(fft_complex) // 2]]  # all vector lengths
        max_val = sqrt(max(lengths))
        if max_val != 0.0:
            self.surface.fill((0, 0, 0))  # blank out
            scale_value = self.height / max_val
            for index, length in enumerate(lengths):  # skip the upper half
                dist = int(scale_value * sqrt(length))
                pygame.draw.line(self.surface, (100, 100, 100), (index, self.height), (index, self.height - dist))
        return self.surface


class SpectrumCircle:
    """ audio spectrograph effect for background """

    def __init__(self, dim, rate=44100):
        self.surface = pygame.Surface(dim)
        self.center = (dim[0] // 2, dim[1] // 2)
        self.radius = dim[1] // 2
        self.radius = 100
        self.chunk = 360  # 360 degrees
        self.format = pyaudio.paInt16
        audio = pyaudio.PyAudio()
        self.stream = audio.open(format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            frames_per_buffer=self.chunk)

    def update(self):
        """ update every frame """
        buff = self.stream.read(self.chunk)  # read chunk paInt16
        data = np.frombuffer(buff, dtype=np.int16)  # to numpy array
        fft_complex = np.fft.fft(data, n=self.chunk)  # fft analysis
        # find total maximum to calculate scale
        lengths = [value.real * value.real + value.imag * value.imag for value in fft_complex[:len(fft_complex) // 2]]  # all vector lengths
        max_val = sqrt(max(lengths))
        if max_val != 0.0:
            self.surface.fill((0, 0, 0))  # blank out
            for index, value in enumerate(fft_complex[:len(fft_complex) // 2]):  # skip the upper half
                x = self.center[0] + int(self.radius * value.real / max_val)
                y = self.center[1] + int(self.radius * value.imag / max_val)
                pygame.draw.line(self.surface, (100, 100, 100), self.center, (x, y))
        return self.surface


def old():
    pygame.init()

    SCREEN_HEIGHT = 50
    RATE = 44100
    CHUNK = RATE // 128
    FORMAT = pyaudio.paInt16

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)
    screen = pygame.display.set_mode((CHUNK // 2, SCREEN_HEIGHT))
    color = (0, 128, 1)  # color to draw the lines
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        buff = stream.read(CHUNK)  # read chunk paInt16
        data = np.frombuffer(buff, dtype=np.int16)  # to numpy array
        fft_complex = np.fft.fft(data, n=CHUNK)  # fft analysis
        # find total maximum to calculate scale
        lengths = [value.real * value.real + value.imag * value.imag for value in fft_complex[:len(fft_complex) // 2]]  # all vector lengths
        max_val = sqrt(max(lengths))
        if max_val != 0.0:
            screen.fill((0, 0, 0))  # blank out
            scale_value = SCREEN_HEIGHT / max_val
            for index, length in enumerate(lengths):  # skip the upper half
                #v = complex(v.real / dist1, v.imag / dist1)
                dist = scale_value * sqrt(length)
                pygame.draw.line(screen, color, (index, SCREEN_HEIGHT), (index, SCREEN_HEIGHT - dist))
            pygame.display.flip()

def main():
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        background = SpectrumCircle((200, 200), 44100)
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                surface.blit(background.update(), (0, 0))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
