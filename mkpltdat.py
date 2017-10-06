import numpy as np
import controller, os, random, sys, layer_params

'''
mkpltdat.py generates N random agents for each generation 0, 5, 10, ... by
reading weights in the directory layerdat. Each agent's lifetime is
written to pltdat.txt.
'''

# import params
ninputs = layer_params.ninputs
nnodes = layer_params.nnodes
nneurons = layer_params.nneurons
noutputs = layer_params.noutputs
l = layer_params.l

w1 = np.zeros((ninputs,nnodes))
w2 = np.zeros((nnodes,noutputs))
N = 100		# number of trial agents per generation
cwd = os.getcwd()
pltdatf = open(cwd+'\pltdat.txt','w')


def get_w(gn):
	for i in range(nnodes):
		fname = cwd+'\layerdat\gen'+str(gn)+'\\nd'+str(i)+'.txt'
		f = open(fname,'r')
		# read random row
		line = random.choice(f.readlines())
		# put line into w1 and w2
		foo = np.fromstring(line, sep=' ')
		w1[:,i] = foo[0:ninputs]
		w2[i,:] = foo[ninputs:l]
		f.close()
	return (w1,w2)

for gen in range(0,21,5):
	for n in range(N):
		w1, w2 = get_w(gen)
		age = controller.Controller(w1,w2,False).go()
		pltdatf.write(str(gen)+' '+str(age)+'\n')
		
pltdatf.close()