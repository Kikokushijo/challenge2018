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
		self.pos = pre.pos - pre.direction * (pre.radius + modelconst.body_radius + modelconst.body_gap)
		self.direction = pre.direction_log[0]
		self.direction_log = [self.direction]
		self.speed = pre.speed
	def update(self):
		self.pos += self.speed * self.direction
		self.direction = self.pre.direction_log[0]
		self.direction_log.append(self.direction)
		if len(self.direction_log) > modelconst.direction_log_max:
			self.direction_log.pop(0)
		self.speed = self.pre.speed
