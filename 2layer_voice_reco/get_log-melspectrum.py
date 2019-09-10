import numpy as np
import matplotlib.pyplot as plt

def filter_humming(signal, samplerate):
    """
    音声データにハミング窓をかけて振幅スペクトルを得る

    Parameters
	----------
	signal : list[float]
        音声データのアナログ情報
    samplerate : int
        音声データのサンプルレート

	Returns
	-------

    """
    # ハミング窓をかける
    hamming = np.hamming(len(signal))
    ham_signal = signal * hamming

    # 振幅スペクトルを求める
    N = 2048 # FFTのサンプル数
    spec = np.abs(np.fft.fft(ham_signal, N))[:N//2]
    fscale = np.fft.fftfreq(N, d = 1.0 / samplerate)[:N//2]

    return fscale, spec

if __name__ == '__main__':
    from wav_split import wav_split
    splited_sig_array, samplerate = wav_split("./PASL-DSR/WAVES/F1/AES/F1AES2.wav")
    signal = splited_sig_array[int(len(splited_sig_array)/2)]
    fscale, spec = filter_humming(signal, samplerate)

    plt.plot(fscale, spec)
    plt.xlabel("frequency [Hz]")
    plt.ylabel("amplitude spectrum")
    plt.show()
