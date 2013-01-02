#!/usr/bin/python

# import the relevant libraries
import sys
import time
import math
from PIL import Image
from PIL import ImageChops
import pygame
import pygame.camera
from pygame.locals import *

SCREEN = (640,480)
# Threshhold for difference between base_image and current image
THRESHHOLD = 28
# sound to play if motion detected
ALARM = 'baby_talk.mp3'
# camera device
CAMERA = "/dev/video1"

def pygame_to_pil_img(pg_surface):
    """convert pygame surface to PIL Image"""
    imgstr = pygame.image.tostring(pg_surface, 'RGB')
    return Image.fromstring('RGB', pg_surface.get_size(), imgstr)

def pil_to_pygame_img(pil_img):
    """convert PIL Image to pygame surface"""
    imgstr = pil_img.tostring()
    return pygame.image.fromstring(imgstr, pil_img.size, 'RGB')

def rmsdiff(img1, img2):
    "Calculate the root-mean-square difference between two images"
    hist = ImageChops.difference(img1, img2).histogram()
    seq = [h*(i**2) for h, i in zip(hist, range(256))]
    total = sum(seq)
    return math.sqrt(total / (float(img1.size[0]) * img1.size[1]))

# this is where one sets how long the script
# sleeps for, between frames.sleeptime__in_seconds = 0.05
# initialise the display window
screen = pygame.display.set_mode(SCREEN)
pygame.init()
# webcam
pygame.camera.init()
# audio mixer
pygame.mixer.init()
pygame.mixer.music.load(ALARM)

# set up a camera object
cam = pygame.camera.Camera(CAMERA, SCREEN, "RGB")
# start the camera
cam.start()
# hflip if front camera and self portait
hflip = True
vflip = False
brightness = 160
# only brightness works
cam.set_controls(hflip=hflip, vflip=vflip, brightness=brightness)

# base image
base_image = None
# flag to signal if motion was detected
in_motion = False

while True:
    # fetch the camera image
    image = cam.get_image()
    # lip horizontal, if self shot camera
    image = pygame.transform.flip(image, hflip, vflip)
    # convert to PIL Image for difference processing
    p_image = pygame_to_pil_img(image)
    # blank out the screen
    events = pygame.event.get()  
    for event in events:  
        if event.type == QUIT:  
            sys.exit(0)
    keyinput = pygame.key.get_pressed()
    # print keyinput
    if keyinput[K_t]:
        if base_image is None:
            print "Taking Base Image"
            base_image = p_image
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
    if base_image is not None:
        # find difference between this image and base_image
        diff = rmsdiff(base_image, p_image)
        if diff > THRESHHOLD:
            print "Motion detected", diff
            # play sound only when first detected
            if in_motion is False:
                pygame.mixer.music.play()
            in_motion = True
        else:
            # print "No Motion detected"
            in_motion = False
    # copy the camera image to the screen
    screen.blit(image, (0, 0))
    # update the screen to show the latest screen image
    pygame.display.update()
