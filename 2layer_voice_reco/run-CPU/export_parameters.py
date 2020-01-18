from parameters import param as par

def export_par(output_path):
    save_path = output_path + ".txt"

    with open(save_path, mode = 'w') as save_file:
        
        save_file.write(str(par.kMelChannelCount_))
        save_file.write("音声処理から得る特徴点の数：" + str(par.kMelChannelCount_))
        save_file.write("\n")

        save_file.write("1層目の発火回数：" + str(par.kTime_))
        save_file.write("\n")

        save_file.write("2層目のニューロン数：" + str(par.kSecondLayerNuerons_))
        save_file.write("\n")

        save_file.write("epoch数：" + str(par.kEpoch_))
        save_file.write("\n")

        save_file.close()

if __name__ == "__main__":
    export_par("a")