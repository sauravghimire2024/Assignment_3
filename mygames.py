import pygame

# Initialize Pygame
pygame.init()

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Player rectangle
player = pygame.Rect(300, 250, 50, 50)

# Game loop
run = True
while run:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), player)

    # Get key presses
    keys = pygame.key.get_pressed()

    # Check keys and move player accordingly
    if keys[pygame.K_a]:
        player.move_ip(-1, 0)
    elif keys[pygame.K_d]:
        player.move_ip(1, 0)
    elif keys[pygame.K_w]:
        player.move_ip(0, -1)
    elif keys[pygame.K_s]:
        player.move_ip(0, 1)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

# Quit pygame
pygame.quit()
