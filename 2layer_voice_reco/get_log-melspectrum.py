import numpy as np
import matplotlib.pyplot as plt

def get_mel(signal):
    # ハミング窓をかける
    hamming = np.hamming(len(signal))
    ham_signal = signal * hamming

    # 振幅スペクトルを求める
    N = 2048 # FFTのサンプル数
    spec = np.abs(np.fft.fft(ham_signal, N))[:N//2]
    fscale = np.fft.fftfreq(N, d = 1.0 / fs)[:N//2]

    plt.plot(fscale, spec)
    plt.ham_signallabel("frequency [Hz]")
    plt.ylabel("amplitude spectrum")
    plt.show()


if __name__ == '__main__':
    from wav_split import wav_split
    splited_sig_array = wav_split("./PASL-DSR/WAVES/F1/AES/F1AES2.wav")
    signal = splited_sig_array[int(len(splited_sig_array)/2)]
    get_mel(signal)
