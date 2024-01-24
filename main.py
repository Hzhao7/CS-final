# Author: Henry Zhao, Benjamin Lu
# Date: 22nd January 2024
# Course: ICS3U0-B
# Description: Vampire Dyres is a 2D top down shooter where the main goal is to survive as long as possible. The player can move around the screen using WASD and shoot with left mouse. Enemies will spawn in depending on how long you have survived for. Hoever, their spawn rates will rapidly increase the longer you are alive. To counter this, you have the chance to upgrade your damage, max health, and speed as the game goes on. 

import pygame
import random
import math

pygame.init()

# Global variables
clock = pygame.time.Clock()
running = True
mouse_button_down = False

# Set window title
pygame.display.set_caption("Vampire Dyers")

# Set screen size
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

# Main Menu
menu = True
difficulty = "easy"
difficulty_factor = 2
instructions = False

# Loading menu images
image_files = [
    'menu_background.jpg',
    'instructions_background.jpg',
    'menu_play_button_default.png',
    'menu_play_button_hover.png',
    'menu_play_button_click.png',
    'menu_instructions_button_default.png',
    'menu_instructions_button_hover.png',
    'menu_instructions_button_click.png',
    'menu_difficulty_easy_button_default.png',
    'menu_difficulty_easy_button_hover.png',
    'menu_difficulty_easy_button_click.png',
    'menu_difficulty_medium_button_default.png',
    'menu_difficulty_medium_button_hover.png',
    'menu_difficulty_medium_button_click.png',
    'menu_difficulty_hard_button_default.png',
    'menu_difficulty_hard_button_hover.png',
    'menu_difficulty_hard_button_click.png'
]

images = {}
for image_file in image_files:
    try:
        images[image_file] = pygame.image.load(image_file)
    except:
        print(f"[DEBUG] Unable to locate {image_file} file")
        images[image_file] = pygame.image.load('missing_asset.png')

# Load the floor image
try:
    floor_img = pygame.image.load('floor.png')
except:
    print("[DEBUG] Unable to locate floor.png file")
    floor_img = pygame.image.load('missing_asset.png')

# Player image
try:
    image = pygame.image.load('player_left.png') #loads the protagonist image
except:
    print("[DEBUG] Unable to locate player_left.png file")
    image = pygame.image.load("missing_asset.png")

# reticle image
try:
    reticle = pygame.image.load('reticle.png')
except:
    print("[DEBUG] Unable to locate reticle.png file")
    reticle = pygame.image.load("missing_asset.png")
reticle_rect = pygame.Rect(width/2, height/2, 1, 1)
pygame.mouse.set_visible(False)

# Player code
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
frame = 0
font = pygame.font.Font('freesansbold.ttf', 32)
clock_text = font.render("{}:{}".format(mins,secs), True, (255,255,255), (0,0,0))
text_rect = pygame.Rect(width/2, 50, 1,1)

# High score code
high_score = open("highscore.txt", "r")
highscore_lines = high_score.readlines()
highscore_text = font.render("Highscore: {}:{}".format(highscore_lines[0].strip(), int(float(highscore_lines[1]))), True, (0,0,0))
highscore_rect = pygame.Rect(0, 0, 1, 1)

# Enemy Class code
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

    def _get_angle(self, player_x, player_y): # gets the angle between the player and the enemy
        try:
            return math.atan(abs(player_y-self.rectangle.y)/abs(player_x-self.rectangle.x))
        except ZeroDivisionError:
            return math.pi* 3/2 if self.rectangle.y < player_y else math.pi* 1/2 # eliminates the crash where the player and the enemy share the same x coordinate

    def move_to_player(self, player_x, player_y):
        angle = self._get_angle(player_x, player_y) 
        rotated = pygame.transform.rotate(self.sprite, 360-(angle*180/math.pi))
        screen.blit(rotated, (self.rectangle.x, self.rectangle.y)) # Rotates the image to align to the player

        # Calculate movement separately
        x_movement = self.speed*math.cos(angle)
        y_movement = self.speed*math.sin(angle)

        # Update x and y position based on player's position
        self.rectangle.x += x_movement if self.rectangle.x < player_x else -x_movement
        self.rectangle.y += y_movement if self.rectangle.y < player_y else -y_movement

    def player_collision(self, player_rect): 
        if self.rectangle.colliderect(player_rect): # checks if the enemy is hitting the player
            global player_health 
            player_health -= self.damage
            self.speed = 0 # the enemy will stop moving if it is hitting
        else:
            self.speed = self.stored_speed # resets the speed once the enemy is not hitting the player

    def take_damage(self, damage): # Everytime and enemy takes damage they will display an indicator for how much damage was done
        self.health -= damage
        damage_font = pygame.font.Font('freesansbold.ttf', 32)
        damage_text = damage_font.render("{}".format(damage), True, (255,255,255), (0,0,0))
        text_rect = pygame.Rect(self.rectangle.x+self.sprite_width/2, self.rectangle.y-25, 1,1)
        screen.blit(damage_text,text_rect) 

    def is_dead(self): # returns if the enemy is dead or not
        if self.health <= 0:
            return True
        else:
            return False
        
