Uses a file to hold layer parameters.

------------------
NN input example:
rcb, thetcb = self.world.get_cb_coords()		# relative r, theta coords to closest ball (cb)
rf, thetf = self.world.get_food_coords()		# relative r, theta coords to food (cb)
x = [rcb, np.cos(thetcb), np.sin(thecb), rf, np.cos(thetf), np.sin(thetf), np.cos(self.world.agent.theta), np.sin(self.world.agent.theta), 1.0]

------------------
Uses pygame.
Neuroevolution.
Single agent.
Layer is a class.
Sprites are in a class together.
