import pygame, sys
import pygame.freetype
from MAIN import Game
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
# Create the window, saving it to a variable.
screen = pygame.display.set_mode((1300, 600), pygame.RESIZABLE)
digifont = pygame.freetype.Font("fonts/digital-7.ttf", 26) 
gamefont = pygame.freetype.Font("fonts/AUTUMN_.TTF", 96) 
gameSubfont = pygame.freetype.Font("fonts/AUTUMN_.TTF", 64) 
gameMenufont = pygame.freetype.Font("fonts/AUTUMN_.TTF", 48) 
font = pygame.font.SysFont(None, 20)
BLACK=(0,0,0)
GOLD=(212,175,55)
MAROON=(128,0,0)
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    text_1, textblock = font.render(str(text),color)
    surface.blit(text_1, (x, y))
 
click = False
 
def main_menu():
    while True:
        screen.fill(MAROON)
        draw_text('SCENARIO PAINTBALL', gamefont, GOLD, screen, 100, 50)
        draw_text('THE VIDEO GAME', gameSubfont, GOLD, screen, 250, 150)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(100, 250, 400, 50)
        
        button_2 = pygame.Rect(100, 350, 400, 50)
        
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        pygame.draw.rect(screen, MAROON, button_1)
        draw_text('DEVELOPMENT MODE', gameMenufont, GOLD, screen, 110, 260)
        pygame.draw.rect(screen, MAROON, button_2)
        draw_text('SINGLE PLAYER', gameMenufont, GOLD, screen, 110, 360)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == KEYDOWN:
            #     if event.key == K_ESCAPE:
            #         pygame.quit()
            #         # sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                 surface = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
        pygame.display.update()
        mainClock.tick(60)

def game():
    g = Game()
    while True:
        g.new()
        g.run()
    else:
        return()

main_menu()

    # pygame.display.update()
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #         sys.exit()
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_ESCAPE:
    #             pygame.quit()
    #             sys.exit()

