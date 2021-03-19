#!/usr/bin/python3
# import pyximport; pyximport.install(pyimport=True)
import array
import math


cdef extern from "complex.h":
    double cos(double x) nogil
    double sin(double x) nogil
    float complex I


def mapto(float value, float min1, float max1, float min2, float max2):
    """ map some value to a different scale """
    cdef float len1, len2
    try:
        assert min1 < max1
        len1 = max1 - min1
        len2 = max2 - min2
        return min2 + value * len2 / len1
    except AssertionError as exc:
        print(f"value {value} not in range [{min1}, {max1}]")
        raise exc


def primes(int nb_primes):
    """ return array of primes, starting at """
    cdef int n, i, len_p
    cdef int p[1000]
    if nb_primes > 1000:
        nb_primes = 1000

    len_p = 0  # The current number of elements in p.
    n = 2
    while len_p < nb_primes:
        # Is n prime?
        for i in p[:len_p]:
            if n % i == 0:
                break

        # If no break occurred in the loop, we have a prime.
        else:
            p[len_p] = n
            len_p += 1
        n += 1

    # Let's return the result in a python list:
    result_as_list  = [prime for prime in p[:len_p]]
    return result_as_list


def fib(long maxvalue):
    """
    Fibonacci sequence generator
    """
    cdef long a, b
    a = 0  # startin values
    b = 1
    while b < maxvalue:
        yield b
        a, b = b, a + b  # next set


def mandelbrot_complex(double complex middle, double step, long width, long height, long maxiter):
    """
    generator to calculate mandelbrot set

    :param start: complex number to start with
    :param step: step in real and imaginar as float
    :param width: width to calculate
    :param height: height to calculate
    :param maxiter: maximum iterations
    """
    cdef long i1, i2, y, x, index, n
    cdef double left, bottom, imag, real
    cdef double complex constant, value
    left = middle.real - width * step / 2
    bottom = middle.imag - height * step / 2
    # starting value
    for y, imag in [(i1, bottom + i1 * step) for i1 in range(height)]:
        for x, real in [(i2, left + i2 * step) for i2 in range(width)]:
            index =  y * width + x
            constant = complex(real, imag)
            value = constant
            n = 0
            while n < maxiter:
                if abs(value) > 2.0:
                    break
                value = value ** 2 + constant
                n += 1
            if n == maxiter:
                yield 0
            else:
                yield n


def mandelbrot_save(middle, step, width, height, maxiter):
    """
    calculate mandelbrot set

    :param start: compex number to start with
    :param step: step in real and imaginar as float
    :param width: width to calculate
    :param height: height to calculate
    :param maxiter: maximum iterations
    """
    data = [0] * width * height
    left = middle.real - width * step / 2
    bottom = middle.imag - height * step / 2
    # starting value
    for y, imag in [(i, bottom + i * step) for i in range(height)]:
        for x, real in [(i, left + i * step) for i in range(width)]:
            index =  y * width + x
            constant = complex(real, imag)
            value = constant
            n = 0
            while n < maxiter:
                if abs(value) > 2.0:
                    break
                value = value ** 2 + constant
                n += 1
            if n == maxiter:
                data[index] = 0
            else:
                data[index] = n
    return data


def mandelbrot_noncomplex(double complex middle, double step, int width, int height, int maxiter):
    """
    non complex number algorithm, mostly the basic form of the algorithm

    :param start: complex number to start with
    :param step: step in real and imaginar as floating point number
    :param width: width to calculate
    :param height: height to calculate
    :param maxiter: maximum iterations
    """
    cdef double zx, zy, cx, tempx, cy
    cdef int x, y, count
    cdef double left, bottom
    left = middle.real - width * step / 2
    bottom = middle.imag - height * step / 2
    for y in range(height):
        cy = y * step + bottom
        for x in range(width):
            cx = x * step + left
            zx = 0
            zy = 0
            count = 0
            while (zx * zx + zy * zy < 4) and (count < maxiter):
                tempx = zx * zx - zy * zy + cx
                zy = 2 * zx * zy + cy
                zx = tempx
                count += 1
            yield count

def mandelbrot_path(double complex middle, int maxiter):
    """
    calculating the iterations of one specific point in complex plane

    :param middle: complex number to calculate
    :param maxiter: maximum iterations
    :return <list>: list with interated complex numbers (x + y)
    """
    cdef double zx, zy, cx, tempx, cy
    cdef int count
    cx = middle.real  # step in real
    cy = middle.imag  # step in imaginary
    zx = 0  # starting value in real
    zy = 0  # starting value in complex
    count = 0  # iteration counter
    while (zx * zx + zy * zy < 4) and (count < maxiter):
        tempx = zx * zx - zy * zy + cx
        zy = 2 * zx * zy + cy
        zx = tempx
        yield (zx, zy)
        count += 1
