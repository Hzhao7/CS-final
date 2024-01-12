# Author: Henry Zhao, Benjamin Lu
# Date: 22nd January 2024
# Course: ICS3U0-B
# Description: ADD WHEN DONE ADD WHEN DONE ADD WHEN DONE

import pygame
import os
import random
import math

pygame.init()

# Global variables
clock = pygame.time.Clock()
running = True

# Set window title
pygame.display.set_caption("Vampire Dyers")

# Set screen size
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

# Load the floor image
floor_img = pygame.image.load('floor.png')
bg_rect = floor_img.get_rect()
floor_pos = [0, 0]   # Initial position of the floor

# Tile size should match the floor image size
tile_size = (bg_rect.width, bg_rect.height)

image = pygame.image.load(os.path.join('placeholder_character.png')) #loads the protagonist image
protagonist = pygame.transform.scale(image, (64, 64))
def draw_player(player):
    screen.blit(protagonist, (player.x,player.y)) #draws the player onto the screen using the rectangle's coordinates
player = pygame.Rect(640-64, 360-64, 64, 64) #creates a rectangle for the player to check collision
player_speed = 5
total_health = 100

# Used for health bar
player_health = total_health

class Enemy: #enemy class code
    def __init__(self, sprite, health, speed, damage): # initialtion 
        self.health = health 
        self.speed = speed
        self.damage = damage
        self.sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(self.sprite, (64, 64))
        self.stored = self.speed # used to store the speed that was lost after colission
        number = random.randint(1,4)
        if number == 1: #generates in anywhere on the left side
            self.rectangle = pygame.Rect(0, random.randint(0,720), 64, 64)
        if number == 2: #generates in anywhere on the right side
            self.rectangle = pygame.Rect(1280, random.randint(0,720), 64, 64)
        if number == 3: #generates in anywhere on the top side
            self.rectangle = pygame.Rect(random.randint(0,1280), 0, 64, 64)
        if number == 4: #generates in anywhere on the bottom side
            self.rectangle = pygame.Rect(random.randint(0,1280), 720, 64, 64)
    def move_to_player(self, player_x, player_y): # moves the player
        screen.blit(self.sprite, (self.rectangle.x, self.rectangle.y))
        try:
            angle = (math.atan(abs(player_y-self.rectangle.y)/abs(player_x-self.rectangle.x))) #finds the angle between the player and the enemy
        except:
            if self.rectangle.y < player_y:
                angle = math.pi*3/2
            if self.rectangle.y > player_y:
                angle = math.pi*1/2
        if self.rectangle.x < player_x: # depending on where the enemy is it will adjust to the player
            self.rectangle.x += self.speed*math.cos(angle)
        if self.rectangle.x > player_x:
            self.rectangle.x -= self.speed*math.cos(angle)
        if self.rectangle.y < player_y:
            self.rectangle.y += self.speed*math.sin(angle)
        if self.rectangle.y > player_y:
            self.rectangle.y -= self.speed*math.sin(angle)
    def player_colision(self, player_rect):
        global player_health
        if self.rectangle.colliderect(player_rect):
            player_health -= self.damage
            print(player_health)
            self.speed = 0
        else:
            self.speed = self.stored
        

placeholder_enemy = Enemy('placeholder_character.png', 0.5, 6, 1)
    

while running:
    screen.fill("blue")
    # Event handling for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x - player_speed > 0:  #associates the keypressed to the movement of the player and checks if it will go off screen
        player.x -= player_speed  
    if keys[pygame.K_d] and player.x + player_speed + 128 < width:  #replace the 128s with the dimentions of the character
        player.x += player_speed  
    if keys[pygame.K_w] and player.y - player_speed > 0:  # (0,0) is the top corner so to move up yo need to subtract
        player.y -= player_speed  
    if keys[pygame.K_s] and player.y + player_speed + 128 < height:  
        player.y += player_speed  

    # Ensure that the floor tiles in all directions by using modulo
    floor_pos[0] %= bg_rect.width
    floor_pos[1] %= bg_rect.height

    # Draw the tiled floor
    for x in range(-bg_rect.width, screen.get_width(), tile_size[0]):
        for y in range(-bg_rect.height, screen.get_height(), tile_size[1]):
            screen.blit(floor_img, (x + floor_pos[0], y + floor_pos[1]))

    # draws the health bar
    ratio = player_health/total_health
    pygame.draw.rect(screen, "red", (player.x-150+32, player.y+75, 300, 40))
    if ratio >=0 :
        pygame.draw.rect(screen, "green", (player.x-150+32, player.y+75, 300*ratio, 40))
    else:
        running = False
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_player(player)
    placeholder_enemy.move_to_player(player.x, player.y)
    placeholder_enemy.player_colision(player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
