#!/usr/bin/python3
"""
simple 3d engine written in pure python and pygame for graphics display

this attempt has educational focus, i fo not think it will be anywhere
near as fast as compiled optimized versions or GPU based versions.

the main goal is:
    how do 3D Engines work
    projection / shading / depth buffer (kind-of) / clipping
    what can be optimize algorithmically (matrices)
    what can be optimized with python (cython?, numpy?)

lets see how far we get

first version - projection, triangles
second version - shading, loading of obj files, refactoring
third version - refactoring, texture
"""

import sys
import math
import time
# non std
import pygame

class Vec4d:

    def __init__(self, x, y, z, w=0.0):
    # also store list of values):
        """
        vector in 3 dimensional space, additional w component
        """
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        # also store list of values
        self._data = [self.x, self.y, self.z, self.w]

    def __add__(self, other):
        return Vec4d(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
            self.w + other.w
            )

    def __sub__(self, other):
        return Vec4d(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            self.w - other.w
            )

    def __getitem__(self, index):
        return self._data[index]

    def length3(self):
        """
        return length of verctor, MISSING w part
        """
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def length(self):
        """
        return length of verctor, including w part
        """
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)

    def cross(self, other):
        """
        return the cross product of self and other as Vec4d
        :returns Vec4d:
        """
        return Vec4d(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
            )

    def normalize(self):
        """
        return normalized version of Vec4d
        :returns Vec4d:
        """
        length = self.length()
        return Vec4d(self.x / length, self.y / length, self.z / length, self.w / length)

    def dot(self, other):
        """
        return dot product of self and ohter Vec4d
        TODO: what todo with this w component?
        :returns float:
        """
        return self.x * other.x + self.y * other.y + self.z * other.z


class Triangle:

    def __init__(self, v1, v2, v3):
        """
        :params v1 <Vec4d>: first vertex
        :params v2 <Vec4d>: second vertex
        :params v3 <Vec4d>: third vertex
        """
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.points = [v1, v2, v3]

    def __getitem__(self, index):
        return self.points[index]

    def normal(self):
        """
        return normal vector fr this triangle
        :returns Vec4d:
        """
        return (self.v2 - self.v1).cross(self.v3 - self.v1)

    def translate(self, vec4d):
        """
        translate this triangle
        :params vec4d:
        :returns Triangle:
        """
        return Triangle(*[
            self.v1 + vec4d,
            self.v2 + vec4d,
            self.v3 + vec4d
        ])

    def __mul__(self, matrix):
        """
        multiply self with matrix, must be 4 x 4
        :params Matrix4x4:
        :return Triangle:
        """
        return Triangle(*[
            matrix * self.v1,
            matrix * self.v2,
            matrix * self.v3
        ])

    def avg_z(self):
        return (self.v1.z + self.v2.z + self.v3.z) / 3

    def __lt__(self, other):
        """
        compare self with other, use in painters algorithm
        """
        return self.avg_z() > other.avg_z()

    def __gt__(self, other):
        """
        compare self with other, use in painters algorithm
        """
        return self.avg_z() < other.avg_z()



class Mesh:

    def __init__(self, triangles):
        self.triangles = triangles

    def __getitem__(self, index):
        return self.triangles[index]

    @staticmethod
    def from_file(filename):
        with open(filename, "rt") as infile:
            vertices = []
            triangles = []
            for line in infile:
                if not line or line[0] == "#":
                    continue
                parts = line.strip().split()
                if not parts:
                    continue
                if parts[0] == "v": # a vertex
                    # something like: v -1.000000 -1.000000 -1.000000
                    vertices.append(Vec4d(*[float(part) for part in parts[1:]]))
                if parts[0] == "f": # a face
                    # something like: f 2/1/1 3/2/1 4/3/1
                    t_vertices = [int(part.split("/")[0])-1 for part in parts[1:]]
                    triangles.append(Triangle(vertices[t_vertices[0]], vertices[t_vertices[1]], vertices[t_vertices[2]]))
            return Mesh(triangles)

