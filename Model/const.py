from pygame.math import Vector2 as Vec
import View.const as viewconst
PlayerNum = 4
MaxManualPlayerNum = 1

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

grav = []


#####################  bullet const  #####################
bullet_r = 1
bullet_a = 0.1
bullet_speed0 = 0.5
#####################  bullet const  #####################


#####################  white ball const  #####################
wb_init_num = 100
wb_max_num  = 150
wb_born_period = 1 #second
wb_radius   = 10
#####################  white ball const  #####################


#####################     head const     #####################


max_dash_time = 100
normal_speed = 1.0
dash_speed = normal_speed * 2
pos_log_max = 20
init_r = 40
head_radius = 15
#the grav now is for debug
grav = [(Vec(200,200),50),(Vec(400,200),50),(Vec(600,200),50),\
(Vec(800,200),50),(Vec(200,400),50),(Vec(200,600),50),(Vec(200,800),50)]

init_r=40
head_radius = 10
dt=1/viewconst.FramePerSec
#####################     head const     #####################

#####################    body const    ######################
body_radius = head_radius
body_gap = 6
#####################    body const    ######################

#####################  item const #####################

PROP_TYPE_EXPLOSION = 0
explosion_radius = 500.0

#####################  item const #####################


