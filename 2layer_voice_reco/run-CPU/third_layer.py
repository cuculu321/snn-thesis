from mapping import *
import numpy as np
from parameters import param as par

import math

def cos_sim(v1, v2):

	return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


if __name__ == "__main__":
	from record_synapse import *

	import random
	import sys
	from get_current_directory import *
	from mapping import max_index, extract_label

	args = sys.argv
	if len(args) == 3:
		print("run")
	else:
		print("-t [1-2synapse path] training 2-3 synapse")
		print("-c [2-3synapse path] check accuracy")
		sys.exit()

	mode = args[1]
	input_synaps = args[2]
	if mode == "-t":
		#synapse = import_synapse("synapse_record/" + str(input_synaps) + ".txt")
		synapse = import_synapse(input_synaps + "/1-2synapse" + input_synaps +".txt")

		secondhand_wav_file = []
		speaker_list = [i for i in range(0, 12)]

		mapping_path = get_mappingfile_path()
		for i in range(len(mapping_path)):
			mapping_path[i].sort()

		third_neuron = []
		mapping_list = []

		for syllable_num in range(len(mapping_path[0])): #単音節の数(F1のファイル数)分ループ
			use_speakers = random.sample(speaker_list, 6)
			resemble_print(use_speakers)
			secondhand_wav_file.append(use_speakers)
			winner_neurons = []

			second_third_synapse = np.zeros(par.kSecondLayerNuerons_)

			for speaker in use_speakers:
				resemble_print(str(speaker) + " : " + str(syllable_num) + " : " + str(mapping_path[speaker][syllable_num]))
				count_neuron_fire = winner_take_all(synapse, mapping_path[speaker][syllable_num])
				num_neuron_fire = sum(count_neuron_fire)
				print(num_neuron_fire)

				second_third_synapse += count_neuron_fire / num_neuron_fire

			second_third_synapse = second_third_synapse / len(use_speakers)
			print(second_third_synapse)
			third_neuron.append(second_third_synapse)
			mapping_list.append(extract_label(mapping_path[speaker][syllable_num]))

		second_third_synapse_path = input_synaps + "/2-3synapse" + input_synaps
		export_list2txt(third_neuron, second_third_synapse_path)

	elif mode == "-c":
		print("check")
		#synapse = import_synapse("synapse_record/" + str(input_synaps) + ".txt")
		synapse = import_synapse(input_synaps + "/1-2synapse" + input_synaps +".txt")
		
		#second_third_synapse = import_synapse("2-3synapse/" + str(input_synaps) + ".txt")
		second_third_synapse = import_synapse(input_synaps + "/2-3synapse" + input_synaps +".txt")

		print(synapse)

		secondhand_wav_file = []
		speaker_list = [i for i in range(0, 12)]

		mapping_path = get_mappingfile_path()
		for i in range(len(mapping_path)):
			mapping_path[i].sort()

		third_neuron = []
		#mapping_list = [[] for _ in range(len(mapping_path[0]))]
		mapping_list = []
		neuron_parsent = np.zeros((len(mapping_path[0]),len(mapping_path[0])))
		win_neuron = np.zeros(len(mapping_path[0]))
		accuracy = np.zeros((len(mapping_path[0]),len(mapping_path[0])))

		for syllable_num in range(len(mapping_path[0])): #単音節の数(F1のファイル数)分ループ
			use_speakers = random.sample(speaker_list, 6)
			resemble_print(use_speakers)
			secondhand_wav_file.append(use_speakers)
			winner_neurons = []

			mapping_list.append(extract_label(mapping_path[0][syllable_num]))

			for speaker in use_speakers:
				resemble_print(str(speaker) + " : " + str(syllable_num) + " : " + str(mapping_path[speaker][syllable_num]))
				count_neuron_fire = winner_take_all(synapse, mapping_path[speaker][syllable_num])
				num_neuron_fire = sum(count_neuron_fire)

				parsent_neuron_fire = count_neuron_fire / num_neuron_fire

				"""
				#各値のらしさを計算
				for syllable in range(len(mapping_path[0])):
					neuron_parsent[syllable_num][syllable] += cos_sim(second_third_synapse[syllable_num], parsent_neuron_fire)
				"""
				#最も近いニューロンに1を加算する
				for syllable in range(len(mapping_path[0])):
					print(second_third_synapse[syllable])
					how_like = cos_sim(second_third_synapse[syllable], parsent_neuron_fire)
					#print(how_like)
					neuron_parsent[syllable_num][syllable] += how_like
					win_neuron[syllable] += how_like
				#print(win_neuron)
				#print(max_index(win_neuron))
				accuracy[syllable_num][max_index(win_neuron)] += 1

		#neuron_parsent = neuron_parsent / len(use_speakers)
		print(neuron_parsent)
		accuracy = accuracy / len(use_speakers)
		export_list2txt(neuron_parsent, input_synaps + "/end" + str(input_synaps))
		export_list2txt(accuracy, input_synaps + "/answer" + str(input_synaps))

		#全体の正答率の算出
		corrent_answers = []
		for i in range(len(mapping_path[0])):
			print(mapping_list[i] + " : " + str(accuracy[i][i]))
			corrent_answers.append(accuracy[i][i])
		
		print(sum(corrent_answers) / len(mapping_path[0]))