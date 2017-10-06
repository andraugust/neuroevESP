import numpy as np
import random

class Neuron:
	
	def __init__(self,l):
		self.w = 2.0*np.random.rand(l)-1.0		# random init between -1 and 1
		self.uses = 0
		self.score = 0.0
		
	def reset(self):
		self.uses = 0
		self.score = 0.0
	
	def update_uses(self):
		self.uses += 1
		
	def update_score(self,s):
		self.score += s