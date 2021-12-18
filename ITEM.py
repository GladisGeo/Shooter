import pygame as pg
from random import uniform, choice,random
from SETTINGS import *
from MAP import collide_hit_rect
from FUNCTIONS import *
from MUZZLEFLASH import *
from CAST import *
from BULLET import *
vec = pg.math.Vector2  
    
class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = 1
        self.type = type
        self.eliminated=False
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if self.type=="mobRespawn":
            self.image = game.item_images['mobRespawn']
        if self.type=="playerRespawn":
            self.image = game.item_images['playerRespawn']
        if self.type=="health":
                self.image = game.item_images['health']           

        self.rect = self.image.get_rect()
        
        self.rect.center = pos
        self.pos = pos