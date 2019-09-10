import numpy as np
import matplotlib.pyplot as plt

def filter_humming(signal, samplerate, N):
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
    spec = np.abs(np.fft.fft(ham_signal, N))[:N//2]
    fscale = np.fft.fftfreq(N, d = 1.0 / samplerate)[:N//2]

    return fscale, spec

def hz2mel(f):
    """
    周波数をメル尺度に変換

    Parameters
	----------
    f : float
        周波数

	Returns
	-------
     : float
        メル尺度
    """
    return 2595 * np.log(f / 700.0 + 1.0)

def mel2hz(m):
    """
    メル尺度を周波数に変換

    Parameters
	----------
    m : float
        メル尺度

	Returns
	-------
     : float
        周波数
    """
    return 700 * (np.exp(m / 2595) - 1.0)

if __name__ == '__main__':
    from wav_split import wav_split
    splited_sig_array, samplerate = wav_split("./PASL-DSR/WAVES/F1/AES/F1AES2.wav")
    signal = splited_sig_array[int(len(splited_sig_array)/2)]
    fscale, spec = filter_humming(signal, samplerate, N)

    plt.plot(fscale, spec)
    plt.xlabel("frequency [Hz]")
    plt.ylabel("amplitude spectrum")
    plt.show()
