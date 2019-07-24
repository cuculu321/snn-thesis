

####################################################### README ####################################################################

# This is the main file which calls all the functions and trains the network by updating weights


#####################################################################################################################################


import numpy as np
from neuron import neuron
import random
from matplotlib import pyplot as plt
from recep_field import rf
import cv2
from spike_train import encode
from rl import rl
from rl import update
from reconstruct import reconst_weights
from parameters import param as par
from var_th import threshold
import os

#potentials of output neurons
pot_arrays = []
for i in range(par.kSecondLayerNuerons_):
	pot_arrays.append([])

#time series 
time  = np.arange(1, par.kTime_+1, 1)

layer2 = []

# creating the hidden layer of neurons
for i in range(par.kSecondLayerNuerons_):
	a = neuron()
	layer2.append(a)

#synapse matrix	initialization
synapse = np.zeros((par.kSecondLayerNuerons_,par.kFirstLayerNuerons_))

for i in range(par.kSecondLayerNuerons_):
	for j in range(par.kFirstLayerNuerons_):
		synapse[i][j] = random.uniform(0,0.4*par.kScale_)

for k in range(par.kEpoch_):
	for i in range(3221,3222):
		print(str(i) + "  " + str(k))
		img = cv2.imread("mnist1/" + str(i) + ".png", 0)
		print("mnist1/" + str(i) + ".png")

		#Convolving image with receptive field
		pot = rf(img)

		#Generating spike train
		train = np.array(encode(pot))

		#calculating threshold value for the image
		var_threshold = threshold(train)

		# print var_threshold
		# synapse_act = np.zeros((par.kSecondLayerNuerons_,par.kFirstLayerNuerons_))
		# var_threshold = 9
		# print var_threshold
		# var_D = (var_threshold*3)*0.07
		
		var_D = 0.15*par.kScale_

		for x in layer2:
			x.initial(var_threshold)

		#flag for lateral inhibition
		f_spike = 0
		
		img_win = 100

		active_pot = []
		for index1 in range(par.kSecondLayerNuerons_):
			active_pot.append(0)

		#Leaky integrate and fire neuron dynamics
		for t in time:
			for j, x in enumerate(layer2):
				active = []	
				if(x.t_rest<t):
					x.P = x.P + np.dot(synapse[j], train[:,t])
					#print("synapse : " + str(synapse[j]))
					if(x.P>par.kPrest_):
						x.P -= var_D
					active_pot[j] = x.P
				
				pot_arrays[j].append(x.P)

			# Lateral Inhibition		
			if(f_spike==0):
				high_pot = max(active_pot)
				if(high_pot>var_threshold):
					f_spike = 1
					winner = np.argmax(active_pot)
					img_win = winner
					print("winner is " + str(winner))
					for s in range(par.kSecondLayerNuerons_):
						if(s!=winner):
							layer2[s].P = par.kMinPotential_

			#Check for spikes and update weights				
			for j,x in enumerate(layer2):
				s = x.check()
				if(s==1):
					x.t_rest = t + x.t_ref
					x.P = par.kPrest_
					for h in range(par.kFirstLayerNuerons_):
						#後シナプスの計算
						for t1 in range(-2,par.kTimeBack_-1, -1):
							if 0 <= t + t1 < par.kTime_ + 1:
								if train[h][t+t1] == 1:
									# print "weight change by" + str(update(synapse[j][h], rl(t1)))
									synapse[j][h] = update(synapse[j][h], rl(t1))
									 


						#前シナプスの計算
						for t1 in range(2,par.kTimeFore_+1, 1):
							if 0<=t+t1<par.kTime_+1:
								if train[h][t+t1] == 1:
									# print "weight change by" + str(update(synapse[j][h], rl(t1)))
									synapse[j][h] = update(synapse[j][h], rl(t1))
									
		if(img_win!=100):
			for p in range(par.kFirstLayerNuerons_):
				if sum(train[p])==0:
					synapse[img_win][p] -= 0.06*par.kScale_
					if(synapse[img_win][p]<par.kMinWait_):
						synapse[img_win][p] = par.kMinWait_
		

ttt = np.arange(0,len(pot_arrays[0]),1)
Pth = []
for i in range(len(ttt)):
	Pth.append(layer2[0].Pth)

#plotting 
for i in range(par.kSecondLayerNuerons_):
	axes = plt.gca()
	axes.set_ylim([-20,50])
	plt.plot(ttt,Pth, 'r' )
	plt.plot(ttt,pot_arrays[i])
	plt.show()

#Reconstructing weights to analyse training
for i in range(par.kSecondLayerNuerons_):
	reconst_weights(synapse[i],i+1)