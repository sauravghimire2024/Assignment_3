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

