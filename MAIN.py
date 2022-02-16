import pygame as pg
import pygame.freetype
import sys
from datetime import datetime
from os import path
from CAMERA import *
from random import uniform, choice,random
from MAP import *
from SETTINGS import *
from FUNCTIONS import *
from MUZZLEFLASH import *
from CAST import *
from BULLET import *
from MOB import *
from PLAYER import *
from WALL import *
from ITEM import *

vec = pg.math.Vector2


class Game:
    def __init__(self,mainmenu):
        pg.init()
        self.mainmenu=mainmenu
    
        self.playing = True
        self.running=True
        self.go=True
        self.now=None
        self.seconds=None
        self.lastSecond=None
        self.timeZone="MST"
        pg.mixer.set_num_channels(10)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        self.respawnOpen=False
        self.respawnCounter=0
        self.respawnIndex=60
        self.respawnTime=60
        self.respawnOpenCounter=10
        self.respawnClosedCounter=20
        self.mobRespawn=None
        self.playerRespawn=None
        self.respawnText=""
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.img_folder=img_folder
        goose_folder = path.join(img_folder, 'Goose')
        mob_folder = path.join(img_folder, 'mobs')
        sfx_folder = path.join(game_folder, 'sfx')
        music_folder = path.join(game_folder, 'music')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'sandbox.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img_right = pg.image.load(path.join(goose_folder, PLAYER_IMG_RIGHT)).convert_alpha()
        self.player_img_left = pg.image.load(path.join(goose_folder, PLAYER_IMG_LEFT)).convert_alpha()
        self.player_img_current =self.player_img_right
        self.mob_stat_img = pg.image.load(path.join(img_folder, STAT_BUBBLE_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.clear_img=pg.image.load(path.join(img_folder, CAST_IMG)).convert_alpha()
        self.eliminated_icon=pg.image.load(path.join(img_folder, MOB_ELIMINATED_ICON)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_eliminated_img = pg.image.load(path.join(mob_folder, MOB_ELIMINATED_RIGHT)).convert_alpha()
        self.gameFont = pygame.freetype.Font("fonts/digital-7.ttf", 26)
        # self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        # self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.gun_flashes = []
        self.tipxMag_sprites = []
        self.tipxMag_selected_sprites = []
        self.mob_images=[]
        self.paint_splats = []
        self.pod_sprites=[]
        self.air_sprites=[]
        self.hopper_sprites=[]
        self.hydro_sprites=[]
        self.co2_sprites=[]
        self.goose_right_sprites=[]
        self.goose_eliminated_sprites=[]
        self.goose_left_sprites=[]
        self.goose_right_reload_sequence=[]
        self.goose_left_reload_sequence=[]
        self.goose_right_hydrate_sequence=[]
        self.mob_right_reload_sequence=[]
        self.mob_right_air_reload_sequence=[]
        self.mob_left_reload_sequence=[]
        self.item_images = {}
        for img in MAG_SELECTED_IMAGES:
            self.tipxMag_selected_sprites.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for img in MAG_IMAGES:
            self.tipxMag_sprites.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for img in HOPPER_IMAGES:
            self.hopper_sprites.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for img in HYDRO_IMAGES:
            self.hydro_sprites.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for img in CO2_IMAGES:
            self.co2_sprites.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for img in AIR_IMAGES:
            self.air_sprites.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for img in POD_IMAGES:
            self.pod_sprites.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for img in GOOSE_RIGHT_RELOAD_SEQUENCE:
            self.goose_right_reload_sequence.append(pg.image.load(path.join(goose_folder, img)).convert_alpha())
        for img in GOOSE_HYDRATE_RIGHT_IMAGES:
            self.goose_right_hydrate_sequence.append(pg.image.load(path.join(goose_folder, img)).convert_alpha())
        for img in GOOSE_LEFT_RELOAD_SEQUENCE:
            self.goose_left_reload_sequence.append(pg.image.load(path.join(goose_folder, img)).convert_alpha())
        for img in MOB_RIGHT_RELOAD_SEQUENCE:
            self.mob_right_reload_sequence.append(pg.image.load(path.join(mob_folder, img)).convert_alpha())
        for img in MOB_RIGHT_AIR_RELOAD_SEQUENCE:
            self.mob_right_air_reload_sequence.append(pg.image.load(path.join(mob_folder, img)).convert_alpha())
        for img in GOOSE_ELIMINATED_SPRITES:
            self.goose_eliminated_sprites.append(pg.image.load(path.join(goose_folder, img)).convert_alpha())  
                
        for img in GOOSE_RIGHT_SPRITES:
            self.goose_right_sprites.append(pg.image.load(path.join(goose_folder, img)).convert_alpha())  
        for img in GOOSE_LEFT_SPRITES:
            self.goose_left_sprites.append(pg.image.load(path.join(goose_folder, img)).convert_alpha())       
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for img in PAINT_SPLATS:
            self.paint_splats.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        self.weapon_sounds = []
        for snd in WEAPON_SOUNDS:
            sfx=pg.mixer.Sound(path.join(sfx_folder, snd))
            sfx.set_volume(0.08)
            self.weapon_sounds.append(sfx)
        self.splatSounds=[]
        for snd in SPLAT_SOUNDS:
            sfx=pg.mixer.Sound(path.join(sfx_folder, snd))
            sfx.set_volume(0.11)
            self.splatSounds.append(sfx)
            #self.splatSound.set_volume(0.1) 
        # self.splatSound =pg.mixer.Sound(path.join(sfx_folder, SPLAT_SOUNDS[0]))
        # self.splatSound.set_volume(0.1) 
        # self.zombie_moan_sounds = []
        # for snd in ZOMBIE_MOAN_SOUNDS:
        #     s = pg.mixer.Sound(path.join(sfx_folder, snd))
        #     s.set_volume(0.2)
        #     self.zombie_moan_sounds.append(s)
        # self.player_hit_sounds = []
        # for snd in PLAYER_HIT_SOUNDS:
        #     self.player_hit_sounds.append(pg.mixer.Sound(path.join(sfx_folder, snd)))
        # self.zombie_hit_sounds = []
        # for snd in ZOMBIE_HIT_SOUNDS:
        #     self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(sfx_folder, snd)))
    
    
    
    
    def respawnTimer(self):
        if self.seconds != self.lastSecond:
            self.respawnCounter+=1
            # if self.respawnCounter==self.respawnIndex:
            #     self.respawnCounter=0
            #     self.respawnTime-=1
            if self.respawnOpen==True:
                    self.respawnOpenCounter-=1
                    self.respawnText="RESPAWN OPEN FOR: %s"%(self.respawnOpenCounter)
                    if self.respawnOpenCounter == 0:
                        self.respawnOpen=False
                        self.respawnOpenCounter=10 

            if self.respawnOpen==False:
                    self.respawnClosedCounter-=1
                    self.respawnText="RESPAWN OPEN IN: %s"%(self.respawnClosedCounter)
                    if self.respawnClosedCounter == 0:
                        self.respawnOpen=True
                        self.respawnClosedCounter=20    
        # if self.respawnTime == 0:
        #         self.respawnTime = 60
    



            
            


    def new(self):
        counter=0
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.stoppers = pg.sprite.Group()
        self.respawns = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.playerBullets = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.items=pg.sprite.Group()
        self.pods=pg.sprite.Group()
        self.mobStats=pg.sprite.Group()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,tile_object.y + tile_object.height / 2)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height,"wall")
            if tile_object.name == 'mobRespawn':
                    Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height,"mobRespawn")
                    self.mobRespawn =Item(self, obj_center, tile_object.name)
                    self.mobRespawn.type="mobRespawn"


            if tile_object.name == 'PlayerRespawn':
                    Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height,"playerRespawn")
                    self.playerRespawn =Item(self, obj_center, tile_object.name)
                    self.playerRespawn.type="playerRespawn"

            if tile_object.name == 'stopper':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height,"stopper")
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)

            if tile_object.name == 'mob':
                self.mob_images.append(self.mob_img)
                Mob(self, counter,tile_object.x, tile_object.y)
                
                counter +=1
            if tile_object.name in ['mobRespawn']:
                    Item(self, obj_center, tile_object.name)   
            if tile_object.name in ['playerRespawn']:
                    Item(self, obj_center, tile_object.name) 
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
                         
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        #pg.mixer.music.play(loops=-1)
        while self.playing:
            self.now =datetime.now()
            self.seconds=self.now.strftime("%S")
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()
            self.respawnTimer()
            self.lastSecond = self.seconds

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop

        self.all_sprites.update()
        self.camera.update(self.player)
        
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < self.player.totalHealth:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT) 
            if hit.type == 'playerRespawn':
                if self.respawnOpen:
                    self.player.inDeadBox=True


        hits = pg.sprite.spritecollide(self.player, self.bullets, False, collide_hit_rect)
        for hit in hits:
            if self.player.eliminated:
                self.player.endurancePoints-=10
                if self.player.endurancePoints<0:
                    self.player.endurancePoints=0
            self.player.defensePoints -= hit.shooter.accuracy
            self.player.actionPoints-=15
            if self.player.actionPoints <0:
                    self.player.actionPoints =0
            if self.player.defensePoints <0:
                self.player.defensePoints=0
                # hit.shooter.target=self.mobRespawn
                MuzzleFlash(self, self.player.pos,"splat")
                choice(self.splatSounds).play(0)
            else:
                pass
                #self.player.dodge()
        if hits:
            hits[0].kill()

        for i in self.mobs:    
            hits = pg.sprite.spritecollide(i, self.items, False)
            for hit in hits:
                if hit.type == 'mobRespawn':
                    if self.respawnOpen:
                        i.inDeadBox=True

        hits = pg.sprite.groupcollide(self.mobs, self.playerBullets,False,True)
        for hit in hits:
            hit.defense -= BULLET_DAMAGE
            if hit.actionPoints >5:
                hit.actionPoints -=5
            else:
                hit.actionPoints=0
            if hit.defense <10:
                MuzzleFlash(self, hit.pos,"splat")
                choice(self.splatSounds).play(0)
            #hit.vel = vec(0, 0)
            hit.dodge()




    #    hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
    #     for hit in hits:
    #         self.player.health -= MOB_DAMAGE
    #         hit.vel = vec(0, 0)
    #         if self.player.health <= 0:
    #             self.playing = False
    #     if hits:
    #         self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

    #     bullets hit mobs 
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))


    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if isinstance(sprite,Mob):
                self.mob_stat_img = pg.image.load(path.join(self.img_folder, STAT_BUBBLE_IMG)).convert_alpha()
                sprite.statBar.image=self.mob_stat_img
                sprite.printStats(sprite.currentPod['count'],sprite.airPercent,sprite.cartridges,sprite.defensePercent,sprite.actionPercent,sprite.movementPercent)
        
        clock_string = self.now.strftime("%H:%M:%S")
        self.clock_surface, textblock = self.gameFont.render( clock_string +' '+self.timeZone , BLACK)
        self.respawn_surface, textblock = self.gameFont.render(str(self.respawnText), BLACK)
        self.difficulty_surface, textblock = self.gameFont.render(str("DIFFICULTY : "+self.mainmenu.difficulty), self.mainmenu.difficultyColor)
        self.screen.blit(self.clock_surface, (825, 13))
        self.screen.blit(self.difficulty_surface, (550, 13))
        self.screen.blit(self.respawn_surface, (1000, 13))
        # HUD functions
        self.player.printStats(self.player.defensePercent,self.player.actionPercent,self.player.movementPercent,self.player.fireMode,self.player.endurancePercent,self.player.name)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.burstCounter=0

                if event.key==HYDRATE:
                    self.player.stowTube=True

            if event.type == pygame.VIDEORESIZE:
                 surface = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)

            elif event.type == pygame.MOUSEMOTION:
                self.player.rotate()


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()
                    self.mainMenu.gameGo=False
                    print(self.mainMenu.gameGo)
                if event.key==HYDRATE:
                    self.player.getTube=True
                    if self.player.currentHand=="LEFT":
                        self.player.drinkSwitch=True
                        self.player.SwitchHands()
                if event.key == pg.K_m:
                    self.player.changeMode()
                if event.key == pg.K_LALT:
                    self.player.SwitchHands()
                if event.key == pg.K_SPACE:
                    if self.player.fireMode=="semi-auto":
                        self.player.fire()



# g = Game()
# while g.go == True:
#     g.new()
#     g.run()
