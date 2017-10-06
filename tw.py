import numpy as np
import controller, os, random, sys, layer_params

# import params
ninputs = layer_params.ninputs
nnodes = layer_params.nnodes
nneurons = layer_params.nneurons
noutputs = layer_params.noutputs
l = layer_params.l

gen = sys.argv[1]	# generation being tested

w1 = np.zeros((ninputs,nnodes))
w2 = np.zeros((nnodes,noutputs))

cwd = os.getcwd()

for i in range(nnodes):
	fname = cwd+'\layerdat\gen'+str(gen)+'\\nd'+str(i)+'.txt'
	f = open(fname,'r')
	# read random row
	line = random.choice(f.readlines())
	# put line into w1 and w2
	foo = np.fromstring(line, sep=' ')
	w1[:,i] = foo[0:ninputs]
	w2[i,:] = foo[ninputs:l]
	f.close()

while True:
	controller.Controller(w1,w2,True).go()