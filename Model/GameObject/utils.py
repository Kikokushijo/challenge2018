class Vec():
	def __init__(self,x,y):
		self.x=x
		self.y=y
	def __init__(self,v):
		self.x=v.x
		self.y=v.y
	def __str__(self):
		return "("+str(self.x)+','+str(self.y)+")"
	def __add__(self,that):
		return Vec(self.x+that.x,self.y+that.y)
	def __sub__(self,that):
		return Vec(self.x-that.x,self.y-that.y)
	def __mul__(self,that):
		return Vec(self.x*that,self.y*that)
	def __truediv__(self,that):
		return Vec(self.x/that,self.y/that)
	def mag(self):
		return (self.x**2+self.y**2)**(1/2)
	def mag2(self):
		return (self.x**2+self.y**2)


