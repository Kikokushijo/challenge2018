import Model.const as modelconst
import View.const as viewconst
import random
import Model.white_ball as white_ball



################################
# WB_List.wb_list[]
################################

class head(object):
	def __init__(self, name, index)
		# basic data
		self.name = name
		self.index = index 
		mid = Vec( viewconst.ScreenSize[0]/2, viewconst.ScreenSize[1]/2 )

		self.position = mid + model.init_r * ()
		self.dir = 
		
		self.speed = modelconst.normal_speed
		self.is_dash = False
		self.dash_timer = 0
		self.radius = modelconst.head_radius
		self.is_alive = True

	
	def update(self):
		
		self.pos += self.dir * self.speed
		#collision with wall
		if self.pos.x > 800 or self.pos.x < 0:
			self.dir.x *= -1
		if self.pos.y > 800 or self.pos.y < 0:
			self.dir.y *= -1
		
		#collision with white ball
		
		
		if 
		
		#collision with competitor's ball
		
		
		
		
	def collision():
		

	def 

			
		
		
		
		
		








