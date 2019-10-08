import pathlib
import glob
import re

def get_wavefile_path():
    path_PASLDSR = pathlib.Path('PASL-DSR')
    path_wavefile = list(path for path in path_PASLDSR.glob('**/**/*.wav')
                                if "ATR" not in str(path)
                                if "SYB" not in str(path))
    return path_wavefile

if __name__ == "__main__":
    get_wavefile_path()
