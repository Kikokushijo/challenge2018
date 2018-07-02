import Model.const as modelconst
import View.const as viewconst
import random
from math import pi, sin, cos
from pygame.math import Vector2 as Vec
class Body(object):
	def __init__(self, pre):
		self.pre = pre
		self.index = pre.index
		#問題：牆不往內縮可能會生成在外面
		self.radius = modelconst.body_radius
		self.pos = pre.pos - pre.dir * (pre.radius + modelconst.body_radius + modelconst.body_gap)
		self.direction = pre.direction_list[0]
		self.direction_list = [self.direction]
		self.speed = pre.speed
	def update(self):
		self.pos += self.speed * self.direction
		self.direction = self.pre.direction_list[0]
		self.direction_list.append(self.direction)
		if len(self.direction_list) > modelconst.max_delay_ticks:
			self.direction_list.pop(0)
		self.speed = self.pre.speed
