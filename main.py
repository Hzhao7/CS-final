import pygame
import os
import random
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Vampire Dyres")
clock = pygame.time.Clock()
running = True

# Load the background image
background_img = pygame.image.load('background.png')
bg_rect = background_img.get_rect()
background_pos = [0, 0]   # Initial position of the background

# Tile size should match the background image size
tile_size = (bg_rect.width, bg_rect.height)

protagonist = pygame.image.load(os.path.join('placeholder_character.png')) #loads the protagonist image
def draw_player(player):
    screen.blit(protagonist, (player.x,player.y)) #draws the player onto the screen using the rectangle's coordinates
player = pygame.Rect(640-64, 360-64, 128, 128) #creates a rectangle for the player to check collision

class Enemy:
    def __init__(self, sprite, health, speed, damage):
        self.health = health 
        self.speed = speed
        self.damage = damage
        self.sprite = pygame.image.load(sprite)
        #self.sprite = pygame.transform.scale(image, (128, 128))
        number = random.randint(1,4)
        if number == 1: #generates in anywhere on the left side
            self.rectangle = pygame.Rect(0, random.randint(0,720), 128, 128)
        if number == 2: #generates in anywhere on the right side
            self.rectangle = pygame.Rect(1280, random.randint(0,720), 128, 128)
        if number == 3: #generates in anywhere on the top side
            self.rectangle = pygame.Rect(random.randint(0,1280), 0, 128, 128)
        if number == 4: #generates in anywhere on the bottom side
            self.rectangle = pygame.Rect(random.randint(0,1280), 720, 128, 128)
    def move_to_player(self, player_x, player_y):
        screen.blit(self.sprite, (self.rectangle.x, self.rectangle.y))

        angle = (math.atan(abs(player_y-self.rectangle.y)/abs(player_x-self.rectangle.x))) #finds the angle between the player and the enemy
        if self.rectangle.x < player_x: # depending on where the enemy is it will adjust to the player
            self.rectangle.x += self.speed*math.cos(angle)
        if self.rectangle.x > player_x:
            self.rectangle.x -= self.speed*math.cos(angle)
        if self.rectangle.y < player_y:
            self.rectangle.y += self.speed*math.sin(angle)
        if self.rectangle.y > player_y:
            self.rectangle.y -= self.speed*math.sin(angle)

placeholder_enemy = Enemy('placeholder_character.png', 1, 1, 1)
    

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
    draw_player(player)
    placeholder_enemy.move_to_player(640-64, 360-64)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
