######################################################## README #############################################################

# This file generates rate based spike train from the potentialential map.

############################################################################################################################


import numpy as np
from numpy import interp
from neuron import neuron
import random
from matplotlib import pyplot as plt
from recep_field import rf
import cv2
from rl import rl
from rl import update
import math
from parameters import param as par

def encode(potential):

	#initializing spike train
	train = []

	for l in range(par.kPixelX_):
		for m in range(par.kPixelX_):
		
			time_list = np.zeros([(par.kTime_+1), ])

			#calculating firing rate proportional to the membrane potential
			freq = interp(potential[l][m], [-1.069, 2.781], [1, 20])

			# print freq
			if freq <= 0:
				print(error)
				
			freq1 = math.ceil(600 / freq)
			#print("freq  1 : " + str(l) + " m : " + str(m) + "   " + str(freq))

			#generating spikes according to the firing rate
			spike_freq = freq1
			if(potential[l][m] > 0):
				while spike_freq < (par.kTime_ + 1):
					time_list[spike_freq] = 1
					spike_freq = spike_freq + freq1
			train.append(time_list)
			#print(sum(time_list))
			#print("time_list  1 : " + str(l) + " m : " + str(m) + "   " + str(sum(time_list)))
	return train

if __name__  == '__main__':
	# m = []
	# n = []
	img = cv2.imread("mnist1/" + str(15) + ".png", 0)

	potential = rf(img)

	# for i in potential:
	# 	m.append(max(i))
	# 	n.append(min(i))

	# print max(m), min(n)
	train = encode(potential)
	f = open('look_ups/train6.txt', 'w')
	print(np.shape(train))

	for i in range(201):
		for j in range(784):
			f.write(str(int(train[j][i])))
		f.write('\n')

	f.close()