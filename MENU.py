import pygame, sys
import pygame.freetype
from MAIN import Game
from SETTINGS import *
from SINGLEPLAYERMENU import *
from MULTIPLAYERMENU import *
from CHARACTERMENU import *
from SETTINGSMENU import *

from pygame.locals import *
# Setup pygame/window ---------------------------------------- #
class mainMenu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('game base')
        # Create the window, saving it to a variable.
        self.difficulty="NORMAL"
        self.difficultyColor=YELLOW
        self.difficultyModifier=0
        self.gameGo=False
        self.screen = pygame.display.set_mode((1300, 600), pygame.RESIZABLE)
        self.digifont = pygame.freetype.Font("fonts/digital-7.ttf", 26) 
        self.gamefont = pygame.freetype.Font("fonts/AUTUMN_.TTF", 96) 
        self.gameSubfont = pygame.freetype.Font("fonts/AUTUMN_.TTF", 64) 
        self.gameMenufont = pygame.freetype.Font("fonts/AUTUMN_.TTF", 48) 
        self.font = pygame.font.SysFont(None, 20)
        self.gameGo=False
        self.BLACK=(0,0,0)
        self.GOLD=(212,175,55)
        self.MAROON=(128,0,0)
        self.click = False

    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        text_1, textblock = font.render(str(text),color)
        surface.blit(text_1, (x, y))

    def main_menu(self):
        while True:
            screen.fill(MAROON)
            draw_text('SCENARIO PAINTBALL', gamefont, GOLD, screen, SETTINGS.WIDTH/5, 10)
            draw_text('THE VIDEO GAME', gameSubfont, GOLD, screen, SETTINGS.WIDTH/3, 100)
            mx, my = pygame.mouse.get_pos()
            button_1 = pygame.Rect(110, 200, 400, 50)
            button_2 = pygame.Rect(100, 270, 400, 50)
            button_3 = pygame.Rect(100, 340, 400, 50)
            button_4 = pygame.Rect(100, 410, 400, 50)       
            button_5 = pygame.Rect(100, 460, 400, 50)   
            if button_1.collidepoint((mx, my)):
                if click:
                    self.game()
            if button_2.collidepoint((mx, my)):
                if click:
                    self.SPmenu()
            if button_3.collidepoint((mx, my)):
                if click:
                    self.MPmenu()

            if button_4.collidepoint((mx, my)):
                if click:
                    self.CHARmenu()
            if button_5.collidepoint((mx, my)):
                if click:
                    self.SETTINGSmenu()
            pygame.draw.rect(screen, MAROON, button_1)
            draw_text('DEVELOPMENT MODE', gameMenufont, GOLD, screen, 110, 210)
            pygame.draw.rect(screen, MAROON, button_2)
            draw_text('SINGLE PLAYER', gameMenufont, GOLD, screen, 110, 280)
            pygame.draw.rect(screen, MAROON, button_3)
            draw_text('MULTI PLAYER', gameMenufont, GOLD, screen, 110, 350)
            pygame.draw.rect(screen, MAROON, button_4)
            draw_text('CHARACTER', gameMenufont, GOLD, screen, 110, 420)     
            pygame.draw.rect(screen, MAROON, button_5)
            draw_text('SETTINGS', gameMenufont, GOLD, screen, 110, 490)         
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

    def SPmenu(self):
        sp_menu()
    def MPmenu(self):
        mp_menu()
    def CHARmenu(self):
        character_menu()
    def SETTINGSmenu(self):
        settings_menu(self)




    def game(self):
        self.gameGo=True
        g=Game(self)
        while self.gameGo==True:
            g.new()
            g.run()
        else:
            return()
one = mainMenu()
one.main_menu()
# while  True:
#     one.new()
#     one.run()

# main_menu()



