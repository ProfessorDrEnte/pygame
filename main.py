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
from speedpowerup import SpeedPowerup

def show_start_screen(screen):
    font_big = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 32)

    title = font_big.render("ASTEROIDS", True, (255, 255, 255))
    controls = [
        "W / A / S / D: Bewegung / Rotation",
        "SPACE: Schießen",
        "1 / 2: Waffen wechseln",
        "B: Bombe zünden",
        "",
        "Drücke eine beliebige Taste zum Start"
    ]

    screen.fill((0, 0, 0))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    for i, line in enumerate(controls):
        text = font_small.render(line, True, (200, 200, 200))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 40))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # Spielstatus
    score = 0
    lives = 3
    bombs_available = 3
    bomb_cooldown = 0

    # Powerup Timer
    next_shield_timer = random.uniform(10, 20)
    next_speed_timer = random.uniform(12, 22)

    # Sprite Gruppen
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Container-Zuweisungen
    Explosion.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    ShieldPowerup.containers = (updatable, drawable)
    SpeedPowerup.containers = (updatable, drawable)
    Player.containers = (updatable, drawable)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        # Event-Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Eingabe lesen
        keys = pygame.key.get_pressed()

        # 💣 Bombenlogik
        if keys[pygame.K_b] and bomb_cooldown <= 0 and bombs_available > 0:
            bombs_available -= 1
            bomb_cooldown = 1  # Sekunden Cooldown
            for asteroid in asteroids.copy():
                if (asteroid.position - player.position).length() < 200:
                    asteroid.kill()
                    asteroid.split()
                    Explosion(asteroid.position)
                    score += 100

        # Update aller Objekte
        updatable.update(dt)

        # ⏱️ Powerups automatisch spawnen
        next_shield_timer -= dt
        if next_shield_timer <= 0:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            ShieldPowerup(x, y)
            next_shield_timer = random.uniform(10, 20)

        next_speed_timer -= dt
        if next_speed_timer <= 0:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            SpeedPowerup(x, y)
            next_speed_timer = random.uniform(12, 22)

        # ⚡ Powerups aufsammeln
        for obj in updatable:
            if isinstance(obj, ShieldPowerup):
                if (player.position - obj.position).length() < PLAYER_RADIUS + 10:
                    obj.kill()
                    player.invulnerable = True
                    player.invulnerable_timer = 5.0

            if isinstance(obj, SpeedPowerup):
                if (player.position - obj.position).length() < PLAYER_RADIUS + 10:
                    obj.kill()
                    player.speed_boost = True
                    player.speed_boost_timer = 5.0

        # 🪨 Asteroiden-Kollisionen
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

                    # Chance auf Shield Powerup beim Zerstören
                    if random.random() < 0.2:
                        ShieldPowerup(asteroid.position.x, asteroid.position.y)

        # 🎨 Zeichnen
        background = pygame.image.load("heic1304c.jpg").convert()
        screen.blit(background, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        # HUD
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Lives: {lives}", True, (255, 255, 255)), (10, 40))
        screen.blit(font.render(f"Bombs: {bombs_available}", True, (255, 255, 255)), (10, 70))
        weapon_text = font.render(f"Weapon: {player.weapon_type}", True, (255, 255, 255))
        screen.blit(weapon_text, (10, 100))


        pygame.display.flip()

        # ⏲️ Zeit und Cooldown aktualisieren
        dt = clock.tick(60) / 1000
        bomb_cooldown -= dt




if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    show_start_screen(screen)
    main()

