######################################################## README #############################################################

# This file generates rate based spike train from the potentialential map.

############################################################################################################################


import numpy as np
from numpy import interp
import math
from parameters import param as par

def encode(potential):
	"""
	メル周波数スペクトラムからスパイク列を生成する

	Parameters
	----------
	potential : float list[22]
		メル周波数スペクトラムのdB要素

	Returns
	------
	train : boolean list[22, 200]
		畳み込みデータの値によって、スパイク率を変え出力された配列データ。
	"""

	#initializing spike train
	train = []

	for hz_point in range(par.kMelChannelCount_):
	
		time_list = np.zeros([(par.kTime_+1), ])

		#calculating firing rate proportional to the membrane potential
		freq = interp(potential[hz_point], [-1.069, 2.781], [1, 20])

		# print freq
		if freq <= 0:
			print(error)
			
		freq1 = math.ceil(600 / freq)
		#print("freq  1 : " + str(l) + " m : " + str(m) + "   " + str(freq))

		#generating spikes according to the firing rate
		spike_freq = freq1
		if(potential[hz_point] > 0):
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
	from wav_split import wav_split
	from get_logmelspectrum import get_log_melspectrum
	from record_synapse import export_txt

	speech_file = "sounddata/F1/F1SYB01_が.wav"

	splited_sig_array, samplerate = wav_split(speech_file)
	signal = splited_sig_array[int(len(splited_sig_array)/2)]

	page = 0
	for signal in splited_sig_array:
		page = page + 1
		f_centers, mel_spectrum = get_log_melspectrum(signal, samplerate)

		# for i in potential:
		# 	m.append(max(i))
		# 	n.append(min(i))

		# print max(m), min(n)
		train = encode(np.log10(mel_spectrum))
		print("page: " + str(page))
		print(np.log10(mel_spectrum))

		export_txt(train, "trainF1AES2が")

	print("All Encoding")