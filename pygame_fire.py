#!/usr/bin/python3

import pygame
from pygame import gfxdraw
import sys
import math
import random
import numpy
import time
from Vec2d import Vec2d
from Vec3d import Vec3d

FPS = 1000

def generator(start, stop, step):
    value = start
    while value <= stop:
        yield value
        value += step

def step_generator(start, stop, steps):
    distance = stop - start
    step = float(distance) / float(steps)
    value = float(start)
    while value <= stop:
        yield value
        value += step

def randint_generator(minimum, maximum, amount):
    for i in xrange(amount):
        yield random.randint(minimum, maximum)

def random_generator(minimum, maximum, amount):
    for i in xrange(amount):
        yield minimum + random.random() * (maximum - minimum)



class SinusText(object):

    def __init__(self, surface, text, hpos, amplitude, frequency, color, size=30):
        self.surface = surface
        appendix = " " * (self.surface.get_width() / size)
        self.text = appendix + text + appendix
        self.hpos = hpos
        self.amplitude = amplitude
        self.frequency = frequency
        self.color = color
        self.size = size
        # initialize
        self.font = None
        self.initialize()

    def initialize(self):
        self.x = 0
        self.faktor = 2 * math.pi / self.surface.get_width()
        self.font = pygame.font.SysFont("mono", self.size, bold=True)
        self.text_surface = self.font.render(self.text, True, self.color)

    def char_getter(self, index):
        return(self.font_surfaces[int(index % len(self.text))])

    def update(self, hpos=None):
        if hpos is not None:
            self.hpos = hpos
        for offset in range(self.text_surface.get_width()):
            self.surface.blit(self.text_surface, (0 + offset, self.hpos + math.sin(offset * self.frequency * self.faktor) * self.amplitude), (self.x + offset, 0, 1, self.size))
        if self.x < self.text_surface.get_width():
            self.x += 1
        else:
            self.x = 0
 

class ScrollText(object):

    def __init__(self, surface, text, hpos, color, size=30):
        self.surface = surface
        appendix = " " * (self.surface.get_width() / size)
        self.text = appendix + text + appendix
        self.hpos = hpos
        self.color = color
        self.size = size
        # initialize
        self.initialize()

    def initialize(self):
        self.x = 0
        self.font = pygame.font.SysFont("mono", self.size, bold=True)
        self.text_surface = self.font.render(self.text, True, self.color)

    def char_getter(self, index):
        return(self.font_surfaces[int(index % len(self.text))])

    def update(self, hpos=None):
        if hpos is not None:
            self.hpos = hpos
        self.surface.blit(self.text_surface, (0, self.hpos), (self.x, 0, self.surface.get_width(), self.size))
        if self.x < self.text_surface.get_width():
            self.x += 1
        else:
            self.x = 0
            

class InfoRenderer(object):

    def __init__(self, surface, pos=Vec2d(100,100), size=10, color=pygame.Color(0, 255, 0)):
        self.surface = surface
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont('mono', self.size, bold=True)
        self.pos = pos
        self.last_tick = time.time()

    def update(self, lines):
        fps = 1 / (time.time()-self.last_tick)
        self.draw_text("Frames per second %f" % fps, offset=Vec2d(0, 0))
        counter = 1
        for line in lines:
            self.draw_text(line, offset=Vec2d(0, self.size * counter))
            counter += 1
        self.last_tick = time.time()

    def draw_text(self, text, offset):
        """Center text in window"""
        fw, fh = self.font.size(text)
        font_surface = self.font.render(text, True, self.color)
        self.surface.blit(font_surface, self.pos + offset)


