import random, math
random.seed()

# agent params
PI2 = 6.28318530717958647692528
TRANSLATION_DISTANCE = 0.004	# normalized units
ROTATION_ANGLE = PI2/15.0	  # radians
METABOLIC_COST = 0.001 #0.0008			# normalized cost to perform an action
ACTION_COST = 0.0 #2.0*METABOLIC_COST
HIT_COST = 0.2 #0.04

# ball params
BALLV = 0.002
BALLR = 0.08

# food params
FOODR = 0.05

class Agent:

	def __init__(self):
		self.x = random.random()
		self.y = random.random()
		self.theta = PI2*random.random()
		self.health = 1.0
		self.lifetime = 0					   # this keeps track of how long the agent has lived for

	def performAction(self, a):
		if a=="trans":
			self.translate()
			self.health -= ACTION_COST
		elif a=="rot":
			self.rotate()
			self.health -= ACTION_COST
		self.health -= METABOLIC_COST
		self.lifetime += 1

	def translate(self):
		xNew = self.x + TRANSLATION_DISTANCE*math.cos(self.theta)
		if 0 < xNew < 1.0:
			self.x = xNew
		yNew = self.y + TRANSLATION_DISTANCE*math.sin(self.theta)
		if 0.0 < yNew < 1.0:
			self.y = yNew

	def rotate(self):
		self.theta += ROTATION_ANGLE
		self.theta = self.theta % (PI2)

	def eat(self):
		self.health = 1.0
		
	def hit(self):
		self.health -= HIT_COST


class Ball:
	
	def __init__(self):
		# init balls on right side, arbitrary y
		self.r = BALLR
		self.x = 1.0+BALLR
		self.y = random.random()*(1.0+2.0*self.r) - self.r

	def translate(self):
		self.x -= BALLV

	
class Food:

	def __init__(self):
		self.r = FOODR				 # normalized units
		self.x = (1.0 - 2.0*self.r)*random.random() + self.r
		self.y = (1.0 - 2.0*self.r)*random.random() + self.r