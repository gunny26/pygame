#!/usr/bin/python
"""Test some Performance Issues"""

import math
import os
try:
    import numpy
    numpy = numpy
except ImportError:
    import numpypy
    numpy = numpypy


def precalc_sin():
    sins = []
    for degree in range(361):
        sins.append(math.sin(degree*math.pi/180))
    return(sins)

def precalc_sin_numpy():
    sins = numpy.zeros(361, float)
    for degree in range(361):
        sins[degree] = math.sin(degree*math.pi/180)
    return(sins)


def sins_list(sins):
    for i in range(10000000):
        x = sins[i % 360]
        # print x

def sins_list_numpy(sins):
    for i in range(10000000):
        x = sins[i % 360]
        # print x

def sins_math():
    for i in range(10000000):
        x = math.sin(i * math.pi / 180)
        # print x

def sins_math2():
    for i in range(10000000):
        x = math.sin(i)
        # print x

def main():
    sins = precalc_sin()
    # check if sin is correct
    assert sins[0] == 0.0
    assert sins[90] == 1.0
    assert abs(sins[180]) <= 0.01
    assert sins[270] == -1.0
    assert abs(sins[360]) <= 0.01
    sins_list(sins)
    sins_math()
    sins_math2()
    # check if sin is correct
    assert sins[0] == 0.0
    assert sins[90] == 1.0
    assert abs(sins[180]) <= 0.01
    assert sins[270] == -1.0
    assert abs(sins[360]) <= 0.01
    sins = precalc_sin_numpy()
    sins_list_numpy(sins)

if __name__ == "__main__":
   # CSI Python
    import pstats
    import cProfile
    profile = "Performance.profile"
    cProfile.runctx( "main()", globals(), locals(), filename=profile)
    s = pstats.Stats(profile)
    s.sort_stats('time')
    s.print_stats(1.0)
    os.unlink(profile)
