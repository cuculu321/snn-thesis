import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

def wav_split(file_name):
    """
    音声データを0.04秒ごと、オーバーラップ50%で分割する

    Parameters
	----------
	file_name : string
        音声ファイルのパス

	Returns
	-------
    sig_data_array : list[float]
        0.04秒ごとオーバーラップ50％で分割された音声データのリスト
    """
    signal, samplerate = sf.read(file_name)

    # 音声波形を0.04毎、オーバーラップ50%で切り出す
    time_interval = 0.02 #オーバーラップ50%なので0.02秒ごと
    cuttime = 0.04 #ポイント前後0.02秒合計0.04秒
    array_interval = 0.02 * samplerate #0.02秒間隔を配列間隔に
    cutpoint = np.arange(array_interval, len(signal) - array_interval, array_interval) #0.02秒ごとのポイント切り出し

    sig_data_array = []
    time_data_array = []
    for cut_center in cutpoint:
        sig_data_array.append(signal[int(cut_center - cuttime / 2 * samplerate) : int(cut_center + cuttime / 2 * samplerate)])

    return sig_data_array, samplerate

if __name__ == '__main__':
    splited_sig_array, samplerate = wav_split("./PASL-DSR/WAVES/F1/AES/F1AES2.wav")

    time = np.arange(0, 40, 0.0625)
    x = splited_sig_array[int(len(splited_sig_array)/2)]
    plt.plot(time * 1000, x)
    plt.xlabel("time [ms]")
    plt.ylabel("amplitude")
    plt.show()