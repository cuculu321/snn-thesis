

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

from console_write import *
from get_current_directory import *
from get_logmelspectrum import get_log_melspectrum
from wav_split import *
from record_synapse import *


def learning(learning_path, synapse):
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

	export_txt(synapse, "synapse_record/" + "initial" + create_timestamp())

	for epoch in range(1):
		for wave_file in learning_path:
		#for wave_file in ["sounddata\F1\F1SYB01_が.wav"]:
			resemble_print(str(wave_file) + "  " + str(epoch))
			
			#音声データの読み込み
			splited_sig_array, samplerate = wav_split(str(wave_file))
			resemble_print(str(wave_file))
			
			#スパイクの連結
			#spike_train = wav_split2spike(splited_sig_array, samplerate)
			#spike_connected = np.array(connect_spike(spike_train))
			#for spike_train in spike_connected:
			for signal in splited_sig_array:
				#Generating melspectrum
				f_centers, mel_spectrum = get_log_melspectrum(signal, samplerate)

				#Generating spike train
				spike_train = np.array(encode(np.log10(mel_spectrum)))

				#calculating threshold value for the image
				var_threshold = threshold(spike_train)

				# resemble_print var_threshold
				# synapse_act = np.zeros((par.kSecondLayerNuerons_,par.kFirstLayerNuerons_))
				# var_threshold = 9
				# resemble_print var_threshold
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
							#resemble_print("synapse : " + str(synapse[second_layer_position]))
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
							resemble_print("winner is " + str(winner_neuron))
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
											# resemble_print "weight change by" + str(update(synapse[j][h], rl(t1)))
											synapse[second_layer_position][first_layer_position] = update(
												synapse[second_layer_position][first_layer_position], rl(back_time)
												)
											resemble_print("back : " + str(second_layer_position) + "-" + str(first_layer_position) + " : " + str(synapse[second_layer_position][first_layer_position]))
								#後シナプスの計算
								for fore_time in range(2, par.kTimeFore_+1, 1): # 2 → 20
									if 0 <= time + fore_time<par.kTime_+1:
										if spike_train[first_layer_position][time + fore_time] == 1:
											# resemble_print "weight change by" + str(update(synapse[j][h], rl(t1)))
											synapse[second_layer_position][first_layer_position] = update(
												synapse[second_layer_position][first_layer_position], rl(fore_time)
												)
											resemble_print("fron : " + str(second_layer_position) + "-" + str(first_layer_position) + " : " + str(synapse[second_layer_position][first_layer_position]))


				if(img_win!=100):
					for first_layer_position in range(par.kFirstLayerNuerons_):
						if sum(spike_train[first_layer_position]) == 0:
							synapse[img_win][first_layer_position] -= 0.06 * par.kScale_
							if(synapse[img_win][first_layer_position]<par.kMinWait_):
								synapse[img_win][first_layer_position] = par.kMinWait_

	return potential_lists, synapse, layer2


def wav_split2spike(splited_sig_array, samplerate):
	spike_train = []
	for signal in splited_sig_array:

		#Generating melspectrum
		f_centers, mel_spectrum = get_log_melspectrum(signal, samplerate)

		#Generating spike train
		spike_train.append(np.array(encode(10 * np.log10(mel_spectrum))))

	return spike_train


def connect_spike(spike_train):
	#頭を基に、後ろ4つのスパイクを連結
	spike_connected = []
	for i in range(0, len(spike_train) - 3, 2):
		spike_connected_wip = []
		spike_connected_wip.extend(spike_train[i])
		spike_connected_wip.extend(spike_train[i+1])
		spike_connected_wip.extend(spike_train[i+2])
		spike_connected_wip.extend(spike_train[i+3])
		spike_connected.append(spike_connected_wip)
	
	return spike_connected


if __name__ == "__main__":
	import random
	from get_current_directory import get_mappingfile_path
	from mapping import *

	#学習
	#get wavefile path for learning
	learning_path = get_mappingfile_path()
	learning_path = [onedivision for a in learning_path for onedivision in a] #2次元のパスを1次元に変更

	#which synapse
	args = sys.argv
	if len(args) == 1:
		#synapse matrix	initialization
		synapse = np.zeros((par.kSecondLayerNuerons_, par.kFirstLayerNuerons_))
		for i in range(par.kSecondLayerNuerons_):
			for j in range(par.kFirstLayerNuerons_):
				synapse[i][j] = random.uniform(0, 0.4 * par.kScale_)
	else:
		input_synaps = args[1]
		synapse = import_synapse("synapse_record/" + str(input_synaps) + ".txt")

	print(synapse)
	potential_lists, synapse, layer2 = learning(learning_path, synapse)

	resemble_print("synapse : ")
	resemble_print(synapse)
	export_txt(synapse, "synapse_record/" + create_timestamp())

	#対応付け
	secondhand_wav_file = []
	speaker_list = [i for i in range(0, 12)]

	mapping_list = [[] for _ in range(par.kSecondLayerNuerons_)]

	mapping_path = get_mappingfile_path()
	for i in range(len(mapping_path)):
		mapping_path[i].sort()

	for syllable_num in range(len(mapping_path[0])):
		use_speakers = random.sample(speaker_list, 6)
		resemble_print(use_speakers)
		secondhand_wav_file.append(use_speakers)
		winner_neurons = []
		for speaker in use_speakers:
			resemble_print(str(speaker) + " : " + str(syllable_num) + " : " + str(mapping_path[speaker][syllable_num]))
			winner_neurons.append(winner_take_all(synapse, mapping_path[speaker][syllable_num]))
	
		neuron_mode = calculate_mode(winner_neurons)
		resemble_print(neuron_mode[0])
		mapping_list = mapping(mapping_list, neuron_mode[0], mapping_path[speaker][syllable_num])
		resemble_print(mapping_list)


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