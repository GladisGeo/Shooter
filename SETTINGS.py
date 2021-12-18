
import pygame as pg
vec = pg.math.Vector2
from random import uniform,randint
# define some colors (R, G, B)
DIFFICULTY = "EASY"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (20, 20, 200)
YELLOW = (255, 255, 0)
LIGHTGREEN = (226,227,219)
PURPLE=(138,43,226)

##________________________CONTROLS____________________________________
MOVEFORWARD =pg.K_UP
MOVEBACK = pg.K_DOWN
MOVELEFT = pg.K_a
MOVERIGHT = pg.K_d
TURNLEFT= pg.K_LEFT
TURNRIGHT = pg.K_RIGHT
SPRINT = pg.K_s
SWAPHANDS = pg.K_LALT
FIRE = pg.K_SPACE
CHANGEMODE=pg.K_m
HYDRATE=pg.K_h


##________________________DISPLAY_____________________________________
# game settings
WIDTH = 1275   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 660  # 16 * 48 or 32 * 24 or 64 * 12 # 16 * 48 or 32 * 24 or 64 * 126656
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = LIGHTGREEN
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
PLAYER_IMG_RIGHT='GooseRight0.png'
PLAYER_IMG_LEFT='GooseLeft0.png'
PISTOL_OFFSET = vec(60, 10)
# Gun settings
BULLET_IMG = 'paintball.png'
CAST_IMG = 'clearImg.png'

ENEMY_FIRE_RATE=160
BULLET_DAMAGE=10
KICKBACK = 0
OFFHAND_SPREAD = 6
#MOB SETTINGS
MOB_IMG = 'easyMob.png'
MOB_HIT_RECT = pg.Rect(1, 1, 35, 35)

MOB_KNOCKBACK=2
# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
PAINT_SPLATS = ['splat1.png', 'splat2.png', 'splat3.png',
                  'splat4.png']
GOOSE_ELIMINATED_SPRITES = ['GooseEliminated0.png', 'GooseEliminated1.png', 'GooseEliminated2.png',
                  'GooseEliminated3.png','GooseEliminated4.png']
GOOSE_RIGHT_SPRITES = ['GooseRight0.png', 'GooseRight1.png', 'GooseRight2.png',
                  'GooseRight3.png','GooseRight4.png']
GOOSE_LEFT_SPRITES = ['GooseLeft0.png', 'GooseLeft1.png', 'GooseLeft2.png',
                  'GooseLeft3.png','GooseLeft4.png']
GOOSE_RIGHT_RELOAD_SEQUENCE = ['GooseRightReload0.png', 
'GooseRightReload1.png', 'GooseRightReload2.png','GooseRightReload3.png','GooseRightReload4.png','GooseRightReload5.png',
'GooseRightReload6.png', 'GooseRightReload7.png','GooseRightReload8.png','GooseRightReload9.png','GooseRightReload10.png',
'GooseRightReload11.png', 'GooseRightReload12.png','GooseRightReload13.png','GooseRightReload14.png','GooseRightReload15.png',
'GooseRightReload16.png', 'GooseRightReload17.png','GooseRightReload18.png','GooseRightReload19.png','GooseRightReload20.png']
STAT_BUBBLE_IMG = 'mobStatBubble.png'

GOOSE_LEFT_RELOAD_SEQUENCE = ['GooseLeftReload0.png', 
'GooseLeftReload1.png', 'GooseLeftReload2.png','GooseLeftReload3.png','GooseLeftReload4.png','GooseLeftReload5.png',
'GooseLeftReload6.png', 'GooseLeftReload7.png','GooseLeftReload8.png','GooseLeftReload9.png','GooseLeftReload10.png',
'GooseLeftReload11.png', 'GooseLeftReload12.png','GooseLeftReload13.png','GooseLeftReload14.png','GooseLeftReload15.png',
'GooseLeftReload16.png', 'GooseLeftReload17.png','GooseLeftReload18.png','GooseLeftReload19.png','GooseLeftReload20.png']

