import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # === CODE GOES BELOW HERE ===
    screen.fill("blue")
    # === CODE GOES ABOVE HERE ===

    pygame.display.flip()
    clock.tick(60)

pygame.quit()