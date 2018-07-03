import Model.const as modelConst
import View.const as viewConst
class Bullet(object):
    def __init__(self, pos,direction,index):
        self.pos = pos
        self.color = viewConst.playerColor[index]
        self.direction = direction
        self.index = index
        self.radius = modelConst.bullet_r
        self.speed = modelConst.bullet_speed0
    def update(self):
        '''
        return:
            True: update success
            False: update failed
        '''

        ########## collide with walls ###########
        if (self.direction.x > 0 and self.pos.x+self.radius >= viewConst.ScreenSize[0] - modelConst.eps) \
            or (self.direction.x < 0 and self.pos.x-self.radius <= -modelConst.eps):
            self.direction.x *= -1
        if (self.direction.y > 0 and self.pos.y+self.radius >= viewConst.ScreenSize[1] - modelConst.eps) \
            or (self.direction.y < 0 and self.pos.y-self.radius <= -modelConst.eps):
            self.direction.y *= -1
        
        self.pos += self.direction * self.speed
        self.speed -= modelConst.bullet_a
        
        return self.speed > 0
    
