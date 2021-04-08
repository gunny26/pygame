#!/usr/bin/python3
import time
import math
# non std modules
import pygame
import pyaudio
import numpy as np
# own modules
from RgbColorGradient import get_rgb_color_gradient


FPS = 50
DIM = (320, 200)


class SpectrumBar:
    """ audio spectrograph effect for background """

    def __init__(self, dim: tuple, rate: int = 44100):
        """
        bar spectrograph

        :param dim: dimension in (x, y)
        :param rate: sampling rate
        """
        self.surface = pygame.Surface(dim)
        self.height = dim[1]
        self.chunk = dim[0]  # width of spectogram
        self.format = pyaudio.paInt16
        audio = pyaudio.PyAudio()
        self.stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        self.colors = get_rgb_color_gradient((255, 0, 0), (0, 0, 255), 256)

    def update(self):
        """ update every frame """
        buff = self.stream.read(self.chunk)  # read chunk paInt16
        data = np.frombuffer(buff, dtype=np.int16)  # to numpy array
        fft_complex = np.fft.fft(data, n=self.chunk)  # fft analysis
        # find total maximum to calculate scale
        lengths = [value.real * value.real + value.imag * value.imag for value in fft_complex[:len(fft_complex) // 2]]  # all vector lengths
        max_val = math.sqrt(max(lengths))
        if max_val != 0.0:
            self.surface.fill((0, 0, 0))  # blank out
            scale_value = self.height / max_val
            for index, length in enumerate(lengths[1:]):  # skip the upper half and the first one
                dist = int(scale_value * math.sqrt(length))
                pygame.draw.line(self.surface, self.colors[index], (index, self.height), (index, self.height - dist))
        return self.surface


class SpectrumCircle:
    """ audio spectrograph effect for background """

    def __init__(self, dim: tuple, rate: int = 44100):
        """
        polar spectrograph

        :param dim: dimension in (x, y)
        :param rate: sampling rate
        """
        self.surface = pygame.Surface(dim)
        self.center = (dim[0] // 2, dim[1] // 2)
        self.radius = dim[1] // 2
        self.radius = 100
        self.chunk = 360  # 360 degrees
        self.format = pyaudio.paInt16
        audio = pyaudio.PyAudio()
        self.stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        self.colors = get_rgb_color_gradient((255, 0, 0), (0, 0, 255), 256)

    def update(self) -> pygame.Surface:
        """ update every frame """
        buff = self.stream.read(self.chunk)  # read chunk paInt16
        data = np.frombuffer(buff, dtype=np.int16)  # to numpy array
        fft_complex = np.fft.fft(data, n=self.chunk)  # fft analysis
        max_val = 2 * 2 ** 16  # maximum value of datatype
        if max_val != 0.0:
            self.surface.fill((0, 0, 0))  # blank out
            for index, value in enumerate(fft_complex[1:len(fft_complex) // 2:4]):  # skip the upper half and the first one
                x = self.center[0] + int(self.radius * value.real / max_val)
                y = self.center[1] + int(self.radius * value.imag / max_val)
                pygame.draw.line(self.surface, self.colors[index], self.center, (x, y))
        return self.surface


def main():
    try:
        pygame.init()
        surface = pygame.display.set_mode(DIM)
        background = SpectrumCircle(DIM, 44100)
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                    return
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                surface.blit(background.update(), (0, 0))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
