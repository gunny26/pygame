#!/usr/bin/python

import pygame
import sys
import math
import logging
logging.basicConfig(level=logging.INFO)
from Vec2d import Vec2d
from Vec3d import Vec3d
import operator


class Vector3d(object):

    def __init__(self, x_or_tuple, y=None, z=None, h=None):
        if y is None:
            self.x = x_or_tuple[0]
            self.y = x_or_tuple[1]
            self.z = x_or_tuple[2]
            self.h = x_or_tuple[3]
        else:
            self.x = x
            selx.y = y
            self.z = z
            self.h = h
        self.data = [x, y, z, h]

    def __getitem__(self, key):
        if 0 <= key <= 3:
            return(self.data[key])

    def __setitem__(self, key, value):
        if 0 <= key <= 3:
            self.data[key] = value


class Matrix3(object):

    def __init__(self, *args):
        logging.debug("__init__(%s)", str(args))
        if args is not None and len(args) > 0:
            if len(args) == 4:
                self.matrix = [
                    args[0], 0, 0, 0,
                    0, args[1], 0, 0,
                    0, 0, args[2], 0,
                    0, 0, 0, args[3]
                    ]
            elif len(args) == 3:
                self.matrix = [
                    args[0], 0, 0, 0,
                    0, args[1], 0, 0,
                    0, 0, args[2], 0,
                    0, 0, 0, 1
                    ]
            elif isinstance(args[0], list) and len(args[0]) == 16:
                self.matrix = args[0]
        else:
            self.matrix = [0] * 16

    def get(self, row, col):
        return(self.matrix[(row + 1) * (col + 1) - 1])

    def get_row(self, row):
        return(self.matrix[row * 4:row * 4 + 4])

    def get_col(self, col):
        return(self.matrix[col::4])

    def set(self, row, col, value):
        self.matrix[(row + 1) * (col + 1) -1] = value

    @staticmethod
    def get_rot_x_matrix(theta_degree):
        theta = theta_degree * math.pi / 180
        sin = math.sin(theta)
        cos = math.cos(theta)
        return(Matrix3([
            1, 0, 0, 0,
            0, cos, sin, 0,
            0, -sin, cos, 0,
            0, 0, 0, 0
            ]))

    @staticmethod
    def get_rot_y_matrix(theta_degree):
        theta = theta_degree * math.pi / 180
        sin = math.sin(theta)
        cos = math.cos(theta)
        return(Matrix3([
            cos, 0, -sin, 0,
            0, 1, 0, 0,
            sin, 0, cos, 0,
            0, 0, 0, 0
            ]))

    @staticmethod
    def get_rot_z_matrix(theta_degree):
        theta = theta_degree * math.pi / 180
        sin = math.sin(theta)
        cos = math.cos(theta)
        return(Matrix3([
            cos, sin, 0, 0,
            -sin, cos, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 0
            ]))

    @staticmethod
    def get_shift_matrix(x, y, z):
        return(Matrix3([
            1, 0, 0, x,
            0, 1, 0, y,
            0, 0, 1, z,
            0, 0, 0, 0,
            ]))

    def __add__(self, other):
        ret = Matrix3(map(operator.add, self.matrix, other.matrix))
        return(ret)

    def __iadd__(self, other):
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                self.matrix[row][col] += other[row][col]
        return(self)

    def __sub__(self, other):
        ret = Matrix3(map(operator.sub, self.matrix, other.matrix))
        return(ret)

    def __isub__(self, other):
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                self.matrix[row][col] -= other[row][col]
        return(self)

    def __mul__(self, other):
        logging.debug("__mul__(%s)", other)
        # matrix multiplication
        if isinstance(other, Matrix3):
            """
            multiply matrix by matrix
            |a11 a12 a13 a14|   |b11 b12 b13 b14|   |(a11*b11+a12*b21+a13*b31+a14*b41) ...
            |a21 a22 a23 a24| * |b21 b22 b23 b24| = 
            |a31 a32 a33 a34|   |b31 b32 b33 b34|
            |a41 a42 a43 a44|   |b41 b42 b43 b44|
            """
            ret = Matrix3()
            for row in (0, 1, 2, 3):
                for col in (0, 1, 2, 3):
                    for row2 in (0, 1, 2, 3):
                        ret.set(row, col, ret.get(row, col) + self.get(row, row2) * other.get(row2, col))
        elif isinstance(other, Vec3d):
            """
            multiply self with vector given
            |x| |t11 t12 t13 t14| |x * t11 + y * t12 + z * t13 + 1 * t14| 
            |y|*|t21 t22 t23 t24|=|x * t21 + y * t22 + z * t23 + 1 * t24|
            |z| |t31 t32 t33 t34| |x * t31 + y * t32 + z * t33 + 1 * t34|
            |1| |t41 t42 t43 t44| |x * t41 + y * t42 + z * t43 + 1 * t44|
            """
            ret = Vector3d((0.0, 0.0, 0.0, 1))
            for row in (0, 1, 2, 3):
                for col in (0, 1, 2, 3):
                    ret[row] += vector[col] * self.get(row, col)
            return(ret)
        else:
            """
            scalar multiplication returns matrix
            """
            ret = Matrix3(map(operator.mul, self.matrix, [other] * 16))
        return(ret)

    def __neg__(self):
        """negate every cell"""
        return(self.__o1__(operator.neg))

    def __pos__(self):
        """positive of every value"""
        return(self.__o1__(operator.pos))

    def __inv__(self):
        """bitwise invert every value"""
        return(self.__o1__(operator.inv))
    __invert__ = __inv__

    def __o1__(self, func):
        """invert every cell"""
        ret = Matrix3(0, 0, 0, 1)
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                ret.set(row, col, func(self.get(row, col)))
        return(ret)

    def __str__(self):
        stringbuffer = "" 
        for row in (0, 1, 2, 3):
            stringbuffer += "|" + ", ".join(str(v) for v in self.get_row(row)) + "|\n"
        return(stringbuffer)

    def __repr__(self):
        return("Matrix3(%s)" % self.matrix)

    def __eq__(self, other):
        if isinstance(other, Matrix3)  and self.matrix == other.matrix:
            return(True)
        return(False)

    def __getitem__(self, row):
        return(self.matrix[row])

    def __setitem__(self, *key):
        print keys

    def add_transpose(self, tx, ty, tz):
        self.set(0, 3, tx)
        self.set(1, 3, ty)
        self.set(2, 3, tz)

    def transpose(self):
        ret = Matrix3(0, 0, 0, 0)
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                ret.set(row, col, self.get(col, row))
        return(ret)

    @staticmethod
    def project(vector):
        """
        |x| |1  0  0  0|
        |y|*|0  1  0  0|
        |z| |0  0 -1 -1|
        |w| |0  0  0  0|
        """
        assert len(vector) == 4
        return((vector[0]/-vector[2], vector[1]/-vector[2]))
    
        
