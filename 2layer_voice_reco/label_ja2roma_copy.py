import shutil
from pykakasi import kakasi

import pathlib
import glob
import re

def get_mappingfile_path():
    """
    対応づけに使う音声ファイルのパスを取得する

    Parameters
	----------

	Returns
	-------
    対応づけに使う音声ファイルのパス
    """

    path_PASLDSR = pathlib.Path('sounddata')

    path_speaker = list(path for path in path_PASLDSR.iterdir() 
                                    if not "DS_Store" in str(path))

    path_wavefile = []
    for speaker in path_speaker:
        path_wavefile.append(list(path for path in speaker.glob('*.wav')
                                    if "SYB" in str(path)))
    return path_wavefile

if __name__ == "__main__":
    kakasi = kakasi()

    kakasi.setMode('H', 'a')
    kakasi.setMode('K', 'a')
    kakasi.setMode('J', 'a')

    conv = kakasi.getConverter()

    file_path = get_mappingfile_path()

    print(file_path)

    for path in file_path:
        for p in path:
            p = str(p)
            underbar_index = p.find("_")
            rename_path = p[10:underbar_index + 1]
            ja_label = p[underbar_index + 1 : len(p) - 4]

            print(conv.do(ja_label))
            shutil.copy(p, "Ubuntu/" + str(rename_path) + conv.do(ja_label) + ".wav")