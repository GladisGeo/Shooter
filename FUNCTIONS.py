
import pygame as pg
from random import uniform, choice,random
from SETTINGS import *
from MAP import collide_hit_rect
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 1.5
                sprite.blocked=True
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 1.5
                sprite.blocked=True
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
        else:
            sprite.blocked=False    
            #print('touchingx')
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                sprite.blocked=True
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
                sprite.blocked=True
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
            #print('touchingy')
        else:
            sprite.blocked=False