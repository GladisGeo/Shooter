import pygame as pg
from random import uniform, choice,random
from SETTINGS import *
from MAP import collide_hit_rect
from FUNCTIONS import *
from MUZZLEFLASH import *
from CAST import *
from BULLET import *
from MOBSTATS import*
vec = pg.math.Vector2

class Mob(pg.sprite.Sprite):
    def __init__(self, game,index, x, y):
        self.groups = game.all_sprites,game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self._layer = 2
        self.game = game
        self.difficultyModifier=self.game.mainmenu.difficultyModifier
        self.minimumRange=80
        self.accuracy=5+self.difficultyModifier
        self.blocked=False
        self.eliminated=False
        self.sprinting=False
        self.totalMovementPoints =100+self.difficultyModifier
        self.movementPoints=self.totalMovementPoints
        self.movementRecharge=8
        self.movementPercent=100
        self.minRange=1000
        self.maxRange=1500
        self.type="mob"
        self.index=index
        self.speed=150+self.difficultyModifier
        self.spread=3
        self.actionPercent=100
        self.totalactionPoints=100
        self.outOfAmmo=False
        self.outOfPods=False
        self.ammoCurrent=7
        self.ammoTotal=7
        self.airIndex=0
        self.airReloadIndex=0
        self.cartridges=3
        self.airPercent=100
        self.airVolume=13
        self.airVolumeTotal=13
        self.totalPods=4
        self.extraPods=1
        self.currentMagImg=self.game.tipxMag_sprites[2]
        self.currentPodIndex=0
        self.reloadIndex=0
        self.airReloadRate=12
        self.reloadRate=8
        self.airReloadImg=0
        self.reloadImg=0
        self.airReloading=False
        self.reloading = False
        self.podCounter=0
        podOffset=5
        self.podPack=[]
        for i in range(self.totalPods):
            pod={'selected':False,'status':'full','capacity':7,'count':7,'img':0,'offset':podOffset}
            self.podPack.append(pod)
            podOffset += 15
        self.currentPod=self.podPack[0]
        self.currentPod['selected']=True
        self.moving=False
        self.rateOfFire=30
        self.image = self.game.mob_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.damage=10
        self.knockback=10
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.statBar=MobStats(self,self.game,self.pos)
        self.rot = 0
        self.currentAmmoCount=7
        self.totalAmmoCount=7
        self.actionPoints=100+self.difficultyModifier
        self.LoS=False
        self.move=True
        self.totalDefense=100+self.difficultyModifier
        self.defense = self.totalDefense
        self.avoidRadius= 50
        self.detectRadius = 900
        self.fireRadius= 400
        self.speed = choice([ 150,100, 175, 125])
        self.target = game.player
        self.respawnPoint=game.mobRespawn
        self.objective=None
        self.statCounter=1
        self.defenseRecharge=60
        self.defensePercent=100
        self.actionRecharge=60
        self.inDeadBox=False
        self.shotTimer=0
        self.shooting=False
        self.airWait=False
        self.movementRecharging=False
        self.resting=False
        print(self.pos)


    def incrementStats(self):
        self.statCounter+=1
        if self.statCounter==self.defenseRecharge:
            if self.defense<self.totalDefense and self.eliminated != True:
                test=self.defense+5
                if test >self.totalDefense:
                    diff=test-self.totalDefense
                    self.defense +=5-diff
                else:
                    self.defense=test
                self.percenter('defense')

        if self.statCounter==self.movementRecharge:
            if self.movementPoints<self.totalMovementPoints and self.eliminated != True and self.move!=True and self.movementRecharging==True:
                self.movementRecharging=True
                test=self.movementPoints+25
                if test >self.totalMovementPoints:
                    diff=test-self.totalMovementPoints
                    self.movementPoints +=25-diff
                else:
                    self.movementPoints=test
                self.percenter('movement')
            if self.movementPoints==100:
                self.resting=False

        if self.statCounter==self.actionRecharge:
                if self.actionPoints<self.totalactionPoints and self.eliminated != True:
                    test=self.actionPoints+10
                    if test >self.totalactionPoints:
                        diff=test-self.totalactionPoints
                        self.actionPoints +=10-diff
                    else:
                        self.actionPoints=test
        if self.statCounter==61:    
            self.statCounter=1

    def respawn(self):
        if self.game.respawnOpen == True :
            if self.inDeadBox==True:
                self.eliminated=False
                self.outOfAmmo=False
                self.outOfPods=False
                self.podCounter=0
                self.currentPodIndex =0 
                self.reloadIndex=0
                self.game.mob_images[self.index] =self.game.mob_right_reload_sequence[0]
                self.actionPoints=self.totalactionPoints
                self.target=self.game.player
                self.defense=self.totalDefense
                self.ammo=self.totalAmmoCount
                self.airVolume=self.airVolumeTotal
                self.cartridges=2
                self.movementPoints=self.totalMovementPoints
                for i in self.podPack:
                    i['selected']=False
                    i['status']='full'
                    i['count']=i['capacity']
                    i['img']=0
                #pod={'selected':False,'status':'full','capacity':7,'count':7,'img':0,'offset':podOffset}
                self.currentPod=self.podPack[0]
                self.currentPod['selected']=True
                self.dodge()
                self.inDeadBox=False

    def printStats(self,e,f,g,h,j,k):
            self.statBar.printStats(e,f,g,h,j,k)
        
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < self.avoidRadius:
                    self.acc += dist.normalize()

    def avoid_walls(self):

        if self.blocked==True:
          for i in range(round(20)):
            adjustrot=160
            self.acc = vec(1, 0).rotate(self.rot+adjustrot)
            self.acc.scale_to_length(self.speed*round(self.defensePercent))
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt*2
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            collide_with_walls(self, self.game.stoppers, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            collide_with_walls(self, self.game.stoppers, 'y')
            self.rect.center = self.hit_rect.center


    def dodge(self):
        self.move=True
        if self.movementPoints >=10:
            self.movementPoints-=10
        else:
            self.movementPoints=0
        self.percenter('defense')
        self.percenter('movement')
        adjustrot=choice([-90,90,45,-45])
        for i in range(round(self.defense/17)):
            self.acc = vec(1, 0).rotate(self.rot+adjustrot)
            self.acc.scale_to_length(self.speed*round(self.defensePercent/10))
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt*2
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            collide_with_walls(self, self.game.stoppers, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
        
            collide_with_walls(self, self.game.stoppers, 'y')
            self.rect.center = self.hit_rect.center
            self.inDeadBox=False

    def percenter(self,selector):
        index=0
        if selector == "air":
            current=self.airVolume
            total=self.airVolumeTotal
        if selector == "ammo":
            current=self.currentAmmoCount
            total=self.totalAmmoCount
        if selector == "defense":
            current=self.defense
            total=self.totalDefense
        if selector == "action":
            current=self.actionPoints
            total=self.totalactionPoints
        if selector == "movement":
            current=self.movementPoints
            total=self.totalMovementPoints
        percent=round(current/total*100)
        if percent <= 85:
            index=1
        if percent <= 70:
            index=2
        if percent <= 65:
            index=3
        if percent <= 50:
            index=4
        if percent <= 35:
            index=5
        if percent <= 20:
            index=6
        if percent == 0:
            index=7   
        if selector == "air":
            self.airVolume=current
            self.airPercent=percent
            self.airIndex=index
            if self.airVolume==0:
                if self.cartridges!=0:
                    self.airReloading=True
            self.minRange=(self.minRange/100)*self.airPercent
            self.minRange=(self.maxRange/100)*self.airPercent
        if selector == "ammo":
            self.currentAmmoCount=current
            self.ammoPercent=percent
            self.ammoIndex=index 
        if selector == "defense":
            self.defense=current
            self.defensePercent=percent
        if selector == "action":
            self.actionPoints=current
            self.actionPercent=percent
        if selector == "movement":
            self.movementPoints=current
            self.movementPercent=percent
            if self.movementPoints==0:
                self.resting=True
                self.movementRecharging=True
            if self.movementPoints==self.totalactionPoints:
                self.movementRecharging=False

    def updateStats(self):
        if self.defense <= 0:
            self.target=self.game.mobRespawn
            self.game.mob_images[self.index]=self.game.mob_eliminated_img
            self.eliminated=True
            self.resting ==False

        if self.eliminated != True:
            self.incrementStats()
            self.draw_defense()
            self.reload()
            self.airReload()
            self.percenter('air')
            self.percenter('action')
            self.percenter('movement')
            self.percenter('defense')
        else:
            self.respawn()


    def update(self):
        self.updateStats()
        ##Distance to target
        self.target_dist = self.target.pos - self.pos
        self.respawnPoint =self.game.mobRespawn
        self.respawn_dist = self.respawnPoint.pos - self.pos
        if self.objective != None:
            self.objective_dist = self.objective.pos - self.pos
        ##In Firing Range bool
        self.inRange= self.target_dist.length_squared() < self.fireRadius**2
        ##In Detect Range Bool
        self.fixedTarget = self.target_dist.length_squared() < self.detectRadius**2

        self.CQB = self.target_dist.length_squared() < self.minimumRange**2

        if self.resting==False and self.actionPoints>0:
            self.move=True

        if self.resting==True:
            self.move=False

        self.makeMove()
        if self.target.type!='mobRespawn':
            if self.target.eliminated ==False and self.target.inDeadBox==False:
                self.shoot()

    def makeMove(self):
        moveDrain=.25
        if not self.eliminated and self.target.eliminated!= True and self.fixedTarget:
            self.rot = self.target_dist.angle_to(vec(1, 0))
        else:
            self.rot = self.respawn_dist.angle_to(vec(1, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.image =pg.transform.rotozoom(self.game.mob_images[self.index], self.rot,1)
        try:
            if self.sprinting==False:
                self.acc.scale_to_length(self.speed)
            else:
                self.acc.scale_to_length(self.speed*2)
                moveDrain=.60
        except:
            pass
        if self.move ==True and self.CQB==False and self.target.eliminated==False or self.eliminated==True: 
            # self.avoid_mobs()
            # self.avoid_walls()
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x

            collide_with_walls(self, self.game.walls, 'x')
            collide_with_walls(self, self.game.stoppers, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            collide_with_walls(self, self.game.stoppers, 'y')
            self.rect.center = self.hit_rect.center

            # if self.movementPoints>1:
            #     self.movementPoints-=moveDrain
            # else:
            #     self.movementPoints=0

    def airReload(self):
        if self.airReloading==True :
            self.airWait = True
            if self.actionPoints>20:
                self.airReloadIndex+=1
                if self.airReloadIndex == self.airReloadRate:
                    self.airReloadIndex=0
                    self.airReloadImg+=1
                    self.game.mob_images[self.index]=self.game.mob_right_air_reload_sequence[self.airReloadImg]
                if self.airReloadImg ==15:
                    self.airReloadImg=0
                    self.airReloading=False
                    self.airVolume=self.airVolumeTotal
                    self.cartridges-=1
                    self.actionPoints-=20
                    self.airWait=False
    def reload(self):
        if self.outOfPods ==False and self.reloading ==True: 
            if self.actionPoints>20 and self.outOfAmmo==False:   
                if self.airWait == True:
                    return()
                self.reloadIndex+=1
                if self.reloadIndex == self.reloadRate:
                    self.reloadIndex=0
                    self.reloadImg+=1
                    self.game.mob_images[self.index]=self.game.mob_right_reload_sequence[self.reloadImg]
                if self.reloadImg ==14:
                    self.reloadImg=0
                    self.reloading=False
                    self.currentPod['selected']=False
                    self.currentPod['img']=0
                    self.currentPod['count']=0
                    self.currentPod['status']="empty"
                    self.currentPodIndex +=1
                    self.actionPoints-=20
                    try:
                        self.currentPod=self.podPack[self.currentPodIndex]
                        self.currentPod['selected']=True
                    except:
                        self.outOfPods=True    
                    self.airWait=False

    def shoot(self):
        dir = vec(1, 0).rotate(-self.rot)
        pos = self.pos + PISTOL_OFFSET.rotate(-self.rot)
        Cast(self.game, pos, dir, self)
        if self.LoS==True and self.inRange==True:
            if self.statCounter % self.rateOfFire == 0 and self.outOfAmmo==False:
                now = pg.time.get_ticks()
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + PISTOL_OFFSET.rotate(-self.rot)
                if self.currentPod['count'] != 0 and self.actionPoints >=10:
                    if self.airVolume !=0:
                        self.airVolume-=1
                        Bullet(self.game, pos, dir,self,self.spread)
                        self.vel = vec(-KICKBACK, 0).rotate(-self.rot)
                        MuzzleFlash(self.game, pos,"flash")
                        self.currentPod['count']-=1
                        if self.actionPoints>15 :
                            self.actionPoints-=15
                        else:
                            self.actionPoints=0
        if self.currentPod['count'] == 0 and self.outOfPods==False:
            self.reloading=True  
        if self.currentPodIndex+1 ==len(self.podPack) and self.currentPod['count'] == 0:
            self.reloading==False
            self.outOfAmmo=True
            self.currentPod['img']=0
            self.currentPod['status']="empty"

    def draw_defense(self):
        defenseWidth = int(30* self.defense / self.totalDefense)
        self.defense_bar = pg.Rect(5, 75, defenseWidth, 7)

        actionWidth = int(30* self.actionPoints / self.totalactionPoints)
        self.action_bar = pg.Rect(5, 100, actionWidth, 7)
        
        movementWidth = int(30* self.movementPoints / self.totalMovementPoints)
        self.movement_bar = pg.Rect(5, 125, movementWidth, 7)




