############################################## README #################################################

# This calculates threshold for an image depending upon its spiking activity.

########################################################################################################


import numpy as np
from spike_train import encode
from parameters import param as par

def threshold(train):
        """
        1Clock時に発火したニューロンの数の合計を計測し、閾値(膜電位)を決定する

        Parameters
        ----------
        train : boolean list[784, 200]
                畳み込みデータの値によって、スパイク率を変えて出力された配列データ。

        Returns
        -------
        (thresh / 3) * par.kScale_ : float
                閾値
        """

        tu = np.shape(train[0])[0]
        thresh = 0
        for i in range(tu):
                simul_active = sum(train[:, i])
                #print(train[:,i])
                if simul_active > thresh:
                        thresh = simul_active

        return (thresh / par.kSecondLayerNuerons_) * par.kScale_


if __name__ == '__main__':

        from wav_split import wav_split
        from get_logmelspectrum import get_log_melspectrum

        splited_sig_array, samplerate = wav_split("sounddata/F1SYB01_あ.wav")
        signal = splited_sig_array[int(len(splited_sig_array)/2)]
        #print(signal)
        f_centers, mel_spectrum = get_log_melspectrum(signal, samplerate)

        train = np.array(encode(signal))
        print(threshold(train))