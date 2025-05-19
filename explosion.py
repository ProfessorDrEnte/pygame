import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(self.containers)
        self.particles = []
        self.position = pygame.Vector2(position)
        self.timer = 0.5  # Lebensdauer

        # Erzeuge Partikel mit zufälliger Richtung und Geschwindigkeit
        for _ in range(20):
            velocity = pygame.Vector2(random.uniform(-100, 100), random.uniform(-100, 100))
            self.particles.append({
                "pos": self.position.copy(),
                "vel": velocity,
                "radius": random.randint(2, 4)
            })

    def update(self, dt):
        self.timer -= dt
        for p in self.particles:
            p["pos"] += p["vel"] * dt
            p["radius"] *= 0.95  # Schrumpfen

        if self.timer <= 0:
            self.kill()

    def draw(self, screen):
        for p in self.particles:
            if p["radius"] > 0.5:
                pygame.draw.circle(screen, (255, 100, 0), p["pos"], int(p["radius"]))
