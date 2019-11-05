

####################################################### README ####################################################################

# This is the main file which calls all the functions and trains the network by updating weights


#####################################################################################################################################

import numpy as np
import cupy as cp
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
from wav_split import wav_split

def learning():
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

        #synapse matrix initialization
        synapse = np.zeros((par.kSecondLayerNuerons_, par.kFirstLayerNuerons_))

        #get wavefile path for learning
        learning_path = get_learning_small_file_path()

        for i in range(par.kSecondLayerNuerons_):
                for j in range(par.kFirstLayerNuerons_):
                        synapse[i][j] = random.uniform(0, 0.4 * par.kScale_)


        synapse_GPU = cp.asarray(synapse)

        for epoch in range(1):
                for wave_file in learning_path:
                #for wave_file in ["sounddata\F1\F1SYB01_が.wav"]:
                        resemble_print(str(wave_file) + "  " + str(epoch))

                        #音声データの読み込み
                        splited_sig_array, samplerate = wav_split(str(wave_file))
                        resemble_print(str(wave_file))

                        for signal in splited_sig_array:
                                #Generating melspectrum
                                f_centers, mel_spectrum = get_log_melspectrum(signal, samplerate)

                                #Generating spike train
                                spike_train = np.array(encode(np.log10(mel_spectrum)))
                                spike_train_GPU = cp.asarray(spike_train)
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
                                                                                                                synapse_GPU[second_layer_position], spike_train_GPU[:, time]
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
                                                                                if spike_train_GPU[first_layer_position][time + back_time] == 1:
                                                                                        # resemble_print "weight change by" + str(update(synapse[j][h], rl(t1)))
                                                                                        synapse_GPU[second_layer_position][first_layer_position] = update(
                                                                                                synapse_GPU[second_layer_position][first_layer_position], rl(back_time)
                                                                                                )
                                                                #後シナプスの計算
                                                                for fore_time in range(2, par.kTimeFore_+1, 1): # 2 → 20
                                                                        if 0 <= time + fore_time<par.kTime_+1:
                                                                                if spike_train_GPU[first_layer_position][time + fore_time] == 1:
                                                                                        # resemble_print "weight change by" + str(update(synapse[j][h], rl(t1)))
                                                                                        synapse_GPU[second_layer_position][first_layer_position] = update(
                                                                                                synapse_GPU[second_layer_position][first_layer_position], rl(fore_time)
                                                                                                )

                                if(img_win!=100):
                                        for first_layer_position in range(par.kFirstLayerNuerons_):
                                                if sum(spike_train_GPU[first_layer_position]) == 0:
                                                        synapse_GPU[img_win][first_layer_position] -= 0.06 * par.kScale_
                                                        if(synapse_GPU[img_win][first_layer_position] < par.kMinWait_):
                                                                synapse_GPU[img_win][first_layer_position] = par.kMinWait_

        synapse = cp.asnumpy(synapse_GPU)
        return potential_lists, synapse, layer2


if __name__ == "__main__":
        from record_synapse import *
        import random
        from get_current_directory import get_mappingfile_path
        from mapping import *

        potential_lists, synapse, layer2 = learning()

        resemble_print("synapse : ")
        resemble_print(synapse)
        export_txt(synapse, "synapse_record/" + create_timestamp())

        secondhand_wav_file = []
        speaker_list = [i for i in range(0, 12)]

        mapping_list = [[] for _ in range(110)]

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