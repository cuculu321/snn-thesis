

####################################################### README ####################################################################

# This is the main file which calls all the functions and trains the network by updating weights


#####################################################################################################################################


import numpy as np
from neuron import neuron
import random
from matplotlib import pyplot as plt
from spike_train import encode
from rl import rl
from rl import update
from parameters import param as par
from var_th import threshold

from get_current_directory import *
from get_logmelspectrum import get_log_melspectrum
from wav_split import wav_split
import os

#potentials of output neurons
potential_lists = []
for i in range(par.kSecondLayerNuerons_):
	potential_lists.append([])

#time series 
time_array  = np.arange(1, par.kTime_+1, 1)

layer2 = []

# creating the hidden layer of neurons
for i in range(par.kSecondLayerNuerons_):
	a = neuron()
	layer2.append(a)

#synapse matrix	initialization
synapse = np.zeros((par.kSecondLayerNuerons_, par.kFirstLayerNuerons_))

#get wavefile path for learning
learning_path = get_learning_path()

for i in range(par.kSecondLayerNuerons_):
	for j in range(par.kFirstLayerNuerons_):
		synapse[i][j] = random.uniform(0, 0.4 * par.kScale_)

for epoch in range(par.kEpoch_):
	for wave_file in learning_path:
		print(str(wave_file) + "  " + str(epoch))

		splited_sig_array, samplerate = wav_split(wave_file)
		print(wave_file)

		#Convolving image with receptive field
		signal = splited_sig_array[int(len(splited_sig_array)/2)]

		f_centers, mel_spectrum = get_log_melspectrum(signal, samplerate)

		#Generating spike train
		spike_train = np.array(encode(mel_spectrum))

		#calculating threshold value for the image
		var_threshold = threshold(spike_train)

		# print var_threshold
		# synapse_act = np.zeros((par.kSecondLayerNuerons_,par.kFirstLayerNuerons_))
		# var_threshold = 9
		# print var_threshold
		# var_D = (var_threshold*3)*0.07
		
		var_D = 0.15 * par.kScale_

		for x in layer2:
			x.initial(var_threshold)

		#flag for lateral inhibition
		flag_spike = 0
		
		img_win = 100

		active_potential = []
		for index1 in range(par.kSecondLayerNuerons_):
			active_potential.append(0)

		#Leaky integrate and fire neuron dynamics
		for time in time_array:
			for second_layer_position, second_layer_neuron in enumerate(layer2):
				active = []	
				if(second_layer_neuron.t_rest < time):
					second_layer_neuron.P = (second_layer_neuron.P 
											+ np.dot(
												synapse[second_layer_position], spike_train[:, time]
											  )
											)
					#print("synapse : " + str(synapse[second_layer_position]))
					if(second_layer_neuron.P > par.kPrest_):
						second_layer_neuron.P -= var_D
					active_potential[second_layer_position] = second_layer_neuron.P
				
				potential_lists[second_layer_position].append(second_layer_neuron.P)

			# Lateral Inhibition
			if(flag_spike==0):
				max_potential = max(active_potential)
				if(max_potential > var_threshold):
					flag_spike = 1
					winner_neuron = np.argmax(active_potential)
					img_win = winner_neuron
					print("winner is " + str(winner_neuron))
					for s in range(par.kSecondLayerNuerons_):
						if(s != winner_neuron):
							layer2[s].P = par.kMinPotential_

			#Check for spikes and update weights				
			for second_layer_position, second_layer_neuron in enumerate(layer2):
				neuron_status = second_layer_neuron.check()
				if(neuron_status == 1):
					second_layer_neuron.t_rest = time + second_layer_neuron.t_ref
					second_layer_neuron.P = par.kPrest_
					for first_layer_position in range(par.kFirstLayerNuerons_):
						#前シナプスの計算
						for back_time in range(-2, par.kTimeBack_-1, -1): #-2 → -20
							if 0 <= time + back_time < par.kTime_ + 1:
								if spike_train[first_layer_position][time + back_time] == 1:
									# print "weight change by" + str(update(synapse[j][h], rl(t1)))
									synapse[second_layer_position][first_layer_position] = update(
										synapse[second_layer_position][first_layer_position], rl(back_time)
										)
									 
						#後シナプスの計算
						for fore_time in range(2, par.kTimeFore_+1, 1): # 2 → 20
							if 0 <= time + fore_time<par.kTime_+1:
								if spike_train[first_layer_position][time + fore_time] == 1:
									# print "weight change by" + str(update(synapse[j][h], rl(t1)))
									synapse[second_layer_position][first_layer_position] = update(
										synapse[second_layer_position][first_layer_position], rl(fore_time)
										)
									
		if(img_win!=100):
			for first_layer_position in range(par.kFirstLayerNuerons_):
				if sum(spike_train[first_layer_position]) == 0:
					synapse[img_win][first_layer_position] -= 0.06 * par.kScale_
					if(synapse[img_win][first_layer_position]<par.kMinWait_):
						synapse[img_win][first_layer_position] = par.kMinWait_
		

x_axis = np.arange(0, len(potential_lists[0]), 1)
layer2_Pth = []
for i in range(len(x_axis)):
	layer2_Pth.append(layer2[0].Pth)

#plotting 
for second_layer_position in range(par.kSecondLayerNuerons_):
	axes = plt.gca()
	axes.set_ylim([-20,50])
	plt.plot(x_axis, layer2_Pth, 'r' )
	plt.plot(x_axis, potential_lists[second_layer_position])
	plt.show()

#Reconstructing weights to analyse training
for second_layer_position in range(par.kSecondLayerNuerons_):
	reconst_weights(synapse[second_layer_position], second_layer_position+1)
