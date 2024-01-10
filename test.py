import pygame
from pygame.locals import *
import os

pygame.init()

width, height = 900, 500
window = pygame.display.set_mode((width, height)) #creates a window
pygame.display.set_caption("Vampire Dyres")
white = (255,255,255)
black = (0, 0, 0)
FPS = 60


protagonist = pygame.image.load(os.path.join('Assets', 'placeholder_character.png')) #loads the protagonist image
player_speed = 5 #how many pixels the player moves each button press

def draw_window():
    window.fill(white)


def draw_player(player):
    window.blit(protagonist, (player.x,player.y)) #draws the player onto the screen using the rectangle's coordinates

def player_movement(keys_pressed, player): # does player movement
    if keys_pressed[pygame.K_a] and player.x - player_speed > 0:  #associates the keypressed to the movement of the player and checks if it will go off screen
        player.x -= player_speed  
        print("pressed a")
    if keys_pressed[pygame.K_d] and player.x + player_speed + 128 < 900:  #replace the 128s with the dimentions of the character
        player.x += player_speed  
        print("pressed d")
    if keys_pressed[pygame.K_w] and player.y - player_speed > 0:  # (0,0) is the top corner so to move up yo need to subtract
        player.y -= player_speed  
        print("pressed w")
    if keys_pressed[pygame.K_s] and player.y + player_speed + 128 < 500:  
        player.y += player_speed  
        print("pressed s")

def main():
    player = pygame.Rect(450, 250, 128, 128) #creates a rectangle for the player to check collision
    clock = pygame.time.Clock() # sets up a clock
    run = True
    while run:
        clock.tick(FPS) # sets FPS
        for event in pygame.event.get(): # if the x is hit the program closes
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed() # finds the current key pressed
        player_movement(keys_pressed, player)   # moves the player
        draw_window() 
        draw_player(player)
        pygame.display.flip() # updates the display
    pygame.quit()

if __name__ == "__main__":
    main()
