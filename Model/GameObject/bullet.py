import Model.const as modelConst
class Bullet(object):
	def __init__(self, pos,dir,id):
		self.pos=pos
		self.dir=dir
		self.id = id
        self.radius = modelConst.bullet_r
	def update():
		self.pos += pos * modelConst.bullet_v
    
		