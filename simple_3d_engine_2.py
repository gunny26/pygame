#!/usr/bin/python3
import sys
import math
import time
# non std
import pygame

class Vec2d:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vec3d:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3d(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
            )

    def __sub__(self, other):
        return Vec3d(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
            )

    def __mul__(self, scalar):
        return Vec3d(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar
            )

    def __div__(self, scalar):
        return Vec3d(
            self.x / scalar,
            self.y / scalar,
            self.z / scalar
            )

    def cross(self, other):
        """
        return the cross product of self and other
        :returns Vec3d:
        """
        return Vec3d(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
            )

    def normalize(self):
        """
        return normalized version of Vec4d
        :returns Vec3d:
        """
        length = self.length()
        return self.__div__(length)

    def length(self):
        """
        return length of verctor, MISSING w part
        :returns float:
        """
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def dot(self, other):
        """
        return dot product of self and ohter Vec3d
        :returns float:
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

class Vec4d:

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

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
        return the cross product of self and other as Vec3d
        :returns Vec3d:
        """
        return Vec3d(
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
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.points = [v1, v2, v3]

    def __getitem__(self, index):
        return self.points[index]

    def normal(self):
        """
        return normal vector fr this triangle
        :returns Vec3d:
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
                    vertices.append(Vec3d(*[float(part) for part in parts[1:]]))
                if parts[0] == "f": # a face
                    # something like: f 2/1/1 3/2/1 4/3/1
                    t_vertices = [int(part.split("/")[0])-1 for part in parts[1:]]
                    triangles.append(Triangle(vertices[t_vertices[0]], vertices[t_vertices[1]], vertices[t_vertices[2]]))
            return Mesh(triangles)

class Matrix4x4:

    def __init__(self, vecs):
        self.vecs = vecs

    def __mul__(self, vec3d):
        vec4d = Vec4d(*[
            vec3d.x * self.vecs[0][0] + vec3d.y * self.vecs[1][0] + vec3d.z * self.vecs[2][0] + self.vecs[3][0],
            vec3d.x * self.vecs[0][1] + vec3d.y * self.vecs[1][1] + vec3d.z * self.vecs[2][1] + self.vecs[3][1],
            vec3d.x * self.vecs[0][2] + vec3d.y * self.vecs[1][2] + vec3d.z * self.vecs[2][2] + self.vecs[3][2],
            vec3d.x * self.vecs[0][3] + vec3d.y * self.vecs[1][3] + vec3d.z * self.vecs[2][3] + self.vecs[3][3]
        ])
        if vec4d.w != 0.0:
            vec4d.x /= vec4d.w
            vec4d.y /= vec4d.w
            vec4d.z /= vec4d.w
        return vec4d

    @staticmethod
    def get_rot_x(f_theta):
        """get rotation matrix around x"""
        return Matrix4x4([
            [ 1,                 0,                  0, 0 ],
            [ 0, math.cos(f_theta), -math.sin(f_theta), 0 ],
            [ 0, math.sin(f_theta),  math.cos(f_theta), 0 ],
            [ 0,                 0,                  0, 1 ]
        ])

    @staticmethod
    def get_rot_y(f_theta):
        """get rotation matrix around y"""
        return Matrix4x4([
            [  math.cos(f_theta), 0, math.sin(f_theta), 0 ],
            [                  0, 1,                 0, 0 ],
            [ -math.sin(f_theta), 0, math.cos(f_theta), 0 ],
            [                  0, 0,                 0, 1 ]
        ])

    @staticmethod
    def get_rot_z(f_theta):
        """get rotation matrix around z"""
        return Matrix4x4([
            [ math.cos(f_theta), -math.sin(f_theta), 0, 0 ],
            [ math.sin(f_theta),  math.cos(f_theta), 0, 0 ],
            [                 0,                  0, 1, 0 ],
            [                 0,                  0, 0, 1 ]
        ])

    def get_projection(aspect, fov, q, z_near):
        """return projection matrix"""
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
            rot_y = Matrix4x4.get_rot_y(f_theta)
            rot_z = Matrix4x4.get_rot_z(f_theta * 0.5)

            raster_triangles =[] # put triangles to draw in
            # do projection
            for triangle in model:

                # rotate z
                t_z = triangle * rot_z

                # rotate x
                t_x = t_z * rot_x

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
        print('shutting down')