# Functions for creating different enemies and creates an empty list to add enemies to.
enemies = []
spawn_factor = 60 # controls how fast they spawn
def spawn_bat(): 
    enemies.append(Enemy('bat.png', 64, 64, 10, 4, 0.5))
def spawn_vampire():
    enemies.append(Enemy('Vampire.png', 64, 90, 100, 2, 1))
def spawn_vampire_boss():
    enemies.append(Enemy('Vampire_boss.png', 128, 90, 250, 1, 2))
    
# bullet class code and bullet global variables.
bullet_damage = 5
bullet_speed = 10
bullets = []
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y):
        super().__init__()
        try:
            self.sprite = pygame.image.load('bullet.png')
        except:
            print("[DEBUG] Unable to locate bullet.png file")
            self.sprite = pygame.image.load("missing_asset.png")
        self.speed = bullet_speed
        self.image = pygame.Surface((50,10))
        self.image.fill((0,0,0))
        global left # tracks if the player is oriented left or right and using that it will change the bullet spawn position
        if left:
            self.rect = self.image.get_rect(center = (player_x, player_y))
        else:
            self.rect = self.image.get_rect(center = (player_x+64, player_y))
    def get_angle(self, mouse_x, mouse_y): # gets the angle between the player and the mouse position
        try:
            self.angle = math.atan2((mouse_y-self.rect.y),(mouse_x-self.rect.x))
        except ZeroDivisionError:
            self.angle = math.pi* 3/2 if self.rect.y < mouse_y else math.pi* 1/2
    def update(self):
        rotated = pygame.transform.rotate(self.sprite, 360-(self.angle*180/math.pi)) # finds the angle it needs to rotate
        screen.blit(rotated, (self.rect.x, self.rect.y))
        x_movement = self.speed*math.cos(self.angle)
        y_movement = self.speed*math.sin(self.angle)

        # Update x and y position based on the angle stored
        self.rect.x += x_movement if self.angle < math.pi/2 or (self.angle > 1/2*math.pi) else -x_movement
        self.rect.y += y_movement if self.angle < math.pi else -y_movement  

# upgrade image loading and storing the anmount of each and available upgrades.
try:
    damage_upgrade_tracker = pygame.image.load('damage_upgrade_tracker.png')
except:
    print("[DEBUG] Unable to locate damage_upgrade_tracker.png file")
    damage_upgrade_tracker = pygame.image.load("missing_asset.png")
damage_upgrades = 0
try:
    health_upgrade_tracker = pygame.image.load('health_upgrade_tracker.png')
except:
    print("[DEBUG] Unable to locate health_upgrade_tracker.png file")
    health_upgrade_tracker = pygame.image.load("missing_asset.png")
health_upgrades = 0
try:
    speed_upgrade_tracker = pygame.image.load('speed_upgrade_tracker.png')
except:
    print("[DEBUG] Unable to locate speed_upgrade_tracker.png file")
    speed_upgrade_tracker = pygame.image.load("missing_asset.png")
speed_upgrades = 0
upgrades = 0
upgrade_text_box = pygame.Rect(15, height-160, 1, 1)

# draws the upgrade box and how much that upgrade has been upgraded
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

