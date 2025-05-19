import pygame
import random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    containers = ()

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(random.uniform(-100, 100), random.uniform(-100, 100))
        self.num_points = random.randint(8, 14)
        self.jitter = self.radius * 0.4
        self.shape = self.generate_shape()

    def generate_shape(self):
        points = []
        for i in range(self.num_points):
            angle = i * (360 / self.num_points)
            distance = self.radius + random.uniform(-self.jitter, self.jitter)
            direction = pygame.Vector2(0, -1).rotate(angle) * distance
            points.append(direction)
        return points

    def draw(self, screen):
        points = [self.position + p for p in self.shape]
        pygame.draw.polygon(screen, (200, 200, 200), points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_around()

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Random split angle
        angle_offset = random.uniform(20, 50)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        a = Asteroid(self.position.x, self.position.y, new_radius)
        a.velocity = self.velocity.rotate(angle_offset) * 1.2

        b = Asteroid(self.position.x, self.position.y, new_radius)
        b.velocity = self.velocity.rotate(-angle_offset) * 1.2
        
    def wrap_around(self):
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
