import neuron
import numpy as np

class Node:	
	
	def __init__(self,nneurons,l):
		self.nrnlst = [neuron.Neuron(l) for i in range(nneurons)]
		self.avg_score_lst = np.array([])
	
	def set_avg_score_lst(self):
		self.avg_score_lst = np.array([])
		for nrn in self.nrnlst:
			self.avg_score_lst = np.append(self.avg_score_lst, nrn.score/nrn.uses)