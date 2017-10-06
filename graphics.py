import pygame, sys, math
from generate import GenerateTone

pygame.init()
clock = pygame.time.Clock()

WIDTH = 600			# screen width pixels
AGENT_WIDTH = 0.015	# normalized units
fps = 200			# frames per second
use_tone = False

if use_tone:
	pygame.mixer.init()
	tone_rate = 100

class Graphics():
	
	def __init__(self):
		self.screen = pygame.display.set_mode((WIDTH, WIDTH))
		self.screen.fill((0,0,0))
		pygame.display.flip()
		self.t = 0
	
	def next(self,world):
		self.t += 1
		self.screen.fill((0,0,0))
		self.update_food(world.food)
		self.update_balls(world.balllst)
		self.update_health_bar(world.agent.health)
		self.update_agent(world.agent)
		pygame.display.flip()
		clock.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		if use_tone and self.t%tone_rate==0:
			self.update_tone(world.get_hearing())
	
	def update_tone(self,f):
		pygame.mixer.stop()
		GenerateTone(400.0*f).play(-1,fade_ms=100)
		#pygame.mixer.fadeout(100)
	
	def update_health_bar(self,health):
		x = int(WIDTH*0.2)
		y = int(WIDTH*0.01)
		w = int(WIDTH*0.6)
		whealth = w*health
		h = int(WIDTH*0.03)
		pygame.draw.rect(self.screen, (255,0,0), [x, y, w, h], 2)	#skeleton
		pygame.draw.rect(self.screen, (255,0,0), [x, y, whealth, h])	#skeleton
		#pygame.draw.rect(Surface, color, Rect, width=0)
	
	def update_balls(self,balllst):
		for bl in balllst:
			pygame.draw.circle(self.screen, (0,0,255), (int(bl.x*WIDTH), int(bl.y*WIDTH)), int(bl.r*WIDTH))
	
	def update_food(self,food):
		x = food.x
		y = food.y
		r = food.r
		pygame.draw.circle(self.screen, (0,255,0), (int(x*WIDTH), int(y*WIDTH)), int(r*WIDTH))
	
	def update_agent(self,agent):
		pygame.draw.polygon(self.screen, (255,0,0), self.get_agent_pts(agent.x,agent.y,agent.theta))
		#pygame.draw.aalines(self.screen, (255,0,0), True, self.get_agent_pts(agent.x,agent.y,agent.theta))
		
	def get_agent_pts(self,x,y,theta):
		# draw agent
		p1x = -AGENT_WIDTH
		p1y = AGENT_WIDTH/2.0
		p2x = -AGENT_WIDTH
		p2y = -AGENT_WIDTH/2.0
		p3x = AGENT_WIDTH
		p3y = 0.0
		# rotate
		Rp1x = p1x*math.cos(theta) - p1y*math.sin(theta)
		Rp1y = p1x*math.sin(theta) + p1y*math.cos(theta)
		Rp2x = p2x*math.cos(theta) - p2y*math.sin(theta)
		Rp2y = p2x*math.sin(theta) + p2y*math.cos(theta)
		Rp3x = p3x*math.cos(theta) - p3y*math.sin(theta)
		Rp3y = p3x*math.sin(theta) + p3y*math.cos(theta)
		# translate
		TRp1x = Rp1x + x
		TRp1y = Rp1y + y
		TRp2x = Rp2x + x
		TRp2y = Rp2y + y
		TRp3x = Rp3x + x
		TRp3y = Rp3y + y
		# set
		trianglePts = [TRp1x, TRp1y, TRp2x, TRp2y, TRp3x, TRp3y]
		ptsFloat = [WIDTH*a for a in trianglePts]      # scale triangle points
		ptsRound = [round(b) for b in ptsFloat]
		return [[ptsRound[0],ptsRound[1]],[ptsRound[2],ptsRound[3]],[ptsRound[4],ptsRound[5]]]