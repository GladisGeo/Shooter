import pygame, sys
import pygame.freetype
from MAIN import Game
import SETTINGS
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
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

def character_menu():
    go=True
    while go == True:
        screen.fill(MAROON)
        draw_text('CHARACTER', gameSubfont, GOLD, screen, SETTINGS.WIDTH/3, 20)
        # draw_text('THE VIDEO GAME', gameSubfont, GOLD, screen, SETTINGS.WIDTH/3, 150)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(110, 250, 400, 50)
        button_2 = pygame.Rect(100, 320, 400, 50)
        button_3 = pygame.Rect(100, 390, 400, 50)
        button_4 = pygame.Rect(100, 460, 400, 50)       
        if button_4.collidepoint((mx, my)):
            if click:
                go=False
        pygame.draw.rect(screen, MAROON, button_1)
        draw_text('NEW', gameMenufont, GOLD, screen, 110, 260)
        pygame.draw.rect(screen, MAROON, button_2)
        draw_text('SAVE', gameMenufont, GOLD, screen, 110, 330)
        pygame.draw.rect(screen, MAROON, button_3)
        draw_text('CHOOSE', gameMenufont, GOLD, screen, 110, 400)
        pygame.draw.rect(screen, MAROON, button_4)
        draw_text('BACK', gameMenufont, GOLD, screen, 110, 470)        
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                surface = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
                SETTINGS.WIDTH=event.w
                SETTINGS.HEIGHT=event.h
        pygame.display.update()
        mainClock.tick(60)
