import Model.const as modelConst
import View.const as viewConst
import random
#####################  const  #####################
# View  --> ScreenSize,FramePerSec
# Model --> wb_init_num, wb_max_num, wb_born_period
#####################  const  #####################

class White_Ball(object):
	def __init__(self):
        self.active=True
        self.color = [0,0,0]
        self.pos = [ random.randint(0,viewConst.ScreenSize[0]), random.randint(0,viewConst.ScreenSize[0]) ]
        #random init the position of balls

class White_Ball_List(object):
	def __init__(self):
		self.fps=viewConst.FramePerSec
		self.num=modelConst.wb_init_num
		#number of balls 
		self.max_num=modelConst.wb_max_num
		#max_number of balls 
		self.born_period=modelConst.wb_born_period
		self.wb_list=[]
		# the list of all white balls
		self.dead_list=[]
		# the index list of inactive balls
		self.dead_num=0
		# the number of inactive balls
        for x in range(num):
        	self.wb_list[x]=White_Ball()
        # initialize the list of balls
    def del_ball(self,index):
    	# call by head, delete all balls
    	self.wb_list[x].active=False
    	self.num-=1
    	self.dead_num+=1
    def Update_list(self):
    	if self.num <= self.max_num && random.randint(0,self.born_period*self.fps)==0:
    		# the num of balls < max nu m of balls
    		# && use random to check if we want to create new balls
    		#let's create new balls!
			if self.dead_num==0: 
				#all balls are active, so create a new ball at the end of the list
				new_ball=White_Ball()
				self.wb_list.append(new_ball)
    		else:
    			#reuse the dead ball in deadlist
    			self.wb_list[self.dead_num-1]=White_Ball()
    			self.dead_num-=1
    		self.num+=1

    			
    		