import pygame
from constants import *

class SpeedPowerup(pygame.sprite.Sprite):
    containers = ()

    def __init__(self, x, y):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)

        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image,
            (255, 255, 0),
            [(12, 2), (20, 12), (14, 12), (22, 22), (10, 14), (10, 18), (2, 10)]
        )
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.rect.center = self.position

    def draw(self, screen):
        pulse = (pygame.time.get_ticks() % 1000) / 1000
        alpha = int(80 + 80 * abs(0.5 - pulse) * 2)

        glow = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 255, 0, alpha), (25, 25), 22)
        screen.blit(glow, self.position - pygame.Vector2(25, 25))
        screen.blit(self.image, self.rect)
