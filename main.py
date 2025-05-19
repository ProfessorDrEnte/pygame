import sys
import pygame
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from shieldpowerup import ShieldPowerup




def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    lives = 3
    next_shield_timer = random.uniform(10, 20)

    font = pygame.font.SysFont(None, 36)

    

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Explosion.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    ShieldPowerup.containers = (updatable, drawable)

    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for obj in updatable:
            if isinstance(obj, ShieldPowerup):
                dist = (player.position - obj.position).length()
                if dist < PLAYER_RADIUS + 10:
                    obj.kill()
                    player.invulnerable = True
                    player.invulnerable_timer = 5.0


        for asteroid in asteroids:
            if not player.invulnerable and asteroid.collides_with(player):
                lives -= 1
                if lives <= 0:
                    print("Game Over!")
                    sys.exit()
                else:
                    player.respawn()



            for shot in shots:
                if asteroid.collides_with(shot):
                    score += 100
                    shot.kill()
                    asteroid.split()
                    Explosion(asteroid.position)

                    if random.random() < 0.2:
                        ShieldPowerup(asteroid.position.x, asteroid.position.y)

        background = pygame.image.load("heic1304c.jpg").convert()
        screen.blit(background, (0, 0))

        for obj in drawable:
            obj.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
