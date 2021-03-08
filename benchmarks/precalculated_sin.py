#!/usr/bin/python3
"""
Hypothesis: pre calculated sin is faster than math.sin
"""
import array
import time
import math

ITERATIONS = 100000000
SIN = []
SIN_F = None
SIN_T = None

# pre calculate SIN form 360 degrees
for degree in range(0, 360, 1):
    SIN.append(math.sin(math.radians(degree)))
# print(SIN)
SIN_F = array.array("f", SIN)
SIN_T = tuple(SIN)

print(f"testing {ITERATIONS} sin calculations with each method and comparing speed")

# calculated sin, input in degrees
starttime = time.time()
for i in range(ITERATIONS):
    value = math.sin(math.radians(i))
print(f"sin calculation with math module took {time.time() - starttime} seconds - radians conversion")

# calculated sin, input in degrees
starttime = time.time()
for i in range(ITERATIONS):
    value = math.sin(i)
print(f"sin calculation with math module took {time.time() - starttime} seconds - no radians conversion")

# calculated sin, input in degrees
starttime = time.time()
for i in range(ITERATIONS):
    value = SIN[i % 360]
print(f"sin calculation with precalculated sins in list took {time.time() - starttime} seconds")

# calculated sin, input in degrees
starttime = time.time()
for i in range(ITERATIONS):
    value = SIN_F[i % 360]
print(f"sin calculation with precalculated sins in array took {time.time() - starttime} seconds")

# calculated sin, input in degrees
starttime = time.time()
for i in range(ITERATIONS):
    value = SIN_F[i % 360]
print(f"sin calculation with precalculated sins in tuple took {time.time() - starttime} seconds")

# calculated sin, input in degrees
starttime = time.time()
for i in range(ITERATIONS):
    value = SIN[(i + 90) % 360]
print(f"cos calculation with precalculated sins in list took {time.time() - starttime} seconds")


