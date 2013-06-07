import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

screen = (800,600)
pygame.init()
surface = pygame.display.set_mode(screen, pygame.OPENGL|pygame.DOUBLEBUF, 16)

def reshape((width,height)):
    # das OpenGL Fenster
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.0*width/height, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)

def init():
    # R, G, B, Alpha
    glClearColor(1.0, 1.0, 1.0, 1.0)
    reshape(screen)

def draw():
    # Bildschirm leeren, mit glClearColor
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    # Einheitsgrafik laden
    glLoadIdentity()
    # position camery x,y,z 
    # lookat 0,0,-100
    # wo ist oben: x, y, z, y nach oben
    gluLookAt(0, 0, 6, 0, 0, -100, 0, 1 ,0)

    # Begin
    glBegin(GL_QUADS)
    glColor(0, 0, 1.0)
    glVertex2f(-2, 2)  # oben links
    glVertex2f(2, 2)   # oben rechts
    glVertex2f(2, -1)  # unten rechts
    glVertex2f(-2, -1) # unten links
    glEnd() 

    # Pygame zeigt was an
    pygame.display.flip()

def get_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

def main():
    pygame.display.set_caption("Hallo Welt!")
    init()
    maxfps = 100
    clock = pygame.time.Clock()
    while True:
        clock.tick(maxfps)
        draw()
        get_event()
 
if __name__ == "__main__":
    main()
