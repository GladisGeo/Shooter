import pygame as pg
from random import uniform, choice,random
from SETTINGS import *
from MAP import collide_hit_rect
vec = pg.math.Vector2

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos,effect):
        self._layer = 4
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.duration = 40
        
        if effect =="flash":
            size = randint(20, 50)
            self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        elif effect=="splat":
            self.image = pg.transform.scale(choice(game.paint_splats), (40, 40))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()
