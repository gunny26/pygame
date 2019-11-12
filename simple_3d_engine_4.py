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
import pyximport; pyximport.install()
import sys
import math
import time
# non std
import pygame
# own modules
from Simple3dEngine import Vec4d, Matrix4x4, Mesh, Triangle

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
        font = pygame.font.Font(None, 20) # to display FPS an some infos
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
        # define light position
        light = Vec4d(0, 0, 3, 0)
        # load from file, the self defined cube has some error
        model = Mesh.from_file("obj_models/teapot.obj")
        print(model)
        model_position = Vec4d(0, 0, 5, 0)
        counter = 0
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
            trans = Matrix4x4.get_translate(Vec4d(0, 0, 5, 1))
            rot_total = rot_total.mul_matrix(trans) # adding translation

            raster_triangles =[] # put triangles to draw in
            # do rotation, projection, translation, scaling
            for triangle in model:

                # rotate around x an z with combined rotation matrix, afterwards project
                t_p = (triangle * rot_total) * projection_matrix

                # calculate normal to triangle
                t_normal = t_p.normal()
                # calculate dot product of camera and normalized vector
                camera_v = (t_p.v1 - camera).normalize() # camera vector normalized
                if camera_v.dot(t_normal) > 0.0:
                #if t_normal.z > 0.0: # normals not pointing in our direction, skipping
                    # z negative means, outwards, to the watching face
                    continue
                # calculate dot product of normal to light direction
                # to get the correct shadings
                light_v = (t_p.v1 - light).normalize() # light vector unit vector
                lum = max(255 * light_v.dot(t_normal), 0)
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
                #draw_triangle(surface, WHITE, t_p)
            # show FPS on screen
            fps = font.render(f"fps: {clock.get_fps()}", True, pygame.Color("red"))
            surface.blit(fps, (50, 50))
            surface.blit(font.render(f"counter: {counter}", True, pygame.Color("red")) , (50, 80))
            pygame.display.flip()
            counter += 1
            if counter >= 100:
                sys.exit(0)
    except KeyboardInterrupt:
        print("shutting down")
