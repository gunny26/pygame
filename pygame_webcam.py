#!/usr/bin/python

# import the relevant libraries
import sys
import time
import pygame
import pygame.camera
from pygame.locals import *

# this is where one sets how long the script
# sleeps for, between frames.sleeptime__in_seconds = 0.05
# initialise the display window
screen = pygame.display.set_mode([800,420])
pygame.init()
pygame.display.set_gamma(0.5)
pygame.camera.init()
# set up a camera object
cam = pygame.camera.Camera("/dev/video1",(640,480), "RGB")
# start the camera
cam.start()
# hflip if front camera and self portait
hflip = True
vflip = False
brightness = 160
cam.set_controls(hflip=hflip, vflip=vflip, brightness=brightness)

track_color = None
crect = None

# transparent surface to draw on
whiteboard = pygame.Surface((640, 480), pygame.SRCALPHA, 32)
pygame.draw.rect(whiteboard, (255, 0, 0), (0, 0, 10, 10), 1)

while True:
    # fetch the camera image
    image = cam.get_image()
    image = pygame.transform.flip(image, hflip, vflip)
    # blank out the screen
    events = pygame.event.get()  
    for event in events:  
        if event.type == QUIT:  
            sys.exit(0)
    keyinput = pygame.key.get_pressed()
    # print keyinput
    if keyinput[K_t]:
        if track_color is None:
            print "Track Color registered" 
            track_color = pygame.transform.average_color(image, crect)
    if keyinput[K_h]:
        hflip = not hflip
        print "switching hflip to", hflip
        cam.set_controls(hflip, vflip, brightness)
    if keyinput[K_v]:
        vflip = not vflip
        print "switching vflip to", vflip
        cam.set_controls(hflip, vflip, brightness)
    if keyinput[K_b]:
        brightness += 1
        print "switching brightness to", brightness
        cam.set_controls(hflip, vflip, brightness)
    # sleep between every frame
    # time.sleep( sleeptime__in_seconds )
    screen.fill([0,0,0])
    if track_color is None:
        crect = pygame.draw.rect(image, (255,0,0), (320,240,10,10), 1)
        # get the average color of the area inside the rect
        ccolor = pygame.transform.average_color(image, crect)
        # fill the upper left corner with that color
        screen.fill(ccolor, (0,0,50,50))
    else:
        # threshold against the color we got before
        mask = pygame.mask.from_threshold(image, track_color, (20, 20, 20))
        # keep only the largest blob of that color
        connected = mask.connected_component()
        # make sure the blob is big enough that it isn't just noise
        if mask.count() > 100:
            # find the center of the blob
            coord = mask.centroid()
            # draw a circle with size variable on the size of the blob
            pygame.draw.circle(image, (0,255,0), coord, max(min(50, mask.count() / 400), 5))
            pygame.draw.circle(whiteboard, (0,0,0), coord, 2, 1)
        screen.fill(track_color, (0, 0, 50, 50))
    # copy the camera image to the screen
    screen.blit(image,(100, 0))
    # draw on whiteboard
    screen.blit(whiteboard, (100,0))
    # update the screen to show the latest screen image
    pygame.display.update()
