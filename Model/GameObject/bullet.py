import Model.const as modelConst
class Bullet(object):
	def __init__(self, pos,direction,index):
		self.pos=pos
		self.dir=direction
		self.id = index
		self.radius = modelConst.bullet_r
	def update(self):
		self.pos += self.pos * modelConst.bullet_v
    
		