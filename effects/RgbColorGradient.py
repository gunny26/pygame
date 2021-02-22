#!/usr/bin/python3
import sys
import math
# non std modules
import pygame


def get_rgb_color_gradient(start_rgb:tuple, target_rgb:tuple, steps:int) -> list:
    """
    calculating color gradient in RGB space from start to end color

    params:
    start_rgb: <tuple> (r, b, b) of starting color
    target_rgb: <tuple> (r, b, b) of target color
    steps: <int> how many substeps

    returns:
    <list> of <tuple> (r, g, b)
    """
    step_r = (target_rgb[0] - start_rgb[0]) / steps
    step_g = (target_rgb[1] - start_rgb[1]) / steps
    step_b = (target_rgb[2] - start_rgb[2]) / steps
    ret_data = []
    for i in range(steps):
        ret_data.append(
            (
                int(start_rgb[0] + i * step_r),
                int(start_rgb[1] + i * step_g),
                int(start_rgb[2] + i * step_b)
            )
        )
    return ret_data


def test():
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        clock = pygame.time.Clock()
        gradient = get_rgb_color_gradient((255, 0, 0), (123, 231, 131), 256)
        gradient += gradient[::-1]
        pause = False
        index = 0
        while True:
            clock.tick(fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
            if pause is not True:
                surface.fill(gradient[index % len(gradient)])
                pygame.display.flip()
            index += 1
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    test()

