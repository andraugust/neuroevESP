import world_class, graphics, time
import numpy as np

actions = ["sit", "rot", "trans"]
PI2 = 6.28318530717958647692528

class Controller:
	
	def __init__(self,W1,W2,use_graphics):
		self.W1 = W1
		self.W2 = W2
		self.world = world_class.World()
		self.use_graphics = use_graphics
		if use_graphics:
			self.g = graphics.Graphics()
	
	def geta(self,x1):
		# evaluate the nn
		tmp = np.dot(np.transpose(self.W1), np.transpose(x1))
		x2 = np.tanh(tmp)
		tmp = np.dot(np.transpose(self.W2), x2)
		return actions[np.argmax(tmp)]		# return action index
	
	def go(self):
		while self.world.agent.health > 0.0:
			rcb, thetcb = self.world.get_cb_coords()		# relative r, theta coords to closest ball (cb)
			rf, thetf = self.world.get_food_coords()# relative r, theta coords to food (cb)
			x = [rcb, np.cos(thetcb), np.sin(thetcb), rf, np.cos(thetf), np.sin(thetf), np.cos(self.world.agent.theta), np.sin(self.world.agent.theta), 1.0]
			a = self.geta(x)
			self.world.step(a)
			if self.use_graphics:
				self.g.next(self.world)
		return self.world.agent.lifetime