        # Prevent going off edges
ifself.rect.left + dx < 0:
dx = -self.rect.left
ifself.rect.right + dx > SCREEN_WIDTH:
dx = SCREEN_WIDTH - self.rect.right

        # Check collision with floor
ifself.rect.bottom + dy> SCREEN_HEIGHT - 110:
dy = SCREEN_HEIGHT - 110 - self.rect.bottom
self.jump = False

        # Update player position  
self.rect.x += dx
self.rect.y += dy

def shoot(self):
ifself.alive:
ifself.direction == 1:
return Projectile(self.rect.centerx + 25, self.rect.centery - 10, 10, projectile_damage)
else:
return Projectile(self.rect.centerx - 25, self.rect.centery - 10, -10, projectile_damage)
else:
return None

deftake_damage(self, amount):
ifself.alive:
self.health -= amount
ifself.health<= 0:
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
ifself.rect.right< 0 or self.rect.left> SCREEN_WIDTH:
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
ifself.rect.right< 0:
self.kill()

deftake_damage(self, amount):
self.health -= amount
ifself.health<= 0:
self.kill()

classHealthPickup(pygame.sprite.Sprite):
def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
self.image = health_pickup_img
self.rect = self.image.get_rect()
self.rect.center = (x, y)

def update(self):
ifpygame.sprite.collide_rect(self, player):
ifplayer.health<player.max_health:
player.health += 25
self.kill()

