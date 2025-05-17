import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Rush - Boss & Power-Ups")

current_path = os.path.dirname(__file__)  # Nota: _file_ debe ser __file__
img_path = os.path.join(current_path, 'images')

# Carga imágenes (usa rectángulos si no hay)
try:
    player_img = pygame.image.load(os.path.join(img_path, 'Nave2.png')).convert_alpha()
    enemy_imgs = [
        pygame.image.load(os.path.join(img_path, 'alien_verde2.png')).convert_alpha(),
        pygame.image.load(os.path.join(img_path, 'alien_morado2.png')).convert_alpha()
    ]
    bullet_img = pygame.image.load(os.path.join(img_path, 'bullet2.png')).convert_alpha()
    background = pygame.image.load(os.path.join(img_path, 'fondo.png')).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    print("⚠ Error cargando imágenes. Usando figuras de prueba.")
    player_img = pygame.Surface((60, 60)); player_img.fill((0, 0, 255))
    enemy_img1 = pygame.Surface((40, 40)); enemy_img1.fill((0, 255, 0))
    enemy_img2 = pygame.Surface((40, 40)); enemy_img2.fill((255, 0, 255))
    bullet_img = pygame.Surface((10, 20)); bullet_img.fill((255, 255, 0))
    background = pygame.Surface((WIDTH, HEIGHT)); background.fill((0, 0, 0))
    enemy_imgs = [enemy_img1, enemy_img2]

# Power-up colores y tipos
POWERUP_COLORS = {
    "speed": (255, 255, 0),      # Amarillo
    "fast_shoot": (0, 255, 255), # Cyan
    "double_shot": (255, 0, 0)   # Rojo
}

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 8
        self.lives = 3
        self.score = 0
        # Power-up states
        self.base_speed = 8
        self.power_speed = 14
        self.power_fast_shoot = False
        self.power_double_shot = False
        self.shoot_delay = 350 # ms entre disparos normales
        self.shoot_timer = 0
        self.powerup_timers = {}

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(screen.get_rect())

        # Power-up: reset estados cuando terminan
        now = pygame.time.get_ticks()
        for ptype in list(self.powerup_timers):
            if now > self.powerup_timers[ptype]:
                self.remove_powerup(ptype)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer < self.shoot_delay:
            return []
        self.shoot_timer = now
        bullets = []
        # Disparo doble
        if self.power_double_shot:
            bullets.append(Bullet(self.rect.centerx - 15, self.rect.top))
            bullets.append(Bullet(self.rect.centerx + 15, self.rect.top))
        else:
            bullets.append(Bullet(self.rect.centerx, self.rect.top))
        return bullets

    def apply_powerup(self, ptype):
        now = pygame.time.get_ticks()
        duration = 7000 # ms
        if ptype == "speed":
            self.speed = self.power_speed
        elif ptype == "fast_shoot":
            self.shoot_delay = 150
            self.power_fast_shoot = True
        elif ptype == "double_shot":
            self.power_double_shot = True
        self.powerup_timers[ptype] = now + duration

    def remove_powerup(self, ptype):
        if ptype == "speed":
            self.speed = self.base_speed
        elif ptype == "fast_shoot":
            self.shoot_delay = 350
            self.power_fast_shoot = False
        elif ptype == "double_shot":
            self.power_double_shot = False
        self.powerup_timers.pop(ptype, None)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = enemy_imgs[type % 2]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1
            self.rect.y += 10

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 0)  # Usa el alien verde
        self.image = pygame.transform.scale(enemy_imgs[0], (120, 120))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.lives = 20
        self.last_powerup_time = pygame.time.get_ticks()

    def update(self):
        # Movimiento simple izquierda/derecha
        self.rect.x += 5 * self.direction
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1
            self.rect.y += 10

    def maybe_drop_powerup(self, powerup_group, all_sprites):
        now = pygame.time.get_ticks()
        if now - self.last_powerup_time > 2000: # cada 2 segundos
            ptype = random.choice(list(POWERUP_COLORS.keys()))
            powerup = PowerUp(self.rect.centerx, self.rect.bottom, ptype)
            powerup_group.add(powerup)
            all_sprites.add(powerup)
            self.last_powerup_time = now

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, ptype):
        super().__init__()
        self.ptype = ptype
        self.image = pygame.Surface((25, 25))
        self.image.fill(POWERUP_COLORS[ptype])
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

def create_enemies():
    for row in range(3):
        for col in range(8):
            enemy = Enemy(100 + col * 70, 50 + row * 60, row)
            enemies.add(enemy)
            all_sprites.add(enemy)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
create_enemies()

boss = None
boss_active = False

clock = pygame.time.Clock()
running = True
game_over = False
game_over_timer = None

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                new_bullets = player.shoot()
                for b in new_bullets:
                    bullets.add(b)
                    all_sprites.add(b)
            elif event.key == pygame.K_ESCAPE:
                running = False

    if not game_over:
        all_sprites.update()
        # Aparece el boss cuando hay suficiente puntaje y no está activo
        if player.score >= 1500 and not boss_active:
            # Quita todos los enemigos restantes
            for e in enemies:
                e.kill()
            boss = Boss(WIDTH//2, 50)
            all_sprites.add(boss)
            boss_active = True

        # Detección de colisiones normales
        if boss_active:
            # Disparos al boss
            hits = pygame.sprite.spritecollide(boss, bullets, True)
            for hit in hits:
                boss.lives -= 1
                if boss.lives <= 0:
                    boss.kill()
                    boss_active = False
                    # Gana el juego o reinicia enemigos (opcional)
            # Power-ups del boss
            boss.maybe_drop_powerup(powerups, all_sprites)
        else:
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            player.score += len(hits) * 100
            if len(enemies) == 0 and not boss_active:
                create_enemies()

        # Colisiones de jugador con enemigos o boss
        collided = pygame.sprite.spritecollide(player, enemies, True)
        if boss_active and pygame.sprite.collide_rect(player, boss):
            player.lives -= 1
        if collided:
            player.lives -= 1
            print(f"⚠ Colisión. Vidas restantes: {player.lives}")
        if player.lives <= 0 and not game_over:
            print("🔴 GAME OVER por colisión")
            game_over = True
            game_over_timer = pygame.time.get_ticks()

        # Power-ups
        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
        for pu in powerup_hits:
            player.apply_powerup(pu.ptype)

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    # Dibuja los rectángulos de colisión (debug visual)
    pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)
    for enemy in enemies:
        pygame.draw.rect(screen, (0, 0, 255), enemy.rect, 2)
    if boss_active and boss is not None:
        pygame.draw.rect(screen, (0, 255, 0), boss.rect, 2)

    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {player.score}  Lives: {player.lives}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    if boss_active and boss is not None:
        boss_text = font.render(f"BOSS HP: {boss.lives}", True, (255, 255, 0))
        screen.blit(boss_text, (WIDTH//2 - 70, 10))

    if game_over:
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        if pygame.time.get_ticks() - game_over_timer > 3000:
            running = False

    pygame.display.flip()

pygame.quit()
