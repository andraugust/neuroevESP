import sprites, numpy

bl_init_T = 150		# time steps between ball inits
PI2 = 6.28318530717958647692528

class World:
	
	def __init__(self):
		self.agent = sprites.Agent()
		self.balllst = [sprites.Ball()]
		self.food = sprites.Food()
		self.t = 0
	
	def step(self,action):
		self.t += 1
		# make new ball
		if self.t % bl_init_T == 0:
			self.balllst.append(sprites.Ball())
		# translate balls, check if need to delete balls
		new_balllst = []
		for i in range(len(self.balllst)):
			self.balllst[i].translate()
			if self.balllst[i].x > -self.balllst[i].r:
				new_balllst.append(self.balllst[i])
		self.balllst = new_balllst[:]
		# agent act
		self.agent.performAction(action)
		# check collision
		for b in self.balllst:
			if self.getD(b) < b.r:
				self.agent.hit()
		# check eating
		if self.getD(self.food) < self.food.r:
			self.agent.eat()
			self.food = sprites.Food()
	
	# get closest ball coordinates
	def get_cb_coords(self):
		dmin = 10.0
		for b in self.balllst:
			d = self.getD(b)
			if d < dmin:
				dmin = d
				b_closest = b
		return (dmin, self.getTheta(b_closest))
	
	def get_food_coords(self):
		return (self.getD(self.food), self.getTheta(self.food))
	
	def getD(self,o):
		# o is an object (e.g. food or ball)
		return numpy.sqrt(((self.agent.x-o.x)**2) + ((self.agent.y-o.y)**2))	   # normalized units
	
	def getTheta(self,o):
		dy = o.y - self.agent.y
		dx = o.x - self.agent.x
		temp = numpy.arctan2(dy,dx)
		t_dr = (temp + PI2) % (PI2)
		t_a = self.agent.theta
		if t_dr >= t_a:
			return t_dr - t_a
		else:
			return PI2 - t_a + t_dr
	
	def get_hearing(self):
		hearing = 0.0
		for bl in self.balllst:
			hearing += 0.03/(self.getD(bl)+0.03)
		return hearing