MOB_RIGHT_AIR_RELOAD_SEQUENCE = ['mobRightAirReload0.png', 
'mobRightAirReload1.png', 'mobRightAirReload2.png','mobRightAirReload3.png','mobRightAirReload4.png','mobRightAirReload5.png',
'mobRightAirReload6.png', 'mobRightAirReload7.png','mobRightAirReload8.png','mobRightReload9.png','mobRightAirReload10.png',
'mobRightAirReload11.png', 'mobRightAirReload12.png','mobRightAirReload13.png','mobRightAirReload14.png','mobRightAirReload15.png']

MOB_RIGHT_RELOAD_SEQUENCE = ['mobRightReload0.png', 
'mobRightReload1.png', 'mobRightReload2.png','mobRightReload3.png','mobRightReload4.png','mobRightReload5.png',
'mobRightReload6.png', 'mobRightReload7.png','mobRightReload8.png','mobRightReload9.png','mobRightReload10.png',
'mobRightReload11.png', 'mobRightReload12.png','mobRightReload13.png','mobRightReload14.png']

MOB_LEFT_RELOAD_SEQUENCE = ['GooseLeftReload0.png', 
'mobLeftReload1.png', 'mobLeftReload2.png','mobLeftReload3.png','mobLeftReload4.png','mobLeftReload5.png',
'mobLeftReload6.png', 'mobLeftReload7.png','mobLeftReload8.png','mobLeftReload9.png','mobLeftReload10.png',
'mobLeftReload11.png', 'mobLeftReload12.png','mobLeftReload13.png','mobLeftReload14.png']


MAG_IMAGES=['tipxMag0.png','tipxMag0.png','tipxMag1.png','tipxMag2.png','tipxMag3.png','tipxMag4.png','tipxMag5.png','tipxMag6.png']
MAG_SELECTED_IMAGES=['tipxMagSelected0.png','tipxMagSelected0.png','tipxMagSelected1.png','tipxMagSelected2.png','tipxMagSelected3.png','tipxMagSelected4.png','tipxMagSelected5.png','tipxMagSelected6.png']

POD_IMAGES=['emptyPod.png','halfPod.png','fullPod.png']
CO2_IMAGES=['CO20.png','CO21.png','CO22.png','CO23.png',
'CO24.png','CO25.png','CO26.png','CO27.png',]
AIR_IMAGES=['airTank0.png','airTank1.png','airTank2.png','airTank3.png',
'airTank4.png','airTank5.png','airTank6.png','airTank7.png',]
HOPPER_IMAGES=['hopper0.png','hopper1.png','hopper2.png','hopper3.png',
'hopper4.png','hopper5.png','hopper6.png','hopper7.png',]
GOOSE_HYDRATE_RIGHT_IMAGES=['hydrateRight0.png','hydrateRight1.png','hydrateRight2.png','hydrateRight3.png',
'hydrateRight4.png','hydrateRight5.png']
HYDRO_IMAGES=['hydroBladder0.png','hydroBladder1.png','hydroBladder2.png','hydroBladder3.png',
'hydroBladder4.png','hydroBladder5.png','hydroBladder6.png','hydroBladder7.png','hydroBladder8.png','hydroBladder9.png','hydroBladder10.png']

MOB_ELIMINATED_RIGHT="mobRightEliminatedStanding.png"
MOB_ELIMINATED_ICON="eliminated.png"
ITEM_IMAGES = {'health': 'medpack.png','mobRespawn':'greenEliminated.png','playerRespawn':'maroonEliminated.png'}
HEALTH_PACK_AMOUNT = 20

WEAPON_SOUNDS= ['shot.wav','tipx.wav']
EFFECTS_SOUNDS = {}
SPLAT_SOUNDS=['splat1.wav','splat2.wav','splat3.wav']