class Matrix4x4:
    """Helper class for matrix operations"""

    def __init__(self, vecs):
        """
        :params vecs list of 4 Vec4d:
        """
        self.vecs = vecs

    def __str__(self):
        output = ""
        for vec in self.vecs:
            output += "| " + " | ".join((f"{value:22}" for value in vec)) + " |\n"
        return output

    def __getitem__(self, index):
        return self.vecs[index]

    def __setitem__(self, index, value):
        print(index)

    def __mul__(self, vec3d):
        """
        multiply this matrix by vector 4D
        :params <Vec4d>: input vector to multiply with this matrix
        :returns <Vec4d>: new vector
        """
        vec4d = Vec4d(*[
            vec3d.x * self.vecs[0][0] + vec3d.y * self.vecs[1][0] + vec3d.z * self.vecs[2][0] + self.vecs[3][0], # x
            vec3d.x * self.vecs[0][1] + vec3d.y * self.vecs[1][1] + vec3d.z * self.vecs[2][1] + self.vecs[3][1], # y
            vec3d.x * self.vecs[0][2] + vec3d.y * self.vecs[1][2] + vec3d.z * self.vecs[2][2] + self.vecs[3][2], # z
            vec3d.x * self.vecs[0][3] + vec3d.y * self.vecs[1][3] + vec3d.z * self.vecs[2][3] + self.vecs[3][3]  # w
        ])
        if vec4d.w != 0.0:
            vec4d.x /= vec4d.w
            vec4d.y /= vec4d.w
            vec4d.z /= vec4d.w
        return vec4d

    def mul_matrix(self, other):
        """
        multiply self by Matrix4x4

        |a11 a12 a13 a14|   |b11 b12 b13 b14|   |(a11*b11+a12*b21+a13*b31+a14*b41) ...
        |a21 a22 a23 a24| * |b21 b22 b23 b24| =
        |a31 a32 a33 a34|   |b31 b32 b33 b34|
        |a41 a42 a43 a44|   |b41 b42 b43 b44|

        :params other <Matrix4x4>: Matrix B in A * B
        :returns <Matrix4x4>:
        """
        ret = Matrix4x4.get_zero() # get zero matrix
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                for row2 in (0, 1, 2, 3):
                    ret[row][col] = ret[row][col] + self[row][row2] * other[row2][col]
        return ret

    @staticmethod
    def get_zero():
        """
        get zero matrix
        :returns <Matrix4x4>:
        """
        return Matrix4x4([
            [ 0, 0, 0, 0 ],
            [ 0, 0, 0, 0 ],
            [ 0, 0, 0, 0 ],
            [ 0, 0, 0, 0 ]
        ])

    @staticmethod
    def get_identity():
        """
        get identity matrix
        :returns <Matrix4x4>:
        """
        return Matrix4x4([
            [ 1, 0, 0, 0 ],
            [ 0, 1, 0, 0 ],
            [ 0, 0, 1, 0 ],
            [ 0, 0, 0, 1 ]
        ])

    @staticmethod
    def get_rot_x(f_theta):
        """
        get rotation matrix around x
        :params f_theta <float>:
        :returns <Matrix4x4>:
        """
        return Matrix4x4([
            [ 1,                 0,                  0, 0 ],
            [ 0, math.cos(f_theta), -math.sin(f_theta), 0 ],
            [ 0, math.sin(f_theta),  math.cos(f_theta), 0 ],
            [ 0,                 0,                  0, 1 ]
        ])

    @staticmethod
    def get_rot_y(f_theta):
        """
        get rotation matrix around y
        :params f_theta <float>:
        :returns <Matrix4x4:
        """
        return Matrix4x4([
            [  math.cos(f_theta), 0, math.sin(f_theta), 0 ],
            [                  0, 1,                 0, 0 ],
            [ -math.sin(f_theta), 0, math.cos(f_theta), 0 ],
            [                  0, 0,                 0, 1 ]
        ])

    @staticmethod
    def get_rot_z(f_theta):
        """
        get rotation matrix around z
        :params f_theta <float>:
        :returns <Matrix4x4:
        """
        return Matrix4x4([
            [ math.cos(f_theta), -math.sin(f_theta), 0, 0 ],
            [ math.sin(f_theta),  math.cos(f_theta), 0, 0 ],
            [                 0,                  0, 1, 0 ],
            [                 0,                  0, 0, 1 ]
        ])

    @staticmethod
    def get_translate(vec):
        """
        get translation matrix from given Vec4d
        TODO: not sure if this correct
        :params f_theta <float>:
        :returns <Matrix4x4:
        """
        return Matrix4x4([
            [ 1, 0, vec[0], 0 ],
            [ 0, 1, vec[1], 0 ],
            [ 0, 0, vec[2], 0 ],
            [ 0, 0, 0, 1 ]
        ])

    @staticmethod
    def get_projection(aspect, fov, q, z_near=0.1):
        """
        return projection matrix
        :params aspect <float>: aspect ratiion height/width
        :params fov <float>: field of view 1 / tan(theta/2))
        :params q <float>: z_far / (z_far - z_near)
        :params znear <float>: z_near value, defaults 0.1
        :returns <Matrix4x4:
        """
        return Matrix4x4([
            [ aspect * fov, 0  , 0          , 0],
            [ 0           , fov, 0          , 0],
            [ 0           , 0  , q          , 1],
            [ 0           , 0  , -z_near * q, 0]
        ])