class Fire(object):
    """
    Simulated Fire
    idea and basic algorithm from
    http://lodev.org/cgtutor/fire.html
    """

    def __init__(self, surface, dest, width, height, scale=4):
        self.surface = surface
        self.dest = dest
        self.width = width / scale
        self.height = height / scale
        self.scale = scale
        self.drawsurface = pygame.Surface((self.width, self.height))
        self.array2d = None
        self.fire = None
        self.initialize()

    def initialize(self):
        # self.drawsurface.fill((0, 0, 0))
        self.array2d = pygame.surfarray.array2d(self.drawsurface)
        self.fire = numpy.zeros((self.width, self.height))
        # generate palette
        self.palette = numpy.zeros(255)
        # aplette should be something from black to yellow red
        self.palette[0] = pygame.Color(0, 0, 0, 255)
        for index in range(1,255):
            color = pygame.Color(0, 0, 0, 255)
            #    //Hue goes from 0 to 85: red to yellow
            #    //Saturation is always the maximum: 255
            #    //Lightness is 0..100 for x=0..128, and 255 for x=128..255
            #    color = HSLtoRGB(ColorHSL(x / 3, 255, std::min(255, x * 2)));
            color.hsla = (index, 100, index / 2.55, 10)
            self.palette[index] = color

    def update(self, **kwds):
        w = self.width
        h = self.height
        # random baseline
        for x in range(w):
            self.fire[x][h - 1] = abs(32768 + random.randint(0, 32768)) % 256
        # calculate each pixel according to neighbours
        for y in range(h - 1):
            for x in range(w):
                self.fire[x][y]= \
                    ((self.fire[(x - 1) % w][(y + 1) % h] \
                    + self.fire[(x) % w][(y + 2) % h] \
                    + self.fire[(x + 1) % w][(y + 1) % h] \
                    + self.fire[(x) % w][(y + 3) % h]) \
                    * 16) / 65
                # the last factor 16/65 should be slightly larger than 4
                # and lesser than 5
                # closer to 4 will make flames higher
                self.array2d[x][y] = self.palette[int(self.fire[x][y])]
        pygame.surfarray.blit_array(self.drawsurface, self.array2d)
        blitsurface = pygame.transform.scale(self.drawsurface, (self.width * self.scale, self.height * self.scale))
        self.surface.blit(blitsurface, self.dest)


class Starfield(object):
    """Starfield with 3D Points"""

    def __init__(self, surface, stars, depth, speed=0.01):
        self.surface = surface
        self.color = pygame.Color(255, 255, 255, 255)
        self.deg2rad = math.pi / 180
        self.stars = stars
        self.depth = depth
        self.speed = speed
        self.generate()

    def generate(self):
        """ generates starfield, z=0 to z=depth """
        class Star(object):
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
        depth_count = self.stars / self.depth
        self.stars = []
        for x in range(depth_count):
            for y in range(depth_count):
                for z in range(depth_count):
                    x = random.random() * 4 - 2
                    y = random.random() * 4 - 2
                    z = random.random() * 4 - 2
                    self.stars.append(Vec3d(x, y, z))
        # self.stars = [Vec3d(x, y, z) for x in random_generator(-1, 1, depth_count) for y in random_generator(-1, 1, depth_count) for z in random_generator(-1, 1, depth_count)]

    def update(self, center=Vec2d(0, 0), fov=2, viewer_distance=256):
        #parray = pygame.surfarray.pixels2d(surface)
        for star in self.stars:
            tstar = star.project(surface.get_width(), surface.get_height(), viewer_distance, fov)
            tstar2d = Vec2d(tstar.x, tstar.y)
            pygame.draw.line(self.surface, self.color, tstar2d, tstar2d, 1)
            star.x -= self.speed
            if star.x < -2:
                star.x = 2


