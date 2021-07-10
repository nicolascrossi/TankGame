import pygame
from line import Line

class Shell:

    def __init__(self, x, y, x_vel, y_vel, friendly, screen):
        self.friendly = friendly
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel

        self.screen = screen
        self.rect = pygame.Rect(self.x, self.y, 2, 2)

    def get_pos(self):
        return (self.x, self.y)

    def get_vels(self):
        return (self.x_vel, self.y_vel)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def render(self):
        self.rect = pygame.draw.rect(self.screen, (255, 255, 255), [self.x, self.y, 2, 2])

    def check_hit(self, tanks):
        for tank in tanks:
            if not tank is self.friendly:
                if tank.get_rect().colliderect(self.rect):
                    return tank
        return None

    def get_rect(self):
        return self.rect

    def get_line(self):
        return Line(self.x, self.y, self.x_vel, self.y_vel)