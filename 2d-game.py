import pygame
import random

# Initialize pygame 
pygame.init()

# Game screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Side Scroller")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 
RED = (255, 0, 0)

# Game fonts
font = pygame.font.SysFont("Arial", 30)
font_small = pygame.font.SysFont("Arial", 20)   
 
# Game variables
scroll_thresh = 200
gravity = 1

# Player variables
current_level= 1 
player_lives = 3
player_health = 100
player_max_health = 100
projectile_damage = 25

# Enemy variables  
enemy_health = 100
enemy_damage = 25

# Levels
level_1 = [
"XXXXXXXXXXXX", 
"X          X",
"X          X",
"X          X",
"X    E     X",
"X     X    X",
"X     XXXXXX",
"X          X",
"XXXXXXXXXXXX"]

level_2 = [
"XXXXXXXXXXXXXX",
"X            X", 
"X            X",
"X            X",
"X      E     X",
"X            X",  
"X            X",
"X     XXXX   X",
"X            X",  
"XXXXXXXXXXXXXX"]

level_3 = [  
"XXXXXXXXXXXXXXXXX",
"X               X",
"X               X",
"X               X",  
"X               X",
"X               X",
"X          E    X", 
"X               X",
"X     XXXXXXXXX X",
"X               X",
"XXXXXXXXXXXXXXXXX"]

levels = [level_1, level_2, level_3]

# Load images
bg = pygame.image.load("bg.png")
player_img = pygame.image.load("player.png") 
projectile_img = pygame.image.load("projectile.png")
enemy_img = pygame.image.load("enemy.png")
health_pickup_img = pygame.image.load("health.png") 
ammo_pickup_img = pygame.image.load("ammo.png")

# Sprite classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.health = player_health
        self.max_health = player_max_health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.alive = True
        
    def update(self):
        dx = 0
        dy = 0
        walk_speed = 10
        jump_speed = 15
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.alive:
            self.vel_y = -jump_speed
            self.jump = True
        if key[pygame.K_LEFT]:
            dx -= walk_speed 
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += walk_speed
            self.direction = 1
            
    def apply_gravity(self):
        dx=0
        dy=0
        # Gravity
        self.vel_y += gravity        
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Prevent going off edges
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # Check collision with floor
        if self.rect.bottom + dy > SCREEN_HEIGHT - 110:
            dy = SCREEN_HEIGHT - 110 - self.rect.bottom
            self.jump = False
            
        # Update player position  
        self.rect.x += dx
        self.rect.y += dy
        
    def shoot(self):
        if self.alive:
            if self.direction == 1:
                return Projectile(self.rect.centerx + 25, self.rect.centery - 10, 10, projectile_damage)
            else:
                return Projectile(self.rect.centerx - 25, self.rect.centery - 10, -10, projectile_damage)
        else:
            return None
        
    def take_damage(self, amount):
        if self.alive:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.alive = False
                
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = projectile_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = vx
        self.damage = damage
        
    def update(self):
        self.rect.x += self.vx
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = -3 
        self.health = enemy_health
        
    def update(self):
        self.rect.x += self.vx
        if self.rect.right < 0:
            self.kill()
            
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            
class HealthPickup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = health_pickup_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        if pygame.sprite.collide_rect(self, player):
            if player.health < player.max_health:
                player.health += 25
                self.kill()

# Tile class
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft = pos)
        
# Level class
class Level():
    def __init__(self, level_data, surface):
        self.display_surface = surface
        
        # Level setup
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

        # Player
        self.player = pygame.sprite.GroupSingle()
        player_sprite = Player(100, 450)
        self.player.add(player_sprite)

        # Health 
        self.health_pickup = pygame.sprite.GroupSingle()
        health_pickup_sprite = HealthPickup(375, 300)
        self.health_pickup.add(health_pickup_sprite)

        # Enemies 
        self.enemies = pygame.sprite.Group()
        self.enemy_setup(level_data)
        
        # Collectibles
        self.collectibles = pygame.sprite.Group()
        self.collectible_setup(level_data)
        
    def setup_level(self, layout):
        # Tiles
        self.tiles = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * 64
                y = row_index * 64
                if cell == "X":
                    tile = Tile((x, y), 64, 64)
                    self.tiles.add(tile)

    def enemy_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * 64
                y = row_index * 64
                if cell == "E":
                    enemy = Enemy(x, y)
                    self.enemies.add(enemy)
                    
    def collectible_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * 64
                y = row_index * 64
                if cell == "C":
                    collectible = Collectible(x, y)
                    self.collectibles.add(collectible)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction

        if player_x < 300 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0    
        elif player_x > 500 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction < 0:
                    player.rect.left = sprite.rect.right
                    player.direction *= -1
                elif player.direction > 0:
                    player.rect.right = sprite.rect.left
                    player.direction *= -1

        for enemy in self.enemies:
            if enemy.rect.colliderect(player.rect):
                pygame.sprite.spritecollide(enemy, self.player, False)

        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction = 0
                elif player.direction < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction = 0 

    def run(self):
        
        # Run the entire level
        level_complete = False
        active_sprites = pygame.sprite.Group()
        active_sprites.add(self.player)
        
        while not level_complete:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    level_complete = True

            # Update sprites     
            active_sprites.update()            
            
            # Level scrolling
            self.scroll_x()

            # Collision detection
            self.horizontal_collision()
            self.vertical_collision()

            # Drawing
            self.tiles.draw(self.display_surface) 
            active_sprites.draw(self.display_surface)

            # Update display
            pygame.display.update()

        # Reset level after completion
        self.reset_level()
            
    def reset_level(self):
        # Reset level specific parameters
        pass
      
# Rest of game code
        
# Create sprite groups
projectile_group = pygame.sprite.Group() 
enemy_group = pygame.sprite.Group()
health_pickup_group = pygame.sprite.Group()

# Create level instances
level_1 = Level(level_1, screen)
level_2 = Level(level_2, screen)
level_3 = Level(level_3, screen)

# Game loop
run = True
while run:

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    # Draw background
    screen.blit(bg, (0, 0))
    
    # Run level
    if current_level == 1:
        level_1.run()
    elif current_level == 2:
        level_2.run() 
    else:
        level_3.run()

    # Update display
    pygame.display.update()
    
pygame.quit()
