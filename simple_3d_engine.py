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

class Vec4d:

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

class Triangle:

    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

class Mesh:

    def __init__(self, triangles):
        self.triangles = triangles

    def __getitem__(self, index):
        return self.triangles[index]

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

def draw_triangle(surface, color, triangle):
    pygame.draw.line(surface, color, (triangle.v1.x, triangle.v1.y), (triangle.v2.x, triangle.v2.y), 1)
    pygame.draw.line(surface, color, (triangle.v2.x, triangle.v2.y), (triangle.v3.x, triangle.v3.y), 1)
    pygame.draw.line(surface, color, (triangle.v3.x, triangle.v3.y), (triangle.v1.x, triangle.v1.y), 1)


if __name__=='__main__':

    try:
        surface = pygame.display.set_mode((600,600))
        pygame.init()
        # constants
        FPS = 20
        WHITE = (255, 255, 255) # white
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
        projection_matrix = Matrix4x4([
            [ aspect * fov, 0  , 0          , 0],
            [ 0           , fov, 0          , 0],
            [ 0           , 0  , q          , 1],
            [ 0           , 0  , -z_near * q, 0]
        ])
        # define cube, all triangle in same direction
        cube = Mesh([
            Triangle(Vec3d(0, 0, 0), Vec3d(0, 1, 0), Vec3d(1, 1, 0)), # south
            Triangle(Vec3d(1, 1, 0), Vec3d(1, 0, 0), Vec3d(0, 0, 0)), # south
            Triangle(Vec3d(1, 0, 0), Vec3d(1, 1, 0), Vec3d(1, 1, 1)), # east
            Triangle(Vec3d(1, 1, 1), Vec3d(1, 0, 1), Vec3d(1, 0, 0)), # east
            Triangle(Vec3d(0, 0, 1), Vec3d(0, 1, 1), Vec3d(0, 1, 0)), # west
            Triangle(Vec3d(0, 1, 0), Vec3d(0, 0, 0), Vec3d(0, 0, 1)), # west
            Triangle(Vec3d(1, 0, 1), Vec3d(1, 1, 1), Vec3d(0, 0, 1)), # north
            Triangle(Vec3d(0, 0, 1), Vec3d(0, 1, 1), Vec3d(1, 1, 1)), # north
            Triangle(Vec3d(0, 0, 1), Vec3d(0, 0, 0), Vec3d(1, 0, 0)), # bottom
            Triangle(Vec3d(1, 0, 0), Vec3d(1, 0, 1), Vec3d(0, 0, 1)), # bottom
            Triangle(Vec3d(0, 1, 0), Vec3d(0, 1, 1), Vec3d(1, 1, 1)), # top
            Triangle(Vec3d(1, 1, 1), Vec3d(1, 1, 0), Vec3d(0, 1, 0))  # top
            ])

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
            rot_x = Matrix4x4([
                [ 1,                 0,                  0, 0 ],
                [ 0, math.cos(f_theta), -math.sin(f_theta), 0 ],
                [ 0, math.sin(f_theta),  math.cos(f_theta), 0 ],
                [ 0,                 0,                  0, 1 ]
            ])
            rot_y = Matrix4x4([
                [  math.cos(f_theta), 0, math.sin(f_theta), 0 ],
                [                  0, 1,                 0, 0 ],
                [ -math.sin(f_theta), 0, math.cos(f_theta), 0 ],
                [                  0, 0,                 0, 1 ]
            ])
            rot_z = Matrix4x4([
                [ math.cos(f_theta * 0.5), -math.sin(f_theta * 0.5), 0, 0 ],
                [ math.sin(f_theta * 0.5),  math.cos(f_theta * 0.5), 0, 0 ],
                [                       0,                        0, 1, 0 ],
                [                       0,                        0, 0, 1 ]
            ])
           # do projection
            for triangle in cube:

                # rotate z
                t_z = Triangle(*[
                    rot_z * triangle.v1,
                    rot_z * triangle.v2,
                    rot_z * triangle.v3
                ])

                # rotate x
                t_x = Triangle(*[
                    rot_x * t_z.v1,
                    rot_x * t_z.v2,
                    rot_x * t_z.v3
                ])

                # translate into Z
                t_t = Triangle(*[
                    Vec3d(t_x.v1.x, t_x.v1.y, t_x.v1.z + 3.0),
                    Vec3d(t_x.v2.x, t_x.v2.y, t_x.v2.z + 3.0),
                    Vec3d(t_x.v3.x, t_x.v3.y, t_x.v3.z + 3.0)
                ])

                # project
                t_p = Triangle(*[
                    projection_matrix * t_t.v1,
                    projection_matrix * t_t.v2,
                    projection_matrix * t_t.v3
                ])

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
                t_p.v2.x *= width/2
                t_p.v2.y *= height / 2
                t_p.v3.x *= width/2
                t_p.v3.y *= height / 2

                draw_triangle(surface, WHITE, t_p)
            pygame.display.flip()
    except KeyboardInterrupt:
        print('shutting down')
