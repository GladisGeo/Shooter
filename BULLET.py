import pygame as pg
from random import uniform, choice,random
from SETTINGS import *
from MAP import collide_hit_rect
from FUNCTIONS import *
from MUZZLEFLASH import *
vec = pg.math.Vector2


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, shooter, spreader):
        if shooter.type=='player':
            self.groups = game.all_sprites, game.playerBullets
        else:
            self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self._layer = 3
        self.speed=700
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.rot = 0
        self.shooter=shooter
        spread = uniform(-spreader, spreader)
        self.vel = dir.rotate(spread) * self.speed
        self.spawn_time = pg.time.get_ticks()
        if self.shooter.type=="player":
            choice(self.game.weapon_sounds).play(0)
            self.game.splatSounds[1].play(0)
        if self.shooter.type=="mob":
             self.game.weapon_sounds[1].play(0)

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.mask = pg.mask.from_surface(self.image)

        #if pg.sprite.spritecollideany(self, self.game.walls, False, pg.sprite.collide_mask):
        if pg.sprite.spritecollideany(self, self.game.walls):
            MuzzleFlash(self.game, self.pos,"splat")
            choice(self.game.splatSounds).play(0)
            self.kill()

        # elif pg.sprite.spritecollideany(self, self.game.players):
        #     if self.shooter.type =="mob":

        #         choice(self.game.splatSounds).play(0)

        if(self.shooter.type=="mob"):

            if pg.time.get_ticks() - self.spawn_time > randint(self.shooter.minRange, self.shooter.maxRange):
                self.kill()
        elif (self.shooter.type=="player"):
            
            if pg.time.get_ticks() - self.spawn_time > randint(self.game.player.minRange, self.game.player.maxRange):
                self.kill()
