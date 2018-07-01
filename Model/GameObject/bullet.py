import Model.const as modelConst
import View.const as viewConst
from white_ball import White_Ball
class Bullet(object):
	def __init__(self, pos,direction,index):
		self.pos=pos
		self.direction=direction
		self.index = index
		self.speed=modelConst.bullet_speed0
	def update(self, wblist):
		'''
		return:
			True: update success
			False: update failed
		'''
		if (self.direction.x > 0 and self.pos.x >= viewConst.ScreenSize[0] - modelConst.eps) \
			or (self.direction.x < 0 and self.pos.x <= 0 - modelConst.eps):
			self.direction.x *= -1
		if (self.direction.y > 0 and self.pos.y >= viewConst.ScreenSize[1] - modelConst.eps) \
			or (self.direction.y < 0 and self.pos.y <= 0 - modelConst.eps):
			self.direction.y *= -1
		self.pos += self.direction * self.speed
		self.speed -= modelConst.bullet_a
		if self.speed <= modelConst.eps:
			wblist.append(White_Ball())
			return False
		return True
    
		