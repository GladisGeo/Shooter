import pygame as pg
import sys
from random import choice, random
from os import path
from settings import *
from sprites import *
from tilemap import *
# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.set_num_channels(10)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        sfx_folder = path.join(game_folder, 'sfx')
        music_folder = path.join(game_folder, 'music')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'sandbox.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img_switch = pg.image.load(path.join(img_folder, PLAYER_IMG_SWITCH)).convert_alpha()
        self.player_img_current =self.player_img
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.clear_img=pg.image.load(path.join(img_folder, CAST_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.gun_flashes = []
        self.paint_splats = []
        self.item_images = {}
        
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for img in PAINT_SPLATS:
            self.paint_splats.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        #pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        # self.effects_sounds = {}
        # for type in EFFECTS_SOUNDS:
        #     self.effects_sounds[type] = pg.mixer.Sound(path.join(sfx_folder, EFFECTS_SOUNDS[type]))

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
    
    
    
    
    
    def new(self):
        # initialize all variables and do all the setup for a new game


        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.stoppers = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.items=pg.sprite.Group()
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
            if tile_object.name == 'stopper':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height,"stopper")
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)

            if tile_object.name == 'mob':
                Mob(self, tile_object.x, tile_object.y)
                
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
                         
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        #pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

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
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT) 


        hits = pg.sprite.spritecollide(self.player, self.bullets, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            MuzzleFlash(self,hits[0].pos,"splat")
            hits[0].kill()
        # hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        # for hit in hits:
        #     self.player.health -= MOB_DAMAGE
        #     hit.vel = vec(0, 0)
        #     if self.player.health <= 0:
        #         self.playing = False
        # if hits:
        #     self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # bullets hit mobs 
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            #hit.vel = vec(0, 0)
            hit.dodge()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))


    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
 
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_LALT:
                    print(self.player_img_switch)
                    self.player.Switch()
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()