class Tree(object):
    """Tree in 3D"""

    def __init__(self, surface, color, root, depth, length):
        self.surface = surface
        self.color = color
        self.depth = depth # depth to go
        self.length = length # initial length of first branch
        self.root = root # Vec2d, root of tree position in 2d
        # The number of branches each branch splits into
        self.branchingFactor = 4
        # The angle between the branches in degrees
        self.angleBetweenBranches = 30
        # Controls how much smaller each level of the tree gets
        self.scaleFactor = 0.7
        # actual angle in degree
        self.deg2rad = math.pi / 180
        # total angle between left and rightmost branch
        self.totalAngle = self.angleBetweenBranches * (self.branchingFactor - 1)
        # draw leafs or not
        self.leafs = True
        self.storyboard = []
        self.initialize()

    def draw(self, root, angle, length, width):
        assert isinstance(root, Vec2d)
        myangle = angle * self.deg2rad
        dest = root + Vec2d(math.cos(myangle), math.sin(myangle)) * (-length)
        self.storyboard.append((pygame.draw.line, (self.surface, self.color, root, dest, width)))
        # return new root point
        return(dest)

    def tree(self, depth, length, root, angle):
        if depth == 0:
            if self.leafs is True:
                leaf_color = (random.randint(16,65), int(length * 2 + 40), 0)
                self.storyboard.append((pygame.draw.ellipse, (self.surface, leaf_color, (int(root.x), int(root.y), 10, 10), 0)))
            return
        # sets thickness of line
        # strokeWeight(self.depth / 2)
        # forward
        root = self.draw(root, angle, length, self.depth / 2)
        # turn right
        angle -= self.totalAngle / 2.0
        for i in range(self.branchingFactor):
            # next recursion, smaller
            self.tree(depth - 1, length * self.scaleFactor * (0.5 + random.random() * 0.5), root, angle)
            # turn left, one step
            angle += self.angleBetweenBranches
            # next branch
        # turn back right, and one step left
        angle -= self.totalAngle / 2.0 + self.angleBetweenBranches
        # draw back
        root = self.draw(root, angle, -length, self.depth / 2)

    def set_color(self, color):
        self.color = color

    def rotate(self, dx, dy, dz, offset2d=Vec2d(0,0), offset3d=Vec3d(0, 0, 0)):
        pass

    def initialize(self):
        self.tree(depth=self.depth, length=self.length, root=self.root, angle=90)

    def update(self, center):
        for func, args in self.storyboard:
            func(*args)


class Circle(object):
    """a Circle in 3D Space"""

    def __init__(self, surface, color, center=Vec3d(0, 0, 0), size=Vec3d(1, 1, 1), steps=36.0, viewer_distance=256, fov=2):
        self.surface = surface
        self.color = color
        self.size = size
        self.center = center
        self.steps = steps
        self.viewer_distance = viewer_distance
        self.fov = fov
        # class variables
        self.circle_raw_points = []
        self.circle = None
        self.transformed_circle = None
        # generate master circle radius 1.0 no rotation
        self.generate()
        self.resize_and_center()

    def generate(self):
        """generate master circle"""
        radius = 1.0
        # draw circle in x-z plane at y=0
        y = 0.0
        for angle in step_generator(0, 2 * math.pi, self.steps):
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius
            self.circle_raw_points.append(Vec3d(x, y, z))
        
    def resize_and_center(self):
        """recenter and resize master circle"""
        self.circle = []
        for point in self.circle_raw_points:
            self.circle.append(point * self.size + self.center)

    def set_color(self, color):
        """setter for self.color"""
        self.color = color

    def set_size(self, size=Vec3d(1, 1, 1)):
        """sets size and resizes circle"""
        self.size = size
        self.resize_and_center()

    def set_center(self, center=Vec3d(0, 0, 0)):
        """sets center and recenters circle"""
        self.center = center
        self.resize_and_center()

    def rotate(self, dx, dy, dz, offset2d=Vec2d(0,0), offset3d=Vec3d(0, 0, 0)):
        """rotates circle points and generates tranformed point array in 2d"""
        # rotate and project every point to 2d
        self.transformed_circle = []
        for point in self.circle:
            new_point = point.rotated_around_x(dx).rotated_around_y(dy).rotated_around_z(dz)
            transformed = new_point.project(surface.get_width(), surface.get_height(), self.viewer_distance, self.fov)
            self.transformed_circle.append((transformed.x + offset2d.x, transformed.y + offset2d.y))
                
    def update(self, center, viewer_distance, fov):
        """drawing"""
        self.viewer_distance = viewer_distance
        self.fov = fov
        pygame.draw.polygon(self.surface, self.color, self.transformed_circle, 1)



