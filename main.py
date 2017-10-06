import random, node, controller, os, layer_params
import numpy as np
random.seed()

# import params
ninputs = layer_params.ninputs
nnodes = layer_params.nnodes
nneurons = layer_params.nneurons
noutputs = layer_params.noutputs
l = layer_params.l

min_uses = 100  # minimum number of times all neurons must be used per generation
mutate_amp = 0.02

max_gen = 21
use_graphics = False

cwd = os.getcwd()

# ---------------------------------------------------------------------------

class Layer:
	def __init__(self):
		self.L = [node.Node(nneurons, l) for i in range(nnodes)]
		self.participating = []

	def make_net(self):
		self.participating = []
		W1 = np.zeros([ninputs, nnodes])  # input weights
		W2 = np.zeros([nnodes, noutputs])  # output weights
		# select one neuron for each node
		for i in range(nnodes):
			nd = self.L[i]
			j = random.randint(0, nneurons - 1)
			nrn = nd.nrnlst[j]
			nrn.update_uses()
			self.participating.append(nrn)
			W1[:, i] = nrn.w[0:ninputs]
			W2[i, :] = nrn.w[ninputs:l]
		return (W1, W2)

	def update_participating_scores(self, s):
		for nrn in self.participating:
			nrn.score += s

	def get_min_uses(self):
		least_uses = 1000
		for nd in self.L:
			for nrn in nd.nrnlst:
				if nrn.uses < least_uses:
					least_uses = nrn.uses
		return least_uses

	def reset_nrns(self):
		for nd in self.L:
			for nrn in nd.nrnlst:
				nrn.reset()

	def evaluate_population(self):
		best_score = 0
		while self.get_min_uses() <= min_uses:
			W1, W2 = self.make_net()
			score = controller.Controller(W1, W2, use_graphics).go()
			
			'''
			if score > best_score:
				best_score = score
				best_W1 = W1[:]
				best_W2 = W2[:]
			scorefile.write(str(gen) + " " + str(score) + "\n")
			np.savetxt('w1.txt', W1, fmt='%f')
			np.savetxt('w2.txt', W2, fmt='%f')
			'''
			self.update_participating_scores(score)
		
		#np.savetxt('w1.txt', best_W1, fmt='%f')
		#np.savetxt('w2.txt', best_W2, fmt='%f')
		
		for nd in self.L:
			nd.set_avg_score_lst()
		self.reset_nrns()

	def mutate(self, w):
		for i in range(l):
			w[i] = w[i] + np.random.uniform(-mutate_amp, mutate_amp)
		return w

	def combine(self, p1w, p2w):
		# init
		wnew = np.random.rand(l)
		# choose cross pt
		pt = random.randint(0, l-1)
		# cross
		wnew[0:pt] = p1w[0:pt]
		wnew[pt:l] = p2w[pt:l]
		return self.mutate(wnew)

	def breed(self):
		num_selected = round(0.5*nneurons)  # select top third of neurons per node
		# loop nodes
		for nd in self.L:
			# get indices of best neurons
			idxs = np.argpartition(nd.avg_score_lst, -1 * num_selected)[-1 * num_selected:]
			# loop neurons
			for n in range(nneurons):
				# if n not selected
				if n not in idxs:
					# get index of two parents
					p1id = random.choice(idxs)
					p2id = random.choice(idxs)
					while p2id==p1id:
						p2id = random.choice(idxs)
					# get parent's weights
					p1w = nd.nrnlst[p1id].w
					p2w = nd.nrnlst[p2id].w
					# replace weights for neuron n
					nd.nrnlst[n].w = self.combine(p1w, p2w)

	def write_weights(self,gen):
		# make gen folder
		dir = 'layerdat\gen'+str(gen)
		if not os.path.exists(dir):
			os.makedirs(dir)
		# write weights
		i = -1
		for nd in self.L:
			# open node file
			i += 1
			f = open(cwd+'\layerdat'+'\gen'+str(gen)+'\\nd'+str(i)+'.txt','w')
			# write weights
			for nrn in nd.nrnlst:
				for val in nrn.w:
					f.write(str(val)+' ')
				f.write('\n')	
			# close node file
			f.close()

#---------------------------------------------------------------------------

# init
L = Layer()

for gen in range(max_gen):
	print("gen = " + str(gen))
	# write weights
	if gen%5 == 0:
		L.write_weights(gen)
	# evaluate
	L.evaluate_population()
	# select
	L.breed()

