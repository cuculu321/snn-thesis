import numpy as np
from neuron import neuron
import random
from spike_train import encode
from parameters import param as par
from var_th import threshold

from console_write import *
from get_logmelspectrum import get_log_melspectrum
from wav_split import wav_split

from collections import Counter

def winner_take_all(synapse, wave_file):
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

	neuron_spiked = np.zeros(par.kSecondLayerNuerons_)

	for epoch in range(1):
		resemble_print(str(wave_file) + "  " + str(epoch))
		
		#音声データの読み込み
		splited_sig_array, samplerate = wav_split(str(wave_file))
		resemble_print(wave_file)

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
						neuron_spiked[winner_neuron] += 1
						resemble_print("winner is " + str(winner_neuron))
						for s in range(par.kSecondLayerNuerons_):
							if(s != winner_neuron):
								layer2[s].P = par.kMinPotential_
	
	#勝ったニューロンの特定
	resemble_print("win neuron : " + str(max_index(neuron_spiked)))

	return max_index(neuron_spiked)


def max_index(list_data):
	np_list_name = np.array(list_data)
	return np_list_name.argmax()


def extract_label(wav_file_name):
	wav_file_str = str(wav_file_name)
	return wav_file_str[wav_file_str.find("_") + 1 : wav_file_str.find(".wav")]


def mapping(mapping_list, neuron_potision, checked_wavfile):
	mapping_list[neuron_potision].append(extract_label(checked_wavfile))
	return mapping_list


def calculate_mode(list_data):
    c = Counter(list_data)
    # すべての要素とその出現回数を取り出します。
    freq_scores = c.most_common()
    #c.most_common内の最も多い要素[0]の最大出現回数[1]を[0][1]で指定
    max_count = freq_scores[0][1]

    modes = []
    for num in freq_scores:
        if num[1] == max_count:
            modes.append(num[0])
    return modes


if __name__ == "__main__":
	from record_synapse import *

	import random
	import sys
	from get_current_directory import *

	args = sys.argv
	input_synaps = args[1]
	synapse = import_synapse("synapse_record/" + str(input_synaps) + ".txt")

	secondhand_wav_file = []
	speaker_list = [i for i in range(0, 12)]

	mapping_list = [[] for _ in range(par.kSecondLayerNuerons_)]

	mapping_path = get_vowel_path()
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
