#!/usr/bin/python

import pygame
import sys
import math
from Vec2d import Vec2d
from Vec3d import Vec3d


class Matrix3(object):

    def __init__(self, *args):
        print "__init__(%s)" % str(args)
        if len(args) == 4:
            self.matrix = [
                [args[0], 0, 0, 0],
                [0, args[1], 0, 0],
                [0, 0, args[2], 0],
                [0, 0, 0, args[3]]
                ]
        elif len(args) == 3:
            self.matrix = [
                [args[0], 0, 0, 0],
                [0, args[1], 0, 0],
                [0, 0, args[2], 0],
                [0, 0, 0, 1]
                ]
        else:
            self.matrix = args[0]

    @staticmethod
    def get_rot_x_matrix(theta_degree):
        theta = theta_degree * math.pi / 180
        sin = math.sin(theta)
        cos = math.cos(theta)
        return(Matrix3([
            [1, 0, 0, 0],
            [0, cos, sin, 0],
            [0, -sin, cos, 0],
            [0, 0, 0, 0]
            ]))

    @staticmethod
    def get_rot_y_matrix(theta_degree):
        theta = theta_degree * math.pi / 180
        sin = math.sin(theta)
        cos = math.cos(theta)
        return(Matrix3([
            [cos, 0, -sin, 0],
            [0, 1, 0, 0],
            [sin, 0, cos, 0],
            [0, 0, 0, 0]
            ]))

    @staticmethod
    def get_rot_z_matrix(theta_degree):
        theta = theta_degree * math.pi / 180
        sin = math.sin(theta)
        cos = math.cos(theta)
        return(Matrix3([
            [cos, sin, 0, 0],
            [-sin, cos, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]
            ]))

    @staticmethod
    def get_shift_matrix(x, y, z):
        return(Matrix3([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 0],
            ]))

    def __add__(self, other):
        ret = Matrix3(0, 0, 0, 0)
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                ret[row][col] = self.matrix[row][col] + other[row][col]
        return(ret)

    def __iadd__(self, other):
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                self.matrix[row][col] += other[row][col]
        return(self)

    def __sub__(self, other):
        ret = Matrix3(0, 0, 0, 0)
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                ret[row][col] = self.matrix[row][col] - other[row][col]
        return(ret)

    def __isub__(self, other):
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                self.matrix[row][col] -= other[row][col]
        return(self)

    def __mul__(self, other):
        print "__mul__(%s)" % other
        ret = Matrix3(0, 0, 0, 0)
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                sb = ""
                for row2 in (0, 1, 2, 3):
                    sb += "%s * %s + " % (self.matrix[row][row2], other[row2][col])
                    ret[row][col] = ret[row][col] + self.matrix[row][row2] * other[row2][col]
        return(ret)

    def __str__(self):
        string = "" 
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                string += str(self.matrix[row][col]) + " "
            string += "\n"
        return(string)

    def __getitem__(self, row):
        return(self.matrix[row])

    def __setitem__(self, *key):
        print keys

    def add_transpose(self, tx, ty, tz):
        self.matrix[0][3] = tx
        self.matrix[1][3] = ty
        self.matrix[2][3] = tz

    def transpose(self):
        ret = Matrix3(0, 0, 0, 0)
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                ret[row][col] = self.matrix[col][row]
        return(ret)

    def vmul(self, vector):
        """
        multiply self with vector given
        |x| |t11 t12 t13 t14| |x * t11 + y * t12 + z * t13 + 1 * t14| 
        |y|*|t21 t22 t23 t24|=|x * t21 + y * t22 + z * t23 + 1 * t24|
        |z| |t31 t32 t33 t34| |x * t31 + y * t32 + z * t33 + 1 * t34|
        |1| |t41 t42 t43 t44| |x * t41 + y * t42 + z * t43 + 1 * t44|
        """
        assert len(vector) == 4
        ret_vector = [0.0, 0.0, 0.0, 1]
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                ret_vector[row] += vector[col] * self.matrix[row][col]
        return(ret_vector)

    def scale(self, scalar):
        """
        multiply self with scalar
                 |t11 t12 t13 t14|
        |scalar|*|t21 t22 t23 t24|
                 |t31 t32 t33 t34|
                 |t41 t42 t43 t44| 
        """
        assert len(vector) == 4
        ret_vector = [0.0, 0.0, 0.0, 1]
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                ret_vector[row] += vector[col] * self.matrix[row][col]
        return(ret_vector)

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
        vector = (1, 0, 1, 1)
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

