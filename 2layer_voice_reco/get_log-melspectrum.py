import numpy as np
import matplotlib.pyplot as plt

def get_amplitude_spectrum(signal, samplerate, N):
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
    frequency_scale : list[float]
        周波数
    amplitude_spectrum : list[float]
        振幅スペクトル

    """
    # ハミング窓をかける
    hamming = np.hamming(len(signal))
    ham_signal = signal * hamming

    # 振幅スペクトルを求める
    amplitude_spectrum = np.abs(np.fft.fft(ham_signal, N))[:N//2]
    frequency_scale = np.fft.fftfreq(N, d = 1.0 / samplerate)[:N//2]

    return frequency_scale, amplitude_spectrum

def hz2mel(f):
    """
    周波数をメル尺度に変換
    """
    return 2595 * np.log(f / 700.0 + 1.0)

def mel2hz(m):
    """
    メル尺度を周波数に変換
    """
    return 700 * (np.exp(m / 2595) - 1.0)

def mel_filterbank(samplerate, N, melChannels):
    """メルフィルタバンクを作成"""
    # ナイキスト周波数（Hz）
    nyquist_f = samplerate / 2
    # ナイキスト周波数（mel）
    nyquist_mel = hz2mel(nyquist_f)
    # 周波数インデックスの最大数
    frequency_index_max = N // 2
    # 周波数解像度（周波数インデックス1あたりのHz幅）
    frequency_resolution = samplerate / N
    # メル尺度における各フィルタの中心周波数を求める
    dmel = nyquist_mel / (melChannels + 1)
    mel_centers = np.arange(1, melChannels + 1) * dmel
    # 各フィルタの中心周波数をHzに変換
    other_filter_centers = mel2hz(mel_centers)
    # 各フィルタの中心周波数を周波数インデックスに変換
    other_filter_center_index = np.round(other_filter_centers / frequency_resolution)
    # 各フィルタの開始位置のインデックス
    other_filter_index_start = np.hstack(([0],  other_filter_center_index[0:melChannels - 1]))
    # 各フィルタの終了位置のインデックス
    other_filter_index_stop = np.hstack(( other_filter_center_index[1:melChannels], [frequency_index_max]))
    filterbank = np.zeros((melChannels, frequency_index_max))
    for c in range(0, melChannels):
        # 三角フィルタの左の直線の傾きから点を求める
        increment= 1.0 / ( other_filter_center_index[c] - other_filter_index_start[c])
        for i in range(int(other_filter_index_start[c]), int( other_filter_center_index[c])):
            filterbank[c, i] = (i - other_filter_index_start[c]) * increment
        # 三角フィルタの右の直線の傾きから点を求める
        decrement = 1.0 / (other_filter_index_stop[c] -  other_filter_center_index[c])
        for i in range(int( other_filter_center_index[c]), int(other_filter_index_stop[c])):
            filterbank[c, i] = 1.0 - ((i -  other_filter_center_index[c]) * decrement)

    return filterbank, other_filter_centers

def get_log_melspectrum(signal, samplerate):
    """
    Parameters
	----------
	signal : list[float]
        音声データ
    samplerate : int
        サンプルレート

	Returns
	-------
    f_centers :
        抽出したメルスペクトラムの周波数
    mel_spectrum :
        メルスペクトラムのパラメータ
    """
    N = 2048
    frequency_scale, amplitude_spectrum = get_amplitude_spectrum(
                                                        signal, samplerate, N)

    melChannels = 22  # メルフィルタバンクのチャネル数
    frequency_resolution = samplerate / N   # 周波数解像度（周波数インデックス1あたりのHz幅）
    filterbank, f_centers = mel_filterbank(samplerate, N, melChannels)

    mel_spectrum = np.dot(amplitude_spectrum, filterbank.T)
    return f_centers, mel_spectrum


if __name__ == '__main__':
    from wav_split import wav_split
    splited_sig_array, samplerate = wav_split("a_1.wav")
    signal = splited_sig_array[int(len(splited_sig_array)/2)]
    
    f_centers, mel_spectrum = get_log_melspectrum(signal, samplerate)
    # 元の振幅スペクトルとフィルタバンクをかけて圧縮したスペクトルを表示
    plt.figure(figsize=(13, 5))

    plt.plot(f_centers, 10 * np.log10(mel_spectrum), "o-", label='Mel Spectrum')
    plt.xlabel("frequency[Hz]")
    plt.ylabel('Amplitude[dB]')
    plt.legend()
    plt.show()