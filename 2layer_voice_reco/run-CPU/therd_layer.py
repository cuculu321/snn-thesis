from mapping import *
import numpy as np
from parameters import param as par

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

	mapping_path = get_mappingfile_path()
	for i in range(len(mapping_path)):
		mapping_path[i].sort()

	therd_neuron = []
	mapping_list = []

	for syllable_num in range(len(mapping_path[0])): #単音節の数(F1のファイル数)分ループ
		use_speakers = random.sample(speaker_list, 6)
		resemble_print(use_speakers)
		secondhand_wav_file.append(use_speakers)
		winner_neurons = []

		second_therd_synapse = np.zeros(par.kSecondLayerNuerons_)

		for speaker in use_speakers:
			resemble_print(str(speaker) + " : " + str(syllable_num) + " : " + str(mapping_path[speaker][syllable_num]))
			count_neuron_fire = winner_take_all(synapse, mapping_path[speaker][syllable_num])
			num_neuron_fire = sum(count_neuron_fire)
			print(num_neuron_fire)

			second_therd_synapse += count_neuron_fire / num_neuron_fire

		second_therd_synapse = second_therd_synapse / len(use_speakers)
		print(second_therd_synapse)
		therd_neuron.append(second_therd_synapse)
		mapping_list.append(extract_label(mapping_path[speaker][syllable_num]))

