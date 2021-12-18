import pygame as pg
from random import uniform, choice,random
from SETTINGS import *
from MAP import collide_hit_rect
from FUNCTIONS import *
from MUZZLEFLASH import *
vec = pg.math.Vector2

class Cast(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, shooter):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self._layer = 3
        self.image = game.clear_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.rot = 0
        self.shooter=shooter
        spread = 0
        self.vel = dir.rotate(spread) * 1400
        self.spawn_time = pg.time.get_ticks()
    def update(self):
        self.rot = (self.shooter.target.pos - self.pos).angle_to(vec(1, 0))
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.shooter.LoS=False
            self.kill()
        elif pg.sprite.spritecollideany(self, self.game.mobs):
            self.shooter.LoS=False
            self.kill()

        elif pg.sprite.spritecollideany(self, self.game.players):
            self.shooter.LoS=True
            self.kill()