def test():
    try:
        fps = 60
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        m1 = Matrix3(1, 1, 1, 1)
        print "M1 =\n%s" % m1
        assert m1 == Matrix3([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
        m2 = Matrix3(2, 2, 2, 1)
        print "M2 =\n%s" % str(m2)
        assert m2 == Matrix3([2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1])
        result = m1 + m2
        print "M1 + M2 =\n%s" % result
        assert result == Matrix3([3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2])
        result = m1 - m2
        print "M1 - M2 =\n%s" % result
        assert result == Matrix3([-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0])
        result = m2 - m1
        print "M2 - M1 =\n%s" % result
        assert result == Matrix3([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]) 
        result = m1 * 2
        print "M1 * 2 =\n%s" % result
        assert result == Matrix3([2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2])
        result = m1 * m2
        print "M1 * M2 =\n%s" % result
        print result.__repr__()
        sys.exit(0)
        result = m1.transpose()
        print "transpose M1 =\n%s" % result
        result =  -m1
        print "negate M1 =\n%s" % result
        result =  +m1
        print "pos M1 =\n%s" % result
        result =  ~m1
        print "inv M1 =\n%s" % result
        result = Matrix3.get_shift_matrix(1, 1, 1) * m1
        print "shift M1 =\n%s" % result
        assert (m1 * 2) == m2
        vec = Vector3d((1, 1, 1, 1))
        test = vector * vec
        print test
        sys.exit(0)
        # rotattion matrix around 1 degree counter clockwise
        rot = Matrix3.get_rot_x_matrix(1)
        print "rotation matrix: %s" % rot
        shift = Matrix3.get_shift_matrix(300, 300, -2)
        print "shift matrix: %s" % shift
        scale = Matrix3(100, 100, 1, 0)
        print "scale matrix: %s" % scale
        shift_scale = shift * scale
        print "shift_scale: %s" % shift_scale
        clock = pygame.time.Clock()       
        while True:
            clock.tick(fps)
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
            surface.fill(0)
            print "scaled : %s" % scale.vmul(vector)
            print "shifted: %s" % shift.vmul(vector)
            print "shift+scaled : %s" % shift.vmul(scale.vmul(vector))
            pygame.draw.line(surface, (100, 0, 0), (300, 300), Matrix3.project(shift.vmul(scale.vmul(vector))))
            vector = rot.vmul(vector)
            pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == '__main__':
    test()

