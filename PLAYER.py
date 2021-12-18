import pygame as pg
from pygame.locals import *
from random import uniform, choice,random
from SETTINGS import *
from BULLET import *
from MAP import collide_hit_rect
from FUNCTIONS import *
from MUZZLEFLASH import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self._layer = 1
        self.type='player'
        self.name='Goose'
        self.game = game
        self.x=x
        self.y=y
        self.statCounter=0
        self.eliminated=False
        self.inDeadBox=False
        #Action stats
        self.actionStat=20
        self.totalActionPoints=self.actionStat*5
        self.actionPoints=self.totalActionPoints
        self.actionPercent=100
        self.actionRecharge=self.actionStat*3
        #Defense Stats
        self.defenseStat=10
        self.totalDefensePoints=self.defenseStat*10
        self.defensePoints=self.totalDefensePoints
        self.defensePercent=100
        self.defenseRecharge=self.defenseStat/2
        self.dodging=False
        #Movement Stat
        self.movementStat=10
        self.totalMovementPoints=self.movementStat*10
        self.movementPoints=self.totalMovementPoints
        self.movementRecharge=self.movementStat/5
        self.movementPercent=100
        self.moving=False
        self.sprinting=False
        self.speed=175
        self.step=0
        self.stepIndex=1
        self.stepRate=8
        self.speedPenalty=0
        self.resting=False
        #Enduranc Stat
        self.enduranceStat=20
        #Accuracy Stat
        self.accuracyStat=15
        #Vision Stat
        self.visionStat=15
        #Attack
        self.rateOfFire=60
        self.burstCounter=0
        self.fireMode="semi-auto"
        self.minRange=1500
        self.maxRange=3000
        self.last_shot=0
        #Stronghand/weakhand
        self.stronghandSpread=3
        self.weakhandSpread=5
        self.spread= self.stronghandSpread
        self.strongHand="RIGHT"
        self.currentHand="RIGHT"
        self.switchTimer=0
        self.offsetRighthand=vec(70, 16)
        self.offsetLefthand=vec(75, -10)
        self.offset=self.offsetRighthand
        #Ammo
        self.totalAmmoCount=250
        self.currentAmmoCount = self.totalAmmoCount
        self.ammoIndex=0
        self.ammoPercent=100
        self.reloading=False
        self.reloadImg=0
        self.reloadIndex=0
        self.reloadRate=10
        self.totalPods=6
        self.podCounter=0
        podOffset=20
        self.podPack=[]
        for i in range(self.totalPods):
            pod={'status':'full','capacity':120,'count':120,'img':2,'offset':podOffset}
            self.podPack.append(pod)
            podOffset += 25
        self.currentPod=self.podPack[0]
        #Air
        self.airIndex=0
        self.airPercent=100
        self.airVolume=1000
        self.airVolumeTotal=1000
        #Water
        self.hydroIndex=0
        self.hydroPercent=100
        self.hydroVolumeTotal=100
        self.hydroVolume=self.hydroVolumeTotal
        self.drinking=False
        self.hydroAnimationCounter=0
        self.hydroAnimationIndex=0
        self.getTube=False
        self.stowTube=False
        self.drinkSwitch=False
        #Endurance
        self.enduranceRecharge=.05
        self.enduranceIndex=0
        self.endurancePercent=100
        self.endurancePointsTotal=50
        self.endurancePoints=self.endurancePointsTotal
        #Image and position
        self.image = game.player_img_current
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.hit_rect = pg.Rect(20, 20, 40,40)
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.rotationSpeed=150
        self.inDeadBoxCounter=1

    def incrementStats(self):
      if self.endurancePoints > 10:  
        self.statCounter+=1
        if self.statCounter==self.defenseRecharge:
            if self.defensePoints<self.totalDefensePoints and self.eliminated != True:
                test=self.defensePoints+5
                if test >self.totalDefensePoints:
                    diff=test-self.totalDefensePoints
                    self.defensePoints +=5-diff
                else:
                    self.defensePoints=test
                self.percenter('defense')

        if self.statCounter==self.movementRecharge:
            if self.movementPoints<self.totalMovementPoints and self.eliminated != True and self.moving!=True:
                self.movementPoints+=15
                if self.movementPoints>self.totalMovementPoints:
                    self.movementPoints=self.totalMovementPoints
            if self.endurancePoints<self.endurancePointsTotal and self.actionPercent==100 and self.defensePercent==100 and self.moving!=True:
                self.endurancePoints+=self.enduranceRecharge
                if self.endurancePoints>self.endurancePointsTotal:
                    self.endurancePoints=self.endurancePointsTotal              
                self.percenter('endurance')
        if self.statCounter==self.actionRecharge:
                if self.actionPoints<self.totalActionPoints and self.eliminated != True:
                    test=self.actionPoints+10
                    if test >self.totalActionPoints:
                        diff=test-self.totalActionPoints
                        self.actionPoints +=10-diff
                    else:
                        self.actionPoints=test

        if self.statCounter==61:    
            self.statCounter=1

    def respawn(self):
        if self.inDeadBox==True:
            if self.game.respawnOpen == True :
                self.inDeadBoxCounter+=1
                self.currentHand="RIGHT"
                self.eliminated=False
                self.outOfAmmo=False
                self.outOfPods=False
                self.podCounter=0
                self.currentPodIndex =0 
                self.reloadIndex=0
                self.game.player_img_current =self.game.goose_eliminated_sprites[0]
                self.actionPoints=self.totalActionPoints
                self.target=self.game.player
                self.defensePoints=self.totalDefensePoints
                self.currentAmmoCount=self.totalAmmoCount
                self.hydroVolume=self.hydroVolumeTotal
                self.hydroIndex=0
                self.airVolume=self.airVolumeTotal
                self.movementPoints=self.totalMovementPoints
                for i in self.podPack:
                    i['selected']=False
                    i['status']='full'
                    i['count']=i['capacity']
                    i['img']=2
                #pod={'selected':False,'status':'full','capacity':7,'count':7,'img':0,'offset':podOffset}
                self.currentPod=self.podPack[0]
                self.currentPod['selected']=True
                
                #self.dodge()

    def SwitchHands(self):
        if self.currentHand=="LEFT":
            self.currentHand="RIGHT"
            self.offset=self.offsetRighthand
            if self.currentHand==self.strongHand:
                self.spread=self.stronghandSpread
                self.rateOfFire=60
            else:
                self.spread=self.weakhandSpread
                self.rateOfFire=140
            self.game.player_img_current=self.game.player_img_right
        elif self.currentHand=="RIGHT":
            self.currentHand="LEFT"
            self.offset=self.offsetLefthand
            if self.currentHand==self.strongHand:
                self.spread=self.stronghandSpread
                self.rateOfFire=60
            else:
                self.spread=self.weakhandSpread
                self.rateOfFire=140
            self.game.player_img_current=self.game.player_img_left

    def stepper(self):
        self.stepIndex+=1
        if self.stepIndex == self.stepRate:
            self.stepIndex=0
            self.step +=1
            if self.eliminated ==True:
                self.game.player_img_current=self.game.goose_eliminated_sprites[self.step]
            elif self.currentHand=="RIGHT":
                self.game.player_img_current=self.game.goose_right_sprites[self.step]
            elif self.currentHand=="LEFT":
                self.game.player_img_current=self.game.goose_left_sprites[self.step]
        if self.step ==4:
            self.step=1


    def hydrate(self):
        if self.drinking:
            if self.hydroVolume!=0 and self.stowTube is False and self.getTube is False:
                self.hydroVolume-=.015
                if self.hydroVolume<0:
                    self.hydroVolume=0
                self.endurancePoints+=.003
                if self.endurancePoints>self.endurancePointsTotal:
                    self.endurancePoints=self.endurancePointsTotal


    def getHydro(self):
        if self.getTube:
            self.hydroAnimationCounter+=1
            if self.hydroAnimationCounter == 10:
                self.hydroAnimationIndex+=1
                self.hydroAnimationCounter=0
                self.game.player_img_current=self.game.goose_right_hydrate_sequence[self.hydroAnimationIndex]
            if self.hydroAnimationIndex==5:
                print("STOP")
                self.drinking=True
                self.getTube=False


    def stowHydro(self):
        if self.stowTube:
            self.hydroAnimationCounter+=1
            if self.hydroAnimationCounter == 10:
                self.hydroAnimationCounter=0
                self.hydroAnimationIndex-=1
                if self.hydroAnimationIndex<0:
                    self.hydroAnimationIndex=0
                self.game.player_img_current=self.game.goose_right_hydrate_sequence[self.hydroAnimationIndex]
            if self.hydroAnimationIndex==0:
                self.drinking=False
                self.stowTube=False
                if self.currentHand=="RIGHT" and self.drinkSwitch:
                    self.drinkSwitch=False
                    self.SwitchHands()              

    def reload(self):
        if self.reloading==True and self.actionPoints>20:
            self.reloadIndex+=1
            if self.reloadIndex == self.reloadRate:
                self.reloadIndex=0
                self.reloadImg+=1
                if self.currentHand=="RIGHT":
                    self.game.player_img_current=self.game.goose_right_reload_sequence[self.reloadImg]
                elif self.currentHand=="LEFT":
                    self.game.player_img_current=self.game.goose_left_reload_sequence[self.reloadImg]
            if self.reloadImg ==20:
                self.reloadImg=0
                self.reloading=False
                self.currentAmmoCount+=self.currentPod['count']
                if self.currentAmmoCount > self.totalAmmoCount:
                    diff=self.currentAmmoCount - self.totalAmmoCount
                    self.currentAmmoCount=self.currentAmmoCount-diff
                    self.currentPod['count']=diff
                    self.currentPod['img']=1
                    self.currentPod['status']='half'
                else:
                    self.currentPod['count']=0
                    self.currentPod['img']=0
                    self.currentPod['status']='empty'
                self.actionPoints-=20
                if self.actionPoints<0:
                    self.actionPoints=0

    def setPod(self,index):
        if index <= self.totalPods and self.actionPoints>20: 
            self.currentPod=self.podPack[index]
            if self.currentPod['status']!='empty':
                if self.currentAmmoCount!=self.totalAmmoCount:
                    self.reloading=True
    def changeMode(self):
        if self.fireMode== "semi-auto":
            self.fireMode= "3 round burst"
        elif self.fireMode== "3 round burst":
            self.fireMode= "full-auto"
        elif self.fireMode== "full-auto":
            self.fireMode= "semi-auto"
    def get_keys(self):
        self.rot_speed=0 
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        self.moving=False
        self.sprinting=False
        if keys[pg.K_1]:
            self.setPod(0) 
        if keys[pg.K_2]:
            self.setPod(1) 
        if keys[pg.K_3]:
            self.setPod(2) 
        if keys[pg.K_4]:
            self.setPod(3) 
        if keys[pg.K_5]:
            self.setPod(4) 
        if keys[pg.K_6]:
            self.setPod(5) 
        if keys[pg.K_7]:
            self.setPod(6) 
        if keys[pg.K_8]:
            self.setPod(7) 
        if keys[pg.K_9]:
            self.setPod(8) 
        if keys[pg.K_0]:
            self.setPod(9)  
        if keys[pg.K_s] :
            self.sprinting=True



        if keys[MOVELEFT] :
                self.vel = vec(self.speed-50-self.speedPenalty, 0).rotate(-self.rot-90)
                self.moving=True
                self.stepper()
        if keys[MOVERIGHT] :
                self.vel = vec(self.speed-50-self.speedPenalty, 0).rotate(-self.rot+90)
                self.moving=True
                self.stepper()
        if keys[TURNLEFT] :
            self.rot_speed=self.rotationSpeed
        if keys[TURNRIGHT] :
            self.rot_speed=-self.rotationSpeed
        if keys[MOVEFORWARD] :
                self.vel = vec(self.speed-self.speedPenalty, 0).rotate(-self.rot)
                self.moving=True
                self.stepper()
        if keys[MOVEBACK] :
                self.vel = vec(-self.speed / 2-self.speedPenalty, 0).rotate(-self.rot)
                self.moving=True
                self.stepper()
        if keys[FIRE]:
            if self. fireMode == 'full-auto' or self.fireMode=="3 round burst":
                self.fire()
        

    def fire(self):
        if self.airPercent > 0 and self.actionPoints>0 and self.eliminated != True:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.rateOfFire and self.burstCounter<3:
                if self.fireMode=="3 round burst":
                    self.burstCounter+=1 
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + self.offset.rotate(-self.rot)
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)
                MuzzleFlash(self.game, pos,"flash")
                self.airVolume-=1
                if self.currentAmmoCount != 0:
                    Bullet(self.game, pos, dir,self,self.spread)
                    self.currentAmmoCount -=1
                    self.actionPoints-=1
                    if self.actionPoints<0:
                        self.actionPoints=0
                else:
                    self.game.weapon_sounds[1].play(0)


    def percenter(self,selector):
        index=0
        if selector == "air":
            current=self.airVolume
            total=self.airVolumeTotal
        if selector == "water":
            current=self.hydroVolume
            total=self.hydroVolumeTotal
        if selector == "ammo":
            current=self.currentAmmoCount
            total=self.totalAmmoCount
        if selector == "defense":
            current=self.defensePoints
            total=self.totalDefensePoints
        if selector == "action":
            current=self.actionPoints
            total=self.totalActionPoints
        if selector == "movement":
            current=self.movementPoints
            total=self.totalMovementPoints
        if selector == "endurance":
            current=self.endurancePoints
            total=self.endurancePointsTotal
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
            self.minRange=(self.minRange/100)*self.airPercent
            self.minRange=(self.maxRange/100)*self.airPercent
        if selector == "ammo":
            self.currentAmmoCount=current
            self.ammoPercent=percent
            self.ammoIndex=index  
        if selector == "water":
            self.hydroVolume=current
            self.hydroPercent=percent
            if self.hydroPercent <= 90:
                self.hydroIndex=1
            if self.hydroPercent <= 80:
                self.hydroIndex=2
            if self.hydroPercent <= 70:
                self.hydroIndex=3
            if self.hydroPercent <= 60:
                self.hydroIndex=4
            if self.hydroPercent <= 50:
                self.hydroIndex=5
            if self.hydroPercent <= 40:
                self.hydroIndex=6
            if self.hydroPercent <= 30:
                self.hydroIndex=7
            if self.hydroPercent <= 20:
                self.hydroIndex=8
            if self.hydroPercent <= 10:
                self.hydroIndex=9
            if self.hydroPercent == 0:
                self.hydroIndex=10            
 
        if selector == "defense":
            self.DefensePoints=current
            self.defensePercent=percent
            if self.defensePoints<=0:
                self.defensePoints=0
                self.image=self.game.goose_eliminated_sprites[self.step]
                self.game.player_img_current=self.game.goose_eliminated_sprites[self.step]
                if self.eliminated != True:
                    self.endurancePoints-=10
                if self.endurancePoints<0:
                    self.endurancePoints=0
                self.eliminated =True
        if selector == "action":
            self.actionPoints=current
            self.actionPercent=percent
            if self.actionPoints == 0 and self.eliminated != True:
                self.endurancePoints-=.01
                if self.endurancePoints<0:
                    self.endurancePoints=0
        if selector == "movement":
            self.movementPoints=current
            self.movementPercent=percent
            if self.movementPoints==0:
                self.resting=True
                self.movementRecharging=True
                if self.eliminated != True:
                    self.endurancePoints-=.01
                    if self.endurancePoints<0:
                        self.endurancePoints=0
            if self.movementPoints==self.totalMovementPoints:
                self.movementRecharging=False
        if selector == "endurance":
            self.endurancePoints=current
            self.endurancePercent=percent
            # if self.endurancePoints==0:
            #     self.resting=True
            #     self.movementRecharging=True
            # if self.movementPoints==self.totalMovementPoints:
            #     self.movementRecharging=False

    def dodge(self):
        self.dodging=True
        self.moving=True
        counter=0
        if self.movementPoints >=10:
            self.movementPoints-=10
        else:
            self.movementPoints=0
        self.percenter('defense')

        while self.dodging==True:
            counter+=1
            if counter % 2 ==0:
                adjustRot=choice([90,-90,45,-45,140,-140])
                self.stepper()
                self.vel = vec(self.speed*4, 0).rotate(-self.rot+adjustRot)
                self.makeMove()
            if counter == 60:
                counter=0
                self.dodging=False

    def update(self):
        self.percenter('air')
        self.percenter('action')
        self.percenter('ammo')
        self.percenter('water')
        self.percenter('movement')
        self.percenter('defense')
        self.percenter('endurance')
        self.incrementStats()
        if not self.eliminated:
            self.get_keys()
            self.reload()
            self.hydrate()
            self.getHydro()
            self.stowHydro()
            self.makeMove()
            #print (self.getTube)
        else:
            self.get_keys()
            self.makeMove()
            self.respawn()


        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotozoom(self.game.player_img_current, self.rot,1)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if not self.moving and not self.reloading and not self.getTube and not self.stowTube and not self.drinking:
            if self.currentHand=="RIGHT":
                self.game.player_img_current=self.game.goose_right_sprites[0]
            elif self.currentHand=="LEFT":
                self.game.player_img_current=self.game.goose_left_sprites[0]
    def makeMove(self):
        if self.moving ==True:
            self.inDeadBox=False
            self.speedPenalty=0
            movedrain=.1
            if self.sprinting == True:
                self.speedPenalty= -100
                movedrain=.5
                self.actionPoints-=.5
                if self.actionPoints <0:
                    self.actionPoints=0
                if self.defensePoints>1:
                    self.defensePoints-=.5
            self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
            self.image = pg.transform.rotozoom(self.game.player_img_current, self.rot,1)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.pos += self.vel * self.game.dt
            self.x=self.pos[0]
            self.y=self.pos[1]
            self.hit_rect.centerx = self.pos.x+5
            collide_with_walls(self, self.game.walls, 'x')
            collide_with_walls(self, self.game.stoppers, 'x')
            self.hit_rect.centery = self.pos.y+5
            collide_with_walls(self, self.game.walls, 'y')
            collide_with_walls(self, self.game.stoppers, 'y')
            self.rect.center = self.hit_rect.center
            self.movementPoints-=movedrain     
            if self.movementPoints<10:
                self.speedPenalty=50
                self.sprinting=False
            if self.movementPoints<=0:
                self.movementPoints=0
                self.moving=False
            if self.eliminated==True:
                self.endurancePoints -= .005
                if self.endurancePoints<0:
                    self.endurancePoints=0
            self.percenter('movement')

    def printStats(self,a,b,c,d,e,f):
        surface=self.game.screen
        surface.blit(self.game.hopper_sprites[self.ammoIndex], (15, 10))
        text_surface, rect = self.game.gameFont.render(str(self.currentAmmoCount), (20, 20, 0))
        surface.blit(text_surface, (55, 13))
        surface.blit(self.game.air_sprites[self.airIndex], (100, 5))
        airtext_surface, rect = self.game.gameFont.render(str(self.airPercent)+"%", (20, 20, 0))
        surface.blit(airtext_surface, (120, 13))
        for i in self.podPack:
            surface.blit(self.game.pod_sprites[i['img']], (i['offset'], 50))

        surface.blit(self.game.hydro_sprites[self.hydroIndex], (170, 7))
        hydrotext_surface, rect = self.game.gameFont.render(str(self.hydroPercent)+"%", (20, 20, 0))
        surface.blit(hydrotext_surface, (195, 13))

        defenseWidth = int(90* self.defensePoints / self.totalDefensePoints)
        self.defense_bar = pg.Rect(70, 110, defenseWidth, 7)
        pg.draw.rect(surface, BLUE, self.defense_bar)
        self.dodge_surface, textblock = self.game.gameFont.render(str(a)+"%", BLUE)
        surface.blit(self.dodge_surface, (20, 105))
        actionWidth = int(90* self.actionPoints / self.totalActionPoints)
        self.action_bar = pg.Rect(70, 130, actionWidth, 7)
        pg.draw.rect(surface, RED, self.action_bar)
        self.action_surface, textblock = self.game.gameFont.render(str(b)+"%", RED)
        surface.blit(self.action_surface, (20, 125))
        movementWidth = int(90* self.movementPoints / self.totalMovementPoints)
        self.movement_bar = pg.Rect(70, 150, movementWidth, 7)
        pg.draw.rect(surface, YELLOW, self.movement_bar)
        self.movement_surface, textblock = self.game.gameFont.render(str(c)+"%", YELLOW)
        surface.blit(self.movement_surface, (20, 145))
 
        enduranceWidth = int(90* self.endurancePoints / self.endurancePointsTotal)
        self.endurance_bar = pg.Rect(70, 170, enduranceWidth, 7)
        pg.draw.rect(surface, GREEN, self.endurance_bar)
        self.endurance_surface, textblock = self.game.gameFont.render(str(e)+"%", GREEN)
        surface.blit(self.endurance_surface, (20, 165))


        self.fireMode_surface, textblock = self.game.gameFont.render('MODE OF FIRE : '+str(d), RED)
        surface.blit(self.fireMode_surface, (250, 13))

        # self.nameplate, textblock = self.game.gameFont.render(str(f), BLACK)
        # surface.blit(self.nameplate, self.pos)
