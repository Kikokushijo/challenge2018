import Model.const as modelconst
import View.const as viewconst
import random
import Model.white_ball as white_ball
import Model.body as body 
import Model.bullet as bullet


################################
# WB_List.wb_list[]
################################

class head(object):
	def __init__(self, name, index)
		# basic data
		self.name = name
		self.index = index 
		mid = Vec( viewconst.ScreenSize[0]/2, viewconst.ScreenSize[1]/2 )

		self.pos = mid + model.init_r * ()
		self.direction = 
		
		self.speed = modelconst.normal_speed
		self.is_dash = False
		self.dash_timer = 0
		self.radius = modelconst.head_radius
		self.is_alive = True
		self.body_list = [self]
	
	def update(self):
		
		self.pos += self.direction * self.speed
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
		for ii,i in enumerate(white_ball.WB_List.wb_list):
			if i.active==True and (self.pos - i.radius).mag2 < (self.radius + i.radius)**2 :
				#delete a withe ball
				white_ball.WB_List.del_ball(ii)
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
		





