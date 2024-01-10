import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Load the background image
background_img = pygame.image.load('background.png')
bg_rect = background_img.get_rect()
background_pos = [0, 0]   # Initial position of the background

# Tile size should match the background image size
tile_size = (bg_rect.width, bg_rect.height)

while running:
    screen.fill("blue")

    # Event handling for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        background_pos[0] += 5
    if keys[pygame.K_RIGHT]:
        background_pos[0] -= 5
    if keys[pygame.K_UP]:
        background_pos[1] += 5
    if keys[pygame.K_DOWN]:
        background_pos[1] -= 5

    # Ensure that the background tiles in all directions by using modulo
    background_pos[0] %= bg_rect.width
    background_pos[1] %= bg_rect.height

    # Draw the tiled background
    for x in range(-bg_rect.width, screen.get_width(), tile_size[0]):
        for y in range(-bg_rect.height, screen.get_height(), tile_size[1]):
            screen.blit(background_img, (x + background_pos[0], y + background_pos[1]))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()