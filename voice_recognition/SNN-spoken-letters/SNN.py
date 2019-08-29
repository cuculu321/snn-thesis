from random import shuffle
import os
import sys
import Utils
import Network
import pyspike as spk
from pyspike import SpikeTrain
from datetime import datetime
from matplotlib import pyplot as plt
from neuronpy.graphics import spikeplot

prototype_trains = [None] * 3

def write_weights(network):
    i = 0
    with open("weights.txt", "a") as f:
        for out in network.output_layer:
            if i == 0:
                f.write("B\n")
            elif i == 1:
                f.write("D\n")
            elif i == 2:
                f.write("G\n")
            elif i == 3:
                f.write("K\n")
            elif i == 4:
                f.write("P\n")
            elif i == 5:
                f.write("T\n")
            for syn in out.synapses:
                if i == 0:
                    f.write("%s\n" % syn.w)
                    i = 1
                else:
                    f.write("%s\n" % syn.w)
                    i = 0
            i += 1

def print_result(results):
    """
    結果の出力

    Parameters
    ----------
    results : list[int]
        出力ニューロンの出力したスパイク列
    """
    print('\tB: ' + str(results[0]))
    print('\tD: ' + str(results[1]))
    print('\tG: ' + str(results[2]))
    print('\tK: ' + str(results[3]))
    print('\tP: ' + str(results[4]))
    print('\tT: ' + str(results[5]))

# Generate a spike train from the given spike
def generate_prototypes(spike, key):
    global prototype_trains
    spike_train = SpikeTrain(spike, [0.0, 500.0])
    if key == 'B':
        prototype_trains[0] = spike_train
    elif key == 'D':
        prototype_trains[1] = spike_train
    elif key == 'G':
        prototype_trains[2] = spike_train
    elif key == 'K':
        prototype_trains[3] = spike_train
    elif key == 'P':
        prototype_trains[4] = spike_train
    elif key == 'T':
        prototype_trains[5] = spike_train

def spike_analysis(spikes, value):
    distances = []
    letters = ['B', 'D', 'G', 'K', 'P', 'T']
    i = 0
    for spike in spikes:
        spike_train = SpikeTrain(spike, [0.0, 500.0])
        isi_profile = spk.spike_sync(prototype_trains[i], spike_train)
        print("\t%s: " % letters[i] + str(isi_profile))
        distances.append(isi_profile)
        i += 1

    val, idx = max((val, idx) for (idx, val) in enumerate(distances))
    print("Distance: %.8f" % val)
    print("Index: %s" % idx)


def show_plots(time, v_plts, currents, spikes):
    plt.figure('B')
    plt.plot(time, v_plts[0], 'g-')
    plt.figure('D')
    plt.plot(time, v_plts[1], 'b-')
    plt.figure('G')
    plt.plot(time, v_plts[2], 'k-')
    plt.figure('K')
    plt.plot(time, v_plts[3], 'r-')
    plt.figure('P')
    plt.plot(time, v_plts[4], 'm-')
    plt.figure('T')
    plt.plot(time, v_plts[5], 'c-')

    sp = spikeplot.SpikePlot()
    sp.plot_spikes(spikes)
    plt.show()

