#!/usr/bin/python
# import cmath
import math
import sys
import time

def blit():
    factor = math.pi / 180
    for y in range(height):
        for x in range(width):
            # to look for color codes in ascii
            # https://en.wikipedia.org/wiki/ANSI_escape_code
            # value = color[y*width+x]
            value = color[y * width +x]
            red = int(128 + 127 * math.sin(value * factor))
            green = int(128 + 127 * math.sin(value * 2 * factor))
            blue = int(128 + 127 * math.sin(value * 4 * factor))
            sys.stdout.write(f"\033[48;2;{red};{green};{blue}m \033[m")
        if y != height:
            sys.stdout.write("\n")


def main(middle, magnify, maxiter):
    step_x = 0.04375
    step_y = 0.08333333333333333
    print(step_x, step_y)
    while True:
        left = middle.real - width * step_x / 2
        right = middle.real + width * step_x / 2
        bottom = middle.imag - height * step_y / 2
        top = middle.real + height * step_y / 2
        imag = bottom
        for y in range(height):
            real = left
            for x in range(width):
                constant = complex(real, imag)
                start = constant
                for i in range(maxiter):
                    if abs(start) > 2:
                        break
                    start = start * start + constant
                if i == maxiter:
                    color[y * width + x] = 0
                else:
                    color[y * width + x] = i
                real += step_x
            imag += step_y
        blit()
        time.sleep(0.1)
        step_x *= magnify
        step_y *= magnify
        maxiter = int(maxiter * 1.01)

if __name__ == "__main__":
    width = 150
    height = 45
    magnify = 0.9
    maxiter = 256
    # 0.04375 0.08333333333333333
    # to what point to zoom in
    middle = complex(-0.75, 0)
    middle = complex(-0.235125, 0.827215)
    middle = complex(0.001643721971153, -0.822467633298876)
    middle = complex(-0.7453, 0.1127)
    middle = complex(-0.8115312340458353, 0.2014296112433656)
    print(middle)
    color = [0] * width * height # array of itertions
    main(middle, magnify, maxiter)
