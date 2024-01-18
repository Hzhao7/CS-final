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
image = pygame.image.load(os.path.join('player_left.png')) #loads the protagonist image

def draw_player(player):
    screen.blit(protagonist, (player.x,player.y)) #draws the player onto the screen using the rectangle's coordinates
player = pygame.Rect(640-64, 360-64, 64, 64) #creates a rectangle for the player to check collision
player_speed = 2.5
total_health = 100

# Used for health bar
player_health = total_health

# Used to store player orientation
left = True 

#Clock code
secs = 0
mins = 0

font = pygame.font.Font('freesansbold.ttf', 32)
clock_text = font.render("{}:{}".format(mins,secs), True, (255,255,255), (0,0,0))
text_rect = pygame.Rect(width/2, 50, 1,1)

bullet_damage = 5

class Enemy:
    def __init__(self, sprite, sprite_width, sprite_height, health, speed, damage):
        self.health = health
        self.speed = speed
        self.damage = damage
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sprite = pygame.transform.scale(pygame.image.load(sprite), (self.sprite_width, self.sprite_height)) # Combined two operations into one
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
            return math.pi* 3/2 if self.rectangle.y < player_y else math.pi* 1/2 # eliminates the crash where they share the same x coordinate

    def move_to_player(self, player_x, player_y):
        angle = self._get_angle(player_x, player_y) # use the newly created function
        rotated = pygame.transform.rotate(self.sprite, 360-(angle*180/math.pi))
        screen.blit(rotated, (self.rectangle.x, self.rectangle.y))

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
            self.speed = 0
        else:
            self.speed = self.stored_speed # used the renamed variable
    def take_damage(self, damage):
        self.health -= damage
        damage_font = pygame.font.Font('freesansbold.ttf', 32)
        damage_text = damage_font.render("{}".format(damage), True, (255,255,255), (0,0,0))
        text_rect = pygame.Rect(self.rectangle.x+self.sprite_width/2, self.rectangle.y-25, 1,1)
        screen.blit(damage_text,text_rect)
    def is_dead(self):
        if self.health <= 0:
            return True
        else:
            return False
    
# bullet class code
bullet_speed = 10
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y):
        super().__init__()
        self.sprite = pygame.image.load('bullet.png')
        self.speed = bullet_speed
        self.image = pygame.Surface((50,10))
        self.image.fill((0,0,0))
        global left # tracks if the player is oriented left or right and using that it will change the bullet spawn position
        if left:
            self.rect = self.image.get_rect(center = (player_x, player_y))
        else:
            self.rect = self.image.get_rect(center = (player_x+64, player_y))
    def get_angle(self, mouse_x, mouse_y): # refactor the calculations of getting an angle into a function for more readability
        try:
            self.angle = math.atan2((mouse_y-self.rect.y),(mouse_x-self.rect.x))
        except ZeroDivisionError:
            self.angle = math.pi* 3/2 if self.rect.y < mouse_y else math.pi* 1/2
    def update(self):
        rotated = pygame.transform.rotate(self.sprite, 360-(self.angle*180/math.pi)) # finds the angle it needs to rotate
        screen.blit(rotated, (self.rect.x, self.rect.y))
        x_movement = self.speed*math.cos(self.angle)
        y_movement = self.speed*math.sin(self.angle)

        # Update x and y position based on player's position
        self.rect.x += x_movement if self.angle < math.pi/2 or (self.angle > 1/2*math.pi) else -x_movement
        self.rect.y += y_movement if self.angle < math.pi else -y_movement  


enemies = []
def spawn_bat(): 
    enemies.append(Enemy('bat.png', 64, 64, 10, 4, 0.5))
def spawn_vampire():
    enemies.append(Enemy('Vampire.png', 64, 90, 100, 2, 1))
def spawn_vampire_boss():
    enemies.append(Enemy('Vampire_boss.png', 128, 90, 250, 1, 2))

# upgrades 
damage_upgrade_tracker = pygame.image.load('damage_upgrade_tracker.png')
damage_upgrades = 0
health_upgrade_tracker = pygame.image.load('health_upgrade_tracker.png')
health_upgrades = 0
speed_upgrade_tracker = pygame.image.load('speed_upgrade_tracker.png')
speed_upgrades = 0
upgrades = 0
upgrade_text_box = pygame.Rect(15, height-160, 1, 1)
def draw_upgrade(text, block_height, upgrades):
    font = pygame.font.Font('freesansbold.ttf', 14)
    upgrade_text = font.render(text, True, (255,255,255))
    text_rect = pygame.Rect(15, block_height, 1,1)
    pygame.draw.rect(screen, "black", (15, block_height, 300, 24))
    if text == "Damage [1]":
        upgrade_tracker = damage_upgrade_tracker
    elif text == "Health [2]":
        upgrade_tracker = health_upgrade_tracker
    elif text == "Speed  [3]":
        upgrade_tracker = speed_upgrade_tracker
    for n in range(upgrades):
        screen.blit(upgrade_tracker, (18.5+50*n, block_height))
    screen.blit(upgrade_text, (text_rect.x, text_rect.y))