# Test our network
def test():
    global prototype_trains
    global test_trains
    prototype_trains = [None] * 6
    test_trains = [None] * 6

    weights = "weights.txt"

    network = Network.Network(weights=weights)
    audio_path = "letter_audio/speech/isolet3"

    audio = [os.path.join(root, name)
                 for root, dirs, files in os.walk(audio_path)
                 for name in files
                 if name.endswith((".wav"))]
    
    mapping = dict()
    for fname in audio:
        mapping[fname] = Utils.get_label(fname)

    test_dict = dict()
    for fname in audio:
        test_dict[fname] = Utils.get_label(fname)

    b_count = 1
    d_count = 1
    g_count = 1
    k_count = 1
    p_count = 1
    t_count = 1
    count = 6

    for key in mapping:
        if mapping[key] == 'B' and b_count != 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            b_count -= 1
            count -= 1
            if b_count == 0:
                generate_prototypes(spikes[0], 'B')
                # Generate a spike train for the 'B' sound

        elif mapping[key] == 'D' and d_count != 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            d_count -= 1
            count -= 1
            if d_count == 0:
                # Generate a spike train for the 'D' sound
                generate_prototypes(spikes[1], 'D')

        elif mapping[key] == 'G' and g_count != 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            g_count -= 1
            count -= 1
            if g_count == 0:
                # Generate a spike train for the 'G' sound
                generate_prototypes(spikes[2], 'G')

        elif mapping[key] == 'K' and k_count != 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            k_count -= 1
            count -= 1
            if k_count == 0:
                # Generate a spike train for the 'K' sound
                generate_prototypes(spikes[3], 'K')

        elif mapping[key] == 'P' and p_count != 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            p_count -= 1
            count -= 1
            if p_count == 0:
                # Generate a spike train for the 'P' sound
                generate_prototypes(spikes[4], 'P')

        elif mapping[key] == 'T' and t_count != 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            t_count -= 1
            count -= 1
            if t_count == 0:
                # Generate a spike train for the 'T' sound
                generate_prototypes(spikes[5], 'T')

    print_result(results)
    spike_analysis(spikes, value)

    # Display our prototype spike trains
    sp = spikeplot.SpikePlot()
    sp.plot_spikes(prototype_trains, label="Prototypes")

    b_count = 10
    d_count = 10
    g_count = 10
    k_count = 10
    p_count = 10
    t_count = 10
    for key in test_dict:
        if test_dict[key] == 'B' and b_count != 0:
            print("Testing %s" % key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            b_count -= 1
            spike_analysis(spikes)
            if b_count == 0:
                # Generate a spike train for the 'B' sound and find a match
                generate_test_signatures(spikes[0], 'P')

        elif test_dict[key] == 'D' and d_count != 0:
            print("Testing %s" % key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            d_count -= 1
            spike_analysis(spikes)
            if d_count == 0:
                # Generate a spike train for the 'D' sound and find a match
                generate_test_signatures(spikes[1], 'D')

        elif test_dict[key] == 'G' and g_count != 0:
            print("Testing %s" % key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            g_count -= 1
            spike_analysis(spikes)
            if g_count == 0:
                # Generate a spike train for the 'G' sound and find a match
                generate_test_signatures(spikes[2], 'G')

        elif test_dict[key] == 'K' and k_count != 0:
            print("Testing %s" % key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            k_count -= 1
            spike_analysis(spikes)
            if k_count == 0:
                # Generate a spike train for the 'K' sound and find a match
                generate_test_signatures(spikes[3], 'K')

        elif test_dict[key] == 'P' and p_count != 0:
            print("Testing %s" % key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            p_count -= 1
            spike_analysis(spikes)
            if p_count == 0:
                # Generate a spike train for the 'P' sound and find a match
                generate_test_signatures(spikes[4], 'P')

        elif test_dict[key] == 'T' and t_count != 0:
            print("Testing %s" % key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            t_count -= 1
            spike_analysis(spikes)
            if t_count == 0:
                # Generate a spike train for the 'T' sound and find a match
                generate_test_signatures(spikes[5], 'T')

    # Display our last round of test spikes
    sp = spikeplot.SpikePlot()
    sp.plot_spikes(test_trains, label="Test")



def train():
    """
    学習を行う
    """
    network = Network.Network(weights=None)

    mapping = dict()

    audio_path = "letter_audio/speech/isolet1"

    # Gets list of all audio files in the directory
    audio = [os.path.join(root, name)
             for root, dirs, files in os.walk(audio_path)
             for name in files
             if name.endswith((".wav"))]
    print(audio)

    audio_path = "letter_audio/speech/isolet2"
    audio2 = [os.path.join(root, name)
              for root, dirs, files in os.walk(audio_path)
              for name in files
              if name.endswith((".wav"))]
    audio.extend(audio2)

    shuffle(audio)

    # Get a mapping of labels to audio
    for fname in audio:
        mapping[fname] = Utils.get_label(fname)

    print(datetime.now())

    b_count = 20
    d_count = 20
    g_count = 20
    k_count = 20
    p_count = 20
    t_count = 20

    for key in mapping:
        if mapping[key] == 'B' and b_count > 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            network.conduct_training(0)
            b_count -= 1
        elif mapping[key] == 'D' and d_count > 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            network.conduct_training(1)
            d_count -= 1
        elif mapping[key] == 'G' and g_count > 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            network.conduct_training(2)
            g_count -= 1
        elif mapping[key] == 'K' and k_count > 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            network.conduct_training(3)
            k_count -= 1
        elif mapping[key] == 'P' and p_count > 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            network.conduct_training(4)
            p_count -= 1
        elif mapping[key] == 'T' and t_count > 0:
            print(key)
            results, currents, time, v_plts, spikes = network.start(key)
            print_result(results)
            network.conduct_training(5)
            t_count -= 1

    write_weights(network)
    print(datetime.now())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'train':
            print('Training...')
            train()
        else:
            print('Testing')
            test()


