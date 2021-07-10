import pygame


class Wall:

    def __init__(self, x, y, width, height, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)

    def get_rect(self):
        return self.rect

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
