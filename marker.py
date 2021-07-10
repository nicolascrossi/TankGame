import pygame

class Marker:
    def __init__(self, x, y, color, screen):
        self.color = color
        self.x = x
        self.y = y
        self.width = 5
        self.height = 5
        self.screen = screen
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)