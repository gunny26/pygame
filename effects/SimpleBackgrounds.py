#!/usr/bin/python3
import sys
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


class GradientBackground():

    def __init__(self, dim, start_rgb, target_rgb):
        """
        Color Gradient background from start to target
        """
        self.surface = pygame.Surface(dim)
        gradient = get_rgb_color_gradient(start_rgb, target_rgb, dim[1])
        for y in range(dim[1]):
            pygame.draw.line(self.surface, gradient[y], (0, y), (dim[0], y))

    def update(self):
        return self.surface


class GradientBackground2():

    def __init__(self, dim, start_rgb, target_rgb):
        """
        Color Gradient background from start to target and back to start
        """
        self.surface = pygame.Surface(dim)
        gradient = get_rgb_color_gradient(start_rgb, target_rgb, dim[1] // 2)
        gradient += gradient[::-1]
        for y in range(dim[1]):
            pygame.draw.line(self.surface, gradient[y], (0, y), (dim[0], y))

    def update(self):
        return self.surface


def main():
    try:
        fps = 1
        width = 600
        height = 400
        start_rgb = (0, 100, 200)
        target_rgb = (200, 100, 0)
        surface = pygame.display.set_mode((width, height))
        pygame.init()
        clock = pygame.time.Clock()
        bg_surface = GradientBackground((width, height), start_rgb, target_rgb)
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                surface.blit(bg_surface.update(), (0, 0))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    main()

