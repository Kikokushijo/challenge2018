import Model.const as modelconst
import View.const as viewconst
import random
from math import pi, sin, cos
from pygame.math import Vector2 as Vec
class Body(object):
	def __init__(self, pre):
		self.pre = pre
		self.index = pre.index
		self.color = pre.color
		#問題：牆不往內縮可能會生成在外面
		self.radius = modelconst.body_radius
		self.pos = Vec(pre.pos_log[0])
		#try:
		#	self.pos = pre.pos - pre.direction * (pre.radius + modelconst.body_radius + modelconst.body_gap)
		#except:
		#	self.pos = pre.pos - (pre.pre.pos - pre.pos).normalize() * (pre.radius + modelconst.body_radius + modelconst.body_gap)
		self.pos_log = [Vec(self.pos)]
	def update(self):
		self.pos = Vec(self.pre.pos_log[0])
		self.pos_log.append(Vec(self.pos))
		if len(self.pos_log) > modelconst.pos_log_max:
			self.pos_log.pop(0)
