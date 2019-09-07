import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

def wav_split(file_name):
    signal, samplerate = sf.read(file_name)

    t = np.arange(0, len(signal) / samplerate, 1/samplerate)

    # 音声波形を0.04毎、オーバーラップ50%で切り出す
    time_interval = 0.02 #オーバーラップ50%なので0.02秒ごと
    cuttime = 0.04 #ポイント前後0.02秒合計0.04秒
    array_interval = 0.02 * samplerate #0.02秒間隔を配列間隔に
    cutpoint = np.arange(array_interval, len(signal) - array_interval, array_interval) #0.02秒ごとのポイント切り出し

    sig_data_array = []
    time_data_array = []
    for cut_center in cutpoint:
        sig_data_array.append(signal[int(cut_center - cuttime / 2 * samplerate) : int(cut_center + cuttime / 2 * samplerate)])
        time_data_array.append(t[int(cut_center - cuttime/2*samplerate) : int(cut_center + cuttime/2*samplerate)])

    return sig_data_array, time_data_array

if __name__ == '__main__':
    splited_sig_array, splited_time_array = wav_split("./PASL-DSR/WAVES/F1/AES/F1AES2.wav")

    time = splited_time_array[int(len(splited_time_array)/2)]
    x = splited_sig_array[int(len(splited_sig_array)/2)]
    plt.plot(time * 1000, x)
    plt.xlabel("time [ms]")
    plt.ylabel("amplitude")
    plt.show()