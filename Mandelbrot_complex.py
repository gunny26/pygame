#!/usr/bin/python
import cmath
import math
import sys
import time

width = 80
height = 24
left=-2.5
right=1.0
bottom=-1.0
top=1.0
maxiter=255
# 0.04375 0.08333333333333333
step_x = (right - left) / width
step_y = (top - bottom) / height
print(step_x, step_y)
# to what point to zoom in
middle = complex((left + right) / 2, (bottom + top) / 2)
middle = complex(-0.75, 0)
# middle = complex(0.001643721971153, -0.822467633298876)
print(middle)
while True:
    left = middle.real - width * step_x / 2
    right = middle.real + width * step_x / 2
    bottom = middle.imag - height * step_y / 2
    top = middle.real + height * step_y / 2
    magnify = 0.9

    imag = bottom
    for y in range(height):
        real = left
        for x in range(width):
            constant = complex(real, imag)
            start = constant
            for i in range(maxiter):
                if abs(start) > 4:
                    break
                start = start * start + constant
            # to look for color codes in ascii
            # https://en.wikipedia.org/wiki/ANSI_escape_code
            sys.stdout.write(f"\033[48;5;{i}m+\033[m")
            real += step_x
        imag += step_y
        #if y == height - 1:
        #    test = input()
        sys.stdout.write("\n")
    time.sleep(0.1)
    step_x *= magnify
    step_y *= magnify
