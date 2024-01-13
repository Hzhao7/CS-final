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

# Player code
image = pygame.image.load(os.path.join('placeholder_character.png')) #loads the protagonist image
protagonist = pygame.transform.scale(image, (64, 64))
def draw_player(player):
    screen.blit(protagonist, (player.x,player.y)) #draws the player onto the screen using the rectangle's coordinates
player = pygame.Rect(640-64, 360-64, 64, 64) #creates a rectangle for the player to check collision
player_speed = 5
total_health = 100

# Used for health bar
player_health = total_health

#Clock code
secs = 0
mins = 0

clock_font = pygame.font.Font('freesansbold.ttf', 32)
clock_text = clock_font.render("{}:{}".format(mins,secs), True, (255,255,255), (0,0,0))
text_rect = pygame.Rect(width/2, 50, 1,1)

class Enemy:
    def __init__(self, sprite, health, speed, damage):
        self.health = health
        self.speed = speed
        self.damage = damage
        self.sprite = pygame.transform.scale(pygame.image.load(sprite), (64, 64)) # Combined two operations into one
        self.stored_speed = speed # renamed stored variable to stored_speed to be more descriptive.

        position_options = [ #Array of position options. Reduces repetitive code and allows for easy additions
            pygame.Rect(0, random.randint(0,720), 64, 64), # Left
            pygame.Rect(1280, random.randint(0,720), 64, 64), # Right
            pygame.Rect(random.randint(0,1280), 0, 64, 64), # Top 
            pygame.Rect(random.randint(0,1280), 720, 64, 64), # Bottom
        ]

        self.rectangle = random.choice(position_options)

    def _get_angle(self, player_x, player_y): # refactor the calculations of getting an angle into a function for more readability
        try:
            return math.atan(abs(player_y-self.rectangle.y)/abs(player_x-self.rectangle.x))
        except ZeroDivisionError:
            return math.pi* 3/2 if self.rectangle.y < player_y else math.pi* 1/2

    def move_to_player(self, player_x, player_y):
    
        screen.blit(self.sprite, (self.rectangle.x, self.rectangle.y))

        angle = self._get_angle(player_x, player_y) # use the newly created function

        # Calculate movement separately
        x_movement = self.speed*math.cos(angle)
        y_movement = self.speed*math.sin(angle)

        # Update x and y position based on player's position
        self.rectangle.x += x_movement if self.rectangle.x < player_x else -x_movement
        self.rectangle.y += y_movement if self.rectangle.y < player_y else -y_movement

    def player_collision(self, player_rect): # corrected spelling of function name
        if self.rectangle.colliderect(player_rect):
            global player_health # consider passing player_health as a parameter rather than using global variable,
            player_health -= self.damage
            print(player_health)
            self.speed = 0
        else:
            self.speed = self.stored_speed # used the renamed variable
        
placeholder_enemy = Enemy('placeholder_character.png', 0.5, 4, 1)
while running:
    # Show floor
    screen.blit(floor_img, (0, 0))
    # shows clock
    clock.tick(60)
    secs += 1/60
    screen.blit(clock_text, text_rect)
    if int(secs) == 60:
        secs = 0
        mins += 1
    clock_text = clock_font.render("{}:{}".format(int(mins),int(secs)), True, (0,0,0), (255,255,255))

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
    placeholder_enemy.player_collision(player)
    pygame.display.flip()
    

pygame.quit()
