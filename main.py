import pygame
import os
import random
import math

# === GLOBAL VARIABLES ===
screen_height = 720
screen_width = 1280
running = True

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Vampire Dyres")
clock = pygame.time.Clock()

# Load the background image
background_img = pygame.image.load('background.png')
bg_rect = background_img.get_rect()
background_pos = [0, 0]   # Initial position of the background
tile_size = (bg_rect.width, bg_rect.height)

protagonist = pygame.image.load(os.path.join('placeholder_character.png')) #loads the protagonist image
def draw_player(player):
    screen.blit(protagonist, (player.x,player.y)) #draws the player onto the screen using the rectangle's coordinates
player = pygame.Rect(640-64, 360-64, 128, 128) #creates a rectangle for the player to check collision
player_speed = 5
player_health = 100

class Enemy: #enemy class code
    def __init__(self, sprite, health, speed, damage): # initialtion 
        self.health = health 
        self.speed = speed
        self.damage = damage
        self.sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(self.sprite, (128, 128))
        number = random.randint(1,4)
        if number == 1: #generates in anywhere on the left side
            self.rectangle = pygame.Rect(0, random.randint(0,720), 128, 128)
        if number == 2: #generates in anywhere on the right side
            self.rectangle = pygame.Rect(1280, random.randint(0,720), 128, 128)
        if number == 3: #generates in anywhere on the top side
            self.rectangle = pygame.Rect(random.randint(0,1280), 0, 128, 128)
        if number == 4: #generates in anywhere on the bottom side
            self.rectangle = pygame.Rect(random.randint(0,1280), 720, 128, 128)
    def move_to_player(self, player_x, player_y): # moves the player
        screen.blit(self.sprite, (self.rectangle.x, self.rectangle.y))
        try:
            angle = (math.atan(abs(player_y-self.rectangle.y)/abs(player_x-self.rectangle.x))) #finds the angle between the player and the enemy
            print(angle)
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
            print("hit")
            print(player_health)

placeholder_enemy = Enemy('placeholder_character.png', 1, 1, 1)
    

while running:
    screen.fill("blue")
    # Event handling for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x - player_speed > 0:  #associates the keypressed to the movement of the player and checks if it will go off screen
        player.x -= player_speed  
        print("pressed a")
    if keys[pygame.K_d] and player.x + player_speed + 128 < 1280:  #replace the 128s with the dimentions of the character
        player.x += player_speed  
        print("pressed d")
    if keys[pygame.K_w] and player.y - player_speed > 0:  # (0,0) is the top corner so to move up yo need to subtract
        player.y -= player_speed  
        print("pressed w")
    if keys[pygame.K_s] and player.y + player_speed + 128 < 720:  
        player.y += player_speed  
        print("pressed s")

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
    placeholder_enemy.move_to_player(player.x, player.y)
    placeholder_enemy.player_colision(player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