# main loop
while running:
    #sets to a max of 60 fps
    clock.tick(60)
    # gets mouse coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # stores player movement
    x_move = 0
    y_move = 0
    # reshapes the image of the player
    protagonist = pygame.transform.scale(image, (64, 66))
    # Show floor
    screen.blit(floor_img, (0, 0))
    # Show clock
    frame += 1
    secs += 1/60
    screen.blit(clock_text, text_rect)
    if int(secs) == 60:
        secs = 0
        mins += 1
    clock_text = font.render("{}:{}".format(int(mins),int(secs)), True, (0,0,0), (255,255,255)) # clock rendering
    # Show Highscore
    screen.blit(highscore_text, highscore_rect)

    # enemy spawning
    if frame % spawn_factor == 0:
        spawn_bat()
    if frame % (spawn_factor*5) == 0:
        spawn_vampire()
    if frame % (spawn_factor*15) == 0:
        spawn_vampire_boss()
    
    # every minute the enemies will spawn 50% faster 
    if frame % (3600) == 0:
        if difficulty_factor == 0.5: # if the difficulty is hard, the spawn rate increase each minute will double
            spawn_factor = spawn_factor*0.5*difficulty_factor
        else:
            spawn_factor = spawn_factor*0.5
    # every number of seconds the player gets an upgrade
    if frame % (900/difficulty_factor) == 0:
        if (speed_upgrades+health_upgrades+damage_upgrades+upgrades) == 18: #if the player is maxed on upgrades it will heal the player to max instead
            player_health = total_health
        else:
            upgrades += 1  

    # Event handling for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x - player_speed > 0:  #associates the keypressed to the movement of the player and checks if it will go off screen
        x_move -= player_speed
        try:
            image = pygame.image.load('player_left.png')
        except:
            print("[DEBUG] Unable to locate player_left.png file")
            image = pygame.image.load("missing_asset.png")
        left = True
    if keys[pygame.K_d] and player.x + player_speed + 64 < width:  
        x_move += player_speed
        try:
            image = pygame.image.load('player_right.png')
        except:
            print("[DEBUG] Unable to locate player_right.png file")
            image = pygame.image.load("missing_asset.png")
        left = False
    if keys[pygame.K_w] and player.y - player_speed > 0:  # (0,0) is the top corner so to move up you need to subtract
        y_move -= player_speed  
    if keys[pygame.K_s] and player.y + player_speed + 66 < height:  
        y_move += player_speed  
    
    if x_move != 0 and y_move !=0: # if the player is moving diagonally, it reduces the x and y speed to prevent the player from moving faster
        x_move = x_move*math.sqrt(2)/2
        y_move = y_move*math.sqrt(2)/2
    # moves the player
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
            mouse_button_down = True
            # ===================================================
            if menu and not instructions:
                if play_button_area.collidepoint((mouse_x, mouse_y)):
                    print("Clicked play")
                    menu = False

                elif difficulty_button_area.collidepoint((mouse_x, mouse_y)):
                    print("Clicked difficulty")
                    print(difficulty)
                    match difficulty:
                        case "easy":
                            difficulty = "medium"
                            difficulty_factor = 1
                        case "medium":
                            difficulty = "hard"
                            difficulty_factor = 0.5
                        case "hard":
                            difficulty = "easy"
                            difficulty_factor = 2

                elif instructions_button_area.collidepoint((mouse_x, mouse_y)):
                    print("Clicked instructions")
                    instructions = True
            elif instructions and mouse_x < 150 and mouse_y < 100:
                instructions = False
            # ===================================================
            bullet = Bullet(player.x, player.y)
            bullet.get_angle(mouse_x,mouse_y)
            bullets.append(bullet) # if the mouse left is clicked a bullet will be added to the list of bullets
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down = False
        if event.type == pygame.KEYDOWN: # adds the upgrades if the player presses the respective button
            if event.key == pygame.K_1:
                if upgrades > 0 and damage_upgrades < 6: # checks if the player has available upgrades and the player is not already capped on the respective upgrade
                    damage_upgrades += 1
                    upgrades -= 1
                    bullet_damage += 5*difficulty_factor
            if event.key == pygame.K_2 and health_upgrades < 6:
                if upgrades > 0:
                    health_upgrades += 1
                    upgrades -= 1
                    total_health += 100*difficulty_factor
                    player_health = total_health  
            if event.key == pygame.K_3 and speed_upgrades < 6:
                if upgrades > 0:
                    speed_upgrades += 1
                    upgrades -= 1
                    player_speed += 2.5
                    bullet_speed += 5*difficulty_factor              
    for i,bullet in enumerate(bullets): # for each bullet on screen it will update their position every frame
        bullet.update()
        if bullet.rect.x >= width + 100 or bullet.rect.y >= height + 100 or bullet.rect.x <= -100 or bullet.rect.y <= -100: # if the bullet is out of bounds it gets removed
            bullets.pop(i)
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rectangle): # if a bullet hits an enemy it will take damage and the bullet disappears
                try:
                    bullets.pop(i)
                except IndexError: # If multiple enemies are hit by a bullet, the program tries to remove the same bullet more than once creating an index error. If that happens the program continues and only one enemy takes damage
                    continue
                enemy.take_damage(bullet_damage)
    for i,enemy in enumerate(enemies): # Moves every enemy and checks if they collide with the player
        enemy.move_to_player(player.x, player.y)
        enemy.player_collision(player)
        if enemy.is_dead(): # if the enemy is dead it removes them from the screen
            enemies.pop(i)

    #reticle code
    reticle_rect.center = (mouse_x, mouse_y)
    screen.blit(reticle, (reticle_rect.x-24, reticle_rect.y-24))

    # Main menu
    if menu == True:
        # Show main menu background
        screen.blit(images['menu_background.jpg'], (0, 0))
        # Reveal cursor that was supposed to replaced by recticle
        pygame.mouse.set_visible(True)
        # Stop game progression
        frame = 0
        secs = 0
        bullets = []
        # Set the display areas for the menu buttons with sizes 291x64
        play_button_area = pygame.Rect(500, 375, 291, 64)
        difficulty_button_area = pygame.Rect(500, 475, 291, 64)
        instructions_button_area = pygame.Rect(500, 575, 291, 64)

        # Do not display buttons if in instructions page
        if not instructions:
            # Display play button
            if play_button_area.collidepoint((mouse_x, mouse_y)):
                screen.blit(images['menu_play_button_hover.png'], play_button_area)
            else:
                screen.blit(images['menu_play_button_default.png'], play_button_area)
            # Display difficulty button
            match difficulty:
                case "easy":
                    if difficulty_button_area.collidepoint((mouse_x, mouse_y)):
                        screen.blit(images['menu_difficulty_easy_button_hover.png'], difficulty_button_area)
                    else:
                        screen.blit(images['menu_difficulty_easy_button_default.png'], difficulty_button_area)
                case "medium":
                    if difficulty_button_area.collidepoint((mouse_x, mouse_y)):
                        screen.blit(images['menu_difficulty_medium_button_hover.png'], difficulty_button_area)
                    else:
                        screen.blit(images['menu_difficulty_medium_button_default.png'], difficulty_button_area)
                case "hard":
                    if difficulty_button_area.collidepoint((mouse_x, mouse_y)):
                        screen.blit(images['menu_difficulty_hard_button_hover.png'], difficulty_button_area)
                    else:
                        screen.blit(images['menu_difficulty_hard_button_default.png'], difficulty_button_area)
            # Display instructions button
            if instructions_button_area.collidepoint((mouse_x, mouse_y)):
                screen.blit(images['menu_instructions_button_hover.png'], instructions_button_area)
            else:
                screen.blit(images['menu_instructions_button_default.png'], instructions_button_area)
        else:
            screen.blit(images['instructions_background.jpg'], (0, 0))

        # Using a dictionary to store information about difficulty levels
        # difficulty = difficulty_dict[difficulty]['next']
        difficulty_dict = {
            # 'easy': {'default': menu_difficulty_easy_button_default, 'hover': menu_difficulty_easy_button_hover, 'click': menu_difficulty_easy_button_click, 'next': 'medium'},
            # 'medium': {'default': menu_difficulty_medium_button_default, 'hover': menu_difficulty_medium_button_hover, 'click': menu_difficulty_medium_button_click, 'next': 'hard'},
            # 'hard': {'default': menu_difficulty_hard_button_default, 'hover': menu_difficulty_hard_button_hover, 'click': menu_difficulty_hard_button_click, 'next': 'easy'}
            'easy': {'default': images['menu_difficulty_easy_button_default.png'], 'hover': images['menu_difficulty_easy_button_hover.png'], 'click': images['menu_difficulty_easy_button_click.png'], 'next': 'medium'},
            'medium': {'default': images['menu_difficulty_medium_button_default.png'], 'hover': images['menu_difficulty_medium_button_hover.png'], 'click': images['menu_difficulty_medium_button_click.png'], 'next': 'hard'},
            'hard': {'default': images['menu_difficulty_hard_button_default.png'], 'hover': images['menu_difficulty_hard_button_hover.png'], 'click': images['menu_difficulty_hard_button_click.png'], 'next': 'easy'}
        }
    pygame.display.flip()

# record down the high score before quitting
if mins >= int(highscore_lines[0].strip()) and secs > int(float(highscore_lines[1].strip())):
    L = [f'{mins}\n', f'{secs}']
    high_score = open("highscore.txt", "w")
    high_score.writelines(L)
    high_score.close()
pygame.quit()
