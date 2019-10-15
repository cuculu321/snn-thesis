import pathlib
import glob
import re

def get_learningfile_path():
    """
    学習に使う音声ファイルのパスを取得する

    Parameters
	----------

	Returns
	-------
    学習に使う音声ファイルのパス
    """

    path_PASLDSR = pathlib.Path('PASL-DSR')
    path_wavefile = list(path for path in path_PASLDSR.glob('**/**/*.wav')
                                if "ATR" not in str(path)
                                if "SYB" not in str(path))
    return path_wavefile

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

    path_speaker = list(path_PASLDSR.iterdir())

    path_wavefile = []
    for speaker in path_speaker:
        path_wavefile.append(list(path for path in speaker.glob('*.wav')
                                    if "SYB" in str(path)))

    return path_wavefile

def get_testfile_path():
    """
    テストに使う音声ファイルのパスを取得する

    Parameters
	----------

	Returns
	-------
    テストに使う音声ファイルのパス
    """

    path_PASLDSR = pathlib.Path('PASL-DSR')
    path_wavefile = list(path for path in path_PASLDSR.glob('**/**/*.wav')
                                if "ATR" in str(path))
    return path_wavefile

if __name__ == "__main__":
    mapping_filelist = get_mappingfile_path()
    print(mapping_filelist[0][1])
