#!/usr/bin/python
import math
import sys

width = 160
height = 40
left=-2.1
right=1.2
bottom=-1.2
top=1.2
maxiter=20

step_x = (right - left) / width
step_y = (top - bottom) / height

for y in range(height):
    for x in range(width):
        # starting point
        # start = start_r + start_i
        # start ^ 2 = (start_r + start_i) * (start_r + start_i)
        # start_next = start_r * start_r + 2 * start_i * start_r  - start_i*start_i
        # left + (step_x * x) + bottom + (step_y * y)
        start_r = left + (step_x * x)
        start_i = bottom + (step_y * y)
        #print(f"starting at {start_r} +  {start_i}i")
        value = math.sqrt(start_r * start_r + start_i * start_i)
        for i in range(maxiter):
            start_r =  start_r * start_r + start_i * start_i
            start_i = 2 * start_r * start_i
            value = math.sqrt(start_r * start_r + start_i * start_i)
            if value > 1.2:
                break
        sys.stdout.write(str(i)[-1])
        #print(f"\t{i} : {start_r} +  {start_i}i = {abs}")
    sys.stdout.write("\n")