class Sphere(object):
    """Object represents a sphere"""

    def __init__(self, surface, color, center=Vec3d(0, 0, 0), size=Vec3d(1, 1, 1), steps=10.0, viewer_distance=256, fov=2):
        self.surface = surface
        self.color = color
        self.size = size
        self.center = center
        self.steps = steps
        self.viewer_distance = viewer_distance
        self.fov = fov
        # 20 circle
        self.sphere_raw_points = []
        self.generate()
        self.sphere_point = None
        self.sphere_transformed = None
        self.resize_and_center()

    def generate(self):
        radius = 0.0
        radius_angle = 0
        radius_step = float(math.pi / self.steps)
        for y in step_generator(-1, 1, self.steps):
            circle = []
            # c**2 = a**2 + b**2
            radius = math.sqrt(1 - y**2)
            # radius = math.sin(radius_angle)
            radius_angle += radius_step
            for angle in step_generator(0, 2 * math.pi, self.steps):
                x = math.cos(angle) * radius
                z = math.sin(angle) * radius
                circle.append(Vec3d(x, y, z))
            self.sphere_raw_points.append(circle)
        

    def resize_and_center(self):
        self.sphere_points = []
        for circle in self.sphere_raw_points:
            new_circle = []
            for point in circle:
                new_circle.append(point * self.size + self.center)
            self.sphere_points.append(new_circle)

    def set_color(self, color):
        self.color = color

    def set_size(self, size=Vec3d(1, 1, 1)):
        self.size = size
        self.resize_and_center()

    def set_center(self, center=Vec3d(0, 0, 0)):
        self.center = center
        self.resize_and_center()

    def rotate(self, dx, dy, dz, offset2d=Vec2d(0,0), offset3d=Vec3d(0, 0, 0)):
        # rotate and project every point to 2d
        self.transformed_sphere = []
        for circle in self.sphere_points:
            transformed_circle = []
            for point in circle:
                new_point = point.rotated_around_x(dx).rotated_around_y(dy).rotated_around_z(dz)
                transformed = new_point.project(surface.get_width(), surface.get_height(), self.viewer_distance, self.fov)
                transformed_circle.append((transformed.x + offset2d.x, transformed.y + offset2d.y))
            self.transformed_sphere.append(transformed_circle)
                
    def update(self, center, viewer_distance, fov):
        # draw every face of the cube
        self.viewer_distance = viewer_distance
        self.fov = fov
        for circle in self.transformed_sphere:
            pygame.draw.polygon(self.surface, self.color, circle, 1)
        for point_index in range(len(self.transformed_sphere[0])):
            points = []
            for circle_index in range(len(self.transformed_sphere)):
                points.append(self.transformed_sphere[circle_index][point_index])
            pygame.draw.polygon(self.surface, self.color, points, 1)


class ColorGradient(object):


    def __init__(self, rstep, gstep, bstep):
        self.rstep = float(rstep)
        self.gstep = float(gstep)
        self.bstep = float(bstep)
        self.red = 0.0
        self.green = 0.0
        self.blue = 0.0
        self.degree = float(math.pi / 360)

    def get_color(self):
        self.red += 256 * math.sin(self.degree * self.rstep)
        self.green += 256 * math.sin(self.degree * self.gstep)
        self.blue += 256 * math.sin(self.degree * self.bstep)
        color = (self.red % 256, self.green % 256, self.blue % 256)
        return(color) 


class BackgroundGradient(object):


    def __init__(self, surface):
        self.surface = surface
        self.cg = ColorGradient(0.3, 0.2, 0.1)
        self.colors = []
        for y in xrange(self.surface.get_height()):
            self.colors.append(self.cg.get_color())

    def update(self):
        for y in xrange(self.surface.get_height()):
            pygame.draw.line(self.surface, self.colors[y], (0, y), (self.surface.get_width(), y))


