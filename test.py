import pygame
import os

pygame.init()

WIDTH, HEIGHT = 900, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("r/wallstreetsbets simulator")
WHITE = (255,255,255)
black = (0, 0, 0)
FPS = 60

cryptoGuy = pygame.image.load(os.path.join('Assets', 'cryptoGuy.png'))
#cryptoGuy = pygame.transform.scale(cryptoGuyImage, (100,100))

textBubble = pygame.image.load(os.path.join('Assets', 'textBubble.png'))

listOfNews = "Photo of monkey holding a physical MonkeyCoin goes viral"

instructions = "yapping"

textFont = pygame.font.Font(None, 30)

def draw_text(string, font, colour, rectangle):
    image = font.render(string, True, colour)
    window.blit(image, (rectangle.x, rectangle.y))


def draw_window():
    window.fill(WHITE)
    window.blit(cryptoGuy, (650, 250))
    window.blit(textBubble, (500, 150))

def main():
    instructionBox = pygame.Rect(525,175,1,1)
    letterBox = pygame.Rect(0,25,1,1)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        draw_window()
        draw_text(listOfNews, textFont, black, letterBox)
        draw_text(instructions, pygame.font.Font(None, 14), black, instructionBox)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.flip()
        letterBox.x += 1
        if letterBox.x == 900:
            letterBox.x = 0
        
    pygame.quit()

if __name__ == "__main__":
    main()