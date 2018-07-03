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
    Vec( -1,0 ), ##left
    Vec( 0,-1 ), ##up
    Vec( 1,0 ),  ##right
    Vec( 0,1 )   ##down
]

grav = []


#####################  bullet const  #####################
bullet_r = 1
bullet_a = 0.1
bullet_speed0 = 0.5
#####################  bullet const  #####################


#####################  white ball const  #####################
wb_init_num = 10
wb_max_num  = 50
wb_born_period= 1 #second
wb_radius   = 4
#####################  white ball const  #####################


#####################     head const     #####################


max_dash_time = 100
dash_speed = 0.5
normal_speed = 0.25
direction_log_max = 120
init_r=20
head_radius=10
#the grav now is for debug
grav=[(Vec(200,200),50),(Vec(400,200),50),(Vec(600,200),50),\
(Vec(800,200),50),(Vec(200,400),50),(Vec(200,600),50),(Vec(200,800),50)]

init_r=40
head_radius = 10
dt=1/viewconst.FramePerSecond
#####################     head const     #####################

#####################    body const    ######################
body_radius=10
body_gap=3
#####################    body const    ######################

#####################  item const #####################

PROP_TYPE_EXPLOSION = 0
explosion_radius = 500.0

#####################  item const #####################