bullets = []
frame = 0
spawn_factor = 60 # controls how fast they spawn
while running:
    x_move = 0
    y_move = 0
    # Show floor
    screen.blit(floor_img, (0, 0))
    # shows clock
    clock.tick(60)
    frame += 1
    secs += 1/60
    screen.blit(clock_text, text_rect)
    if int(secs) == 60:
        secs = 0
        mins += 1
    clock_text = font.render("{}:{}".format(int(mins),int(secs)), True, (0,0,0), (255,255,255)) # clock rendering

    # enemy spawning
    if frame % spawn_factor == 0:
        spawn_bat()
    if frame % (spawn_factor*5) == 0:
        spawn_vampire()
    if frame % (spawn_factor*15) == 0:
        spawn_vampire_boss()
    
    # every minute the enemies will spawn 50% faster 
    if frame % (3600) == 0:
        spawn_factor = spawn_factor*0.5
    # every 15 seconds you get an upgrade, if the player is already maxed it heals the player to full
    if frame % (900) == 0:
        if (speed_upgrades+health_upgrades+damage_upgrades) == 18:
            player_health = total_health
        else:
            upgrades += 1
    protagonist = pygame.transform.scale(image, (64, 66))  
    # Event handling for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x - player_speed > 0:  #associates the keypressed to the movement of the player and checks if it will go off screen
        x_move -= player_speed  
        image = pygame.image.load(os.path.join('player_left.png'))
        left = True
    if keys[pygame.K_d] and player.x + player_speed + 128 < width:  #replace the 128s with the dimentions of the character
        x_move += player_speed  
        image = pygame.image.load(os.path.join('player_right.png'))
        left = False
    if keys[pygame.K_w] and player.y - player_speed > 0:  # (0,0) is the top corner so to move up yo need to subtract
        y_move -= player_speed  
    if keys[pygame.K_s] and player.y + player_speed + 128 < height:  
        y_move += player_speed  
    
    if x_move != 0 and y_move !=0: 
        x_move = x_move*math.sqrt(2)/2
        y_move = y_move*math.sqrt(2)/2

    player.x += x_move
    player.y += y_move
    draw_player(player)
    # draws the health bar
    ratio = player_health/total_health
    pygame.draw.rect(screen, "red", (player.x-150+32, player.y+75, 300, 40))
    if ratio > 0 :
        pygame.draw.rect(screen, "green", (player.x-150+32, player.y+75, 300*ratio, 40))
    else:
        running = False
    #draws upgrades
    upgrade_text = font.render("Number of upgrades x{}".format(upgrades), True, (0,0,0))
    screen.blit(upgrade_text, (upgrade_text_box.x, upgrade_text_box.y))
    draw_upgrade("Damage [1]", height-96, damage_upgrades)
    draw_upgrade("Health [2]", height-64, health_upgrades)
    draw_upgrade("Speed  [3]", height-32, speed_upgrades)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet(player.x, player.y)
            bullet.get_angle(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            bullets.append(bullet)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if upgrades > 0 and damage_upgrades < 6:
                    damage_upgrades += 1
                    upgrades -= 1
                    bullet_damage += 5
            if event.key == pygame.K_2 and health_upgrades < 6:
                if upgrades > 0:
                    health_upgrades += 1
                    upgrades -= 1
                    total_health += 100
                    player_health = total_health  
            if event.key == pygame.K_3 and speed_upgrades < 6:
                if upgrades > 0:
                    speed_upgrades += 1
                    upgrades -= 1
                    player_speed += 2.5
                    bullet_speed += 5              
    for i,bullet in enumerate(bullets):
        bullet.update()
        if bullet.rect.x >= width + 100 or bullet.rect.y >= height + 100 or bullet.rect.x <= -100 or bullet.rect.y <= -100:
            bullets.pop(i)
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rectangle):
                try:
                    bullets.pop(i)
                except IndexError: # there is a thing that crashes if you are hit and shooting and this catches it
                    continue
                enemy.take_damage(bullet_damage)
    for i,enemy in enumerate(enemies):
        enemy.move_to_player(player.x, player.y)
        enemy.player_collision(player)
        if enemy.is_dead():
            enemies.pop(i)
    pygame.display.flip()
pygame.quit()


