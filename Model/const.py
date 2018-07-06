from pygame.math import Vector2 as Vec
import View.const as viewconst
from math import sqrt, ceil
PlayerNum = 4
MaxManualPlayerNum = 4

#dir const
dirConst = [
    [0,0],              # can't movw
    [0,-1],             # Up
    [0.707,-0.707],     # Right up
    [1,0],              # Right
    [0.707,0.707],      # Right down
    [0,1],              # Down
    [-0.707,0.707],     # Left down
    [-1,0],             # Left
    [-0.707,-0.707]     # Left up
]
dirBounce = [
    [0, 1, 8, 7, 6, 5, 4, 3, 2], # x bouce
    [0, 5, 4, 3, 2, 1, 8, 7, 6], # y bouce
]

eps=1e-7


#####################  Vec direction #####################
Vec_dir = [
    Vec( 0,1 ), ##left
    Vec( 1,0 ), ##up
    Vec( 0,-1 ),  ##right
    Vec( -1,0 )   ##down
]

#####################  white ball const  #####################
wb_init_num = 30
wb_max_num  = 50
wb_born_period = 1 #second
wb_radius   = 10
#####################  white ball const  #####################


def init_grav_list(g_list):
    grav_st=120
    grav_r = 75
    grav_dr=(800-grav_st*2)/4
    for i in range(5):
        if i % 2 == 0:
            for j in range(3):
                g_list[0].append([Vec(grav_st+grav_dr*2*j,grav_st+grav_dr*i), grav_r])
        else:
            for j in range(2):
                g_list[0].append([Vec(grav_st + grav_dr + grav_dr * 2 * j, 0.5+grav_st+grav_dr*i), grav_r])
    # grav = [(Vec(160,160),50),(Vec(320,160),50),(Vec(480,160),50),\
    # (Vec(640,160),50),(Vec(200,400),50),(Vec(200,600),50),(Vec(200,800),50)]

    grav_r=55
    grav_circle_num=int(viewconst.GameSize[0] / sqrt(2) / grav_r - sqrt(2) + 1)
    shift_size=int((viewconst.GameSize[0]-2*grav_r)/(grav_circle_num-1))
    for i in range(grav_circle_num):
        g_list[1].append([Vec(viewconst.GameSize[0] - grav_r - (shift_size*i), grav_r + (shift_size*i)),grav_r])

def next_grav():
    '''change the gravity map cyclicly'''
    global grav
    grav = grav_list[next_grav.counter%len(grav_list)]
    next_grav.counter += 1
next_grav.counter = 0



#####################     head const     #####################


max_dash_time = 50

normal_speed = 2
#dash_speed = normal_speed * 3
dash_speed_multiplier = 3
dash_speed = normal_speed * dash_speed_multiplier
pos_log_max = 25 / normal_speed + 1
init_r = 40
init_no_wb_r = 80
head_radius = 11
#the grav now is for debug
grav_list = [ [] for _ in range(5) ]

grav = grav_list[0]
init_grav_list(grav_list)


init_r=40
#####################     head const     #####################

#####################    body const    ######################
body_radius = 10
body_gap = 6
dash_radius = head_radius + body_radius
#####################    body const    ######################

#####################  bullet const  #####################
bullet_radius = 8
bullet_a = 0.1
bullet_speed0 = normal_speed * 7

suddendeath_ticks = viewconst.FramePerSec * 20
suddendeath_speed = normal_speed
freq = 7
#####################  bullet const  #####################

#####################  item const #####################

PROP_TYPE_EXPLOSIVE = 0
PROP_TYPE_MULTIBULLET = 1
PROP_TYPE_BIGBULLET = 2
item_max = 10
item_born_period = 1#second
item_init_num = 0
item_radius = 12

explosive_radius = 150.0

bigbullet_r = bullet_radius * 4


#####################  item const #####################

wb_speed = normal_speed * 1.5
wb_fast_speed = dash_speed * 1.5



