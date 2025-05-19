import pygame
from constants import *

class ShieldPowerup(pygame.sprite.Sprite):
    containers = ()

    def __init__(self, x, y):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)

        # Bild laden (Pfad anpassen, falls nötig)
        self.image = pygame.image.load("shield.png").convert_alpha()

        # Skalieren, wenn zu groß
        self.image = pygame.transform.smoothscale(self.image, (32, 32))

        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.rect.center = self.position

    def draw(self, screen):
        # Glow-Effekt im Hintergrund
        pulse = (pygame.time.get_ticks() % 1000) / 1000
        alpha = int(100 + 80 * abs(0.5 - pulse) * 2)

        glow_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (0, 150, 255, alpha), (30, 30), 25)
        screen.blit(glow_surface, self.position - pygame.Vector2(30, 30))

        # Schild-Icon oben drüber
        screen.blit(self.image, self.rect)
