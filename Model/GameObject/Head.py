import Model.const as modelconst
import View.const as viewconst
import random
import math 

from white_ball import white_ball
from body import body 
from bullet import bullet


################################
# WB_List.wb_list[]
################################

class head(object):
	def __init__(self, name, index)
		# basic data
		self.name = name
		self.index = index 
		screen_mid = Vec( viewconst.ScreenSize[0]/2, viewconst.ScreenSize[1]/2 )

		#up down left right
		self.pos = screen_mid + model.init_r * Vec_dir[self.index]
		
		self.theta = index * (pi/2)
		self.direction = Vec( cos(self.theta), sin(self.theta) )
		
		self.speed = modelconst.normal_speed
		self.is_dash = False
		self.dash_timer = 0
		self.radius = modelconst.head_radius
		self.is_alive = True
		self.body_list = [self]
		self.is_ingrav = False
		self.is_circling = False
		self.circling_radius = 0
		#in which grav
		self.grav_center = Vec(0,0)

	def update(self, wb_list, bullet_list):
		
		self.pos += self.direction * self.speed
		
		if self.is_circling == True :
			self.theta += (self.speed/self.circling_radius)*modelconst.dt
			self.direction = Vec( cos(self.theta), sin(self.theta) )
		
		#is in circle
		for i in modelconst.grav :
			if ( self.pos - i[0] ).mag2 < i[1]**2 :
				self.is_ingrav = True
				self.circling_radius = (self.pos - i[0]).mag
				self.grav_center = i[0]

		#collision with wall
		if (self.direction.x > 0) and (self.pos.x > viewconst.ScreenSize[0]-modelconst.eps) :
			self.direction.x *= -1
		if (self.direction.x < 0) and (self.pos.x < 0 - eps) :
			self.direction.x *= -1
		if (self.direction.y > 0) and (self.pos.y > viewconst.ScreenSize[1]-modelconst.eps) :
			self.direction.y *= -1
		if (self.direction.y < 0) and (self.pos.x < 0 - eps) :
			self.direction.y *= -1
		
		#collision with white ball
		for ii,i in enumerate(wb_list):
			if (self.pos - i.radius).mag2 < (self.radius + i.radius)**2 :
				#delete a withe ball
				del wb_list[i]
				#lengthen body list
				self.body_list.append( body.Body(self.body_list[-1]) )
		
		#collision with competitor's body
		if self.is_dash == False :
			for i in player:
				if i.index == self.index :
					continue
				for j in range(1,len(i.body_list)) :
					if (self.pos - i.radius).mag2 < (self.radius + i.radius)**2 :
						#self die
						self.is_alive = False

		#collision with competitor's bullet
		if self.is_dash == False :
			for i in bullet.Bullet.bullet_list :
				if (self.pos - i.radius).mag2 < (self.radius + i.radius)**2 :
					self.is_alive = False
		
		#collision with item


		#dash timer
		if self.is_dash == True :
			self.dash_timer--
			if self.dash_timer == 0 :
				self.is_dash = False
	
	def click(self) :
		if self.is_ingrav == True :
			self.is_circling = (not self.is_circling)
			self.theta = atan2( self.pos[0]-self.grav_center[0], self.pos[1]-self.grav_center[1] )
		
		else :
			self.is_dash = True 
			self.dash_timer = modelconst.max_dash_time
			self.speed = modelconst.dash_speed
			## call bullet