if __name__=='__main__':

    try:
        surface = pygame.display.set_mode((600,600))
        pygame.init()
        origin = (surface.get_width() / 2, surface.get_height() / 2)
        theta = 1
        step = math.pi / 180
        center_x = surface.get_width() / 2
        center_y = surface.get_height() / 2
        # Cube( surface, color, center3d, size)
        spheres = (
            # Fire(surface, (100,100), 400, 200, 4), 
            Sphere(surface, (100, 0, 0), Vec3d(-1.5, -1.5, -1.5), Vec3d(1, 1, 1)),
            #Sphere(surface, (100, 0, 0), Vec3d(0, 0, 0), Vec3d(1, 1, 1)),
            #Sphere(surface, (100, 0, 0), Vec3d(1.5, 1.5, 1.5), Vec3d(1, 1, 1)),
            Circle(surface, (100, 0, 0), Vec3d(1.5, -1.5, -1.5), Vec3d(1, 1, 1)),
            Tree(surface, (0, 100, 100), Vec2d(300, 500), 5, 50),
            Tree(surface, (0, 100, 100), Vec2d(330, 500), 5, 100),
            Starfield(surface, stars=100, depth=10),
            InfoRenderer(surface, pos=Vec2d(100,100)),
            ScrollText(surface, "Dolor Ipsum Dolor uswef", 400, pygame.Color(255,255,0)),
            SinusText(surface, "Dolor Ipsum Dolor uswef", 200, 30, 2, pygame.Color(0,255,255)),
            )
        clock = pygame.time.Clock()       
 
        size_angle = 0
        size_angle_step = math.pi / 720
        cg = ColorGradient(0.0, 0.05, 0.05)
        background_gradient = BackgroundGradient(surface)
        # for 3d projection
        fov = 2
        viewer_distance = 256
        pause = False
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
                #if keyinput[pygame.K_z]:
                #    theta[2] += math.pi / 180
                #if keyinput[pygame.KMOD_SHIFT | pygame.K_z]:
                #    theta[2] -= math.pi / 180
                #if keyinput[pygame.K_x]:
                #    theta[0] += math.pi / 180
                #if keyinput[pygame.KMOD_SHIFT | pygame.K_x]:
                #    theta[0] -= math.pi / 180
                #if keyinput[pygame.K_y]:
                #    theta[1] += math.pi / 180
                #if keyinput[pygame.KMOD_SHIFT | pygame.K_y]:
                #    theta[1] -= math.pi / 180
                if keyinput[pygame.K_UP]:
                    viewer_distance += 1
                if keyinput[pygame.K_DOWN]:
                    viewer_distance -= 1
                if keyinput[pygame.K_PLUS]:
                    fov += .1
                if keyinput[pygame.K_MINUS]:
                    fov -= .1
                if keyinput[pygame.K_p]:
                    pause = not pause
                if keyinput[pygame.K_r]:
                    viewer_distance = 256
                    fov = 2
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                #background_gradient.update()
                for thing in spheres:
                    if type(thing) == InfoRenderer:
                        thing.update(lines=("viewer_distance : %f" % viewer_distance, "fov: %f" % fov))
                        continue
                    elif type(thing) == Tree:
                        thing.update(center=Vec2d(0, 0))
                        continue
                    elif type(thing) in (Sphere, Circle, ):
                        # rotate
                        thing.rotate(dx=theta, dy=theta, dz=0.0, offset2d=Vec2d(0, 0), offset3d=Vec3d(1,1,1))
                        theta += step * 16
                        # color changing
                        color = cg.get_color()
                        thing.set_color(color=color)
                        # size wobbling
                        # size_angle += size_angle_step
                        # thing.set_size(0.5 + math.sin(size_angle) * 0.125)
                        # draw
                        thing.update(center=(0, 0), viewer_distance=viewer_distance, fov=fov)
                        continue
                    elif type(thing) in (SinusText, ScrollText, ):
                        thing.update()
                    elif type(thing) == Tree:
                        thing.update(center=Vec2d(0, 0), viewer_distance=viewer_distance, fov=fov)
                    else:
                        thing.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'
