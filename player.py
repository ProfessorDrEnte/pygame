import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 300
        self.friction = 0.98

        self.rotation = 0
        self.shoot_timer = 0
        self.invulnerable = False
        self.invulnerable_timer = 0

        self.speed_boost = False
        self.speed_boost_timer = 0
        self.default_acceleration = 300
        self.acceleration = self.default_acceleration



    def draw(self, screen):
        if self.invulnerable and int(pygame.time.get_ticks() * 0.005) % 2 == 0:
            return  
        pygame.draw.polygon(screen, "white", self.triangle(), 2)


    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def update(self, dt):
        # Update cooldowns & Timers
        self.shoot_timer -= dt
        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        if self.speed_boost:
            self.speed_boost_timer -= dt
            self.acceleration = self.default_acceleration * 2  # doppelte Beschleunigung
            if self.speed_boost_timer <= 0:
                self.speed_boost = False
                self.acceleration = self.default_acceleration

        keys = pygame.key.get_pressed()

        # Movement Input
        if keys[pygame.K_w]:
            self.move(dt, 1)
        if keys[pygame.K_s]:
            self.move(dt, -1)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        # Shooting
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Apply velocity & friction
        self.position += self.velocity * dt
        self.velocity *= self.friction

        # Wrap around screen
        self.wrap_around()


    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED


    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt, direction=1):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * self.acceleration * dt * direction


    def wrap_around(self):
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH

        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT


    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.rotation = 0
        self.shoot_timer = 0
        self.invulnerable = True
        self.invulnerable_timer = 2.0