def draw_triangle(surface, color, triangle):
    points = [(p.x, p.y) for p in triangle]
    pygame.draw.polygon(surface, color, points, 1)

def draw_filled_triangle(surface, color, triangle):
    points = [(p.x, p.y) for p in triangle]
    pygame.draw.polygon(surface, color, points, 0)

if __name__=='__main__':

    try:
        surface = pygame.display.set_mode((600,600))
        pygame.init()
        # constants
        FPS = 60
        WHITE = (255, 255, 255) # white
        GRAY = (100, 100, 100) # Gray
        clock = pygame.time.Clock()
        width = surface.get_width()
        height = surface.get_height()
        theta = 90.0 # sixtee degree
        z_near = 0.1
        z_far = 1000.0
        # some well known terms
        fov = 1 / math.tan(theta / 2) # field of view
        aspect = width / height
        q = z_far / (z_far - z_near) # z projection
        # help:
        # x = aspect * fov * x / z
        # y = fov * y / z
        # z = z * (q - q * z_near)
        projection_matrix = Matrix4x4.get_projection(aspect, fov, q, z_near)
        # define Camera position
        camera = Vec4d(0, 0, 0, 0)
        # define light direction
        light = Vec4d(1, 2, 3, 0)
        #light_direction = Vec4d(0, 0, -1, 0).normalize()
        # load from file, the self defined cube has some error
        model = Mesh.from_file("obj_models/teapot.obj")
        model_position = Vec4d(0, 0, 5, 0)
        while True:
            clock.tick(FPS)
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
            # create rotation matrix around x and z axis
            f_theta = time.time()
            rot_x = Matrix4x4.get_rot_x(f_theta)
            rot_z = Matrix4x4.get_rot_z(f_theta * 0.5)
            rot_total = rot_x.mul_matrix(rot_z) # combined matrix

            raster_triangles =[] # put triangles to draw in
            # do rotation, projection, translation, scaling
            for triangle in model:

                # rotate around x an z with combined rotation matrix
                t_x = triangle * rot_total

                # translate into Z
                t_t = t_x.translate(model_position)

                # project to 2D
                t_p = t_t * projection_matrix

                # calculate normal to triangle
                t_normal = t_p.normal().normalize()
                # calculate dot product of camera and normalized vector
                camera_v = t_p.v1 - camera # camera vector
                if camera_v.dot(t_normal) > 0.0:
                #if t_normal.z > 0.0: # normals not pointing in our direction, skipping
                    # z negative means, outwards, to the watching face
                    continue
                # calculate dot product of normal to light direction
                # to get the correct shadings
                light_v = (t_p.v1 - light).normalize() # light vector
                lum = 128 * light_v.dot(t_normal) + 128
                color = (lum, lum, lum)

                # shift to positive values
                t_p.v1.x += 1.0
                t_p.v1.y += 1.0
                t_p.v2.x += 1.0
                t_p.v2.y += 1.0
                t_p.v3.x += 1.0
                t_p.v3.y += 1.0

                # scale by half the screen
                t_p.v1.x *= width / 2
                t_p.v1.y *= height / 2
                t_p.v2.x *= width / 2
                t_p.v2.y *= height / 2
                t_p.v3.x *= width / 2
                t_p.v3.y *= height / 2

                raster_triangles.append((t_p, color))

            for t_p, color in sorted(raster_triangles):
                # drawing triangles to show from back to front
                draw_filled_triangle(surface, color, t_p)
                draw_triangle(surface, WHITE, t_p)

            pygame.display.flip()
    except KeyboardInterrupt:
        print("shutting down")
