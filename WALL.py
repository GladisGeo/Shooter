import pygame as pg
from random import uniform, choice,random
from SETTINGS import *
from MAP import collide_hit_rect
from FUNCTIONS import *
from MUZZLEFLASH import *
from CAST import *
from BULLET import *
vec = pg.math.Vector2

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.mask = pg.mask.from_surface(self.image)
        self._layer = 2
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.pos = vec(self.x, self.y)
        self.rect.center=self.pos
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h,type):
        if type =="stopper":
            self.groups = game.stoppers
        elif type =="wall":
            self.groups = game.walls
        elif type == "mobRespawn":
            self.groups = game.items,game.walls
            self.type="mobRespawn"
        elif type == "playerRespawn":
            self.groups = game.items,game.walls
            self.type="playerRespawn"
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.pos = vec(self.x, self.y)
        self.rect.center=self.pos
        self.rect.x = x
        self.rect.y = y
 