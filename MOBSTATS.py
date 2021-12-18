import pygame as pg
from random import uniform, choice,random
from SETTINGS import *
from MAP import collide_hit_rect
from FUNCTIONS import *
from MUZZLEFLASH import *
vec = pg.math.Vector2


class MobStats(pg.sprite.Sprite):
    def __init__(self, mob,game, pos):
        self.groups = game.all_sprites, game.mobStats
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.mob=mob
        self.pos = vec((pos.x,pos.y+80))
        self._layer = 5
        self.vel = vec(0, 0)
        self.image = self.game.mob_stat_img
        self.rect = self.image.get_rect()
        self.vel=self.mob.vel
        self.rect.center = pos
        self.rot = 0
        # for i in self.mob.podPack:
        #     self.image.blit(self.game.tipxMag_sprites[i['img']], (i['offset'], 5))
        # self.ammo_surface, rect = self.game.gameFont.render(str(self.mob.ammoCurrent), (20, 5, 20))
        # self.image.blit(self.ammo_surface, (50, 5))
    def update(self):
        self.rot = 0
        self.image = self.game.mob_stat_img
        self.rect = self.image.get_rect()
        self.rect.center = self.mob.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.pos = vec(self.mob.pos.x+10,self.mob.pos.y+150)
        self.rect = self.image.get_rect()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

    def printStats(self,e,f,g,h,j,k):
        self.image = self.game.mob_stat_img
        if self.mob.eliminated != True:
            for i in self.mob.podPack:
                if i['selected']==True:
                    self.image.blit(self.game.tipxMag_selected_sprites[i['count']], (i['offset'], 5))
                else:
                    self.image.blit(self.game.tipxMag_sprites[i['count']], (i['offset'], 5)) 
            self.image.blit(self.game.co2_sprites[self.mob.airIndex], (5, 40)) 
            self.ammo_surface, textblock = self.game.gameFont.render(str(e), PURPLE)
            self.air_surface, textblock = self.game.gameFont.render(str(f)+"%", WHITE)  
            self.air_reload_surface, textblock = self.game.gameFont.render(str(g), LIGHTGREY)              
            self.dodge_surface, textblock = self.game.gameFont.render(str(h)+"%", BLUE)
            self.action_surface, textblock = self.game.gameFont.render(str(j)+"%", RED)
            self.image.blit(self.ammo_surface, (65, 10))
            self.image.blit(self.air_surface, (20, 45))
            self.image.blit(self.air_reload_surface, (65, 45))

            self.image.blit(self.dodge_surface, (40, 70))
            pg.draw.rect(self.image, BLUE, self.mob.defense_bar)
            
            self.image.blit(self.action_surface, (40, 95))
            pg.draw.rect(self.image, RED, self.mob.action_bar)

            self.movement_surface, textblock = self.game.gameFont.render(str(k)+"%", YELLOW)
            self.image.blit(self.movement_surface, (40, 120))
            pg.draw.rect(self.image, YELLOW, self.mob.movement_bar)
        else:
            self.image.blit(self.game.eliminated_icon, (17, 30))