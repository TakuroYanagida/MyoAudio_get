# --- coding:utf-8 ---
import numpy as np

def MyoAudio_correl(Myo_analysis_filename, Audio_analysis_i_filename, MyoAudio_correl_filename, start_num, end_num):
        text_f = open(MyoAudio_correl_filename, "w")
        while start_num <= end_num:

            mf = np.loadtxt(Myo_analysis_filename + str(start_num) + ".txt") #median frequency
            iv = np.loadtxt(Audio_analysis_i_filename + str(start_num) + ".txt") #between onsets intervals
            corr = np.corrcoef(mf[0:mf.size-1],iv[1:])[0, 1]

            text_f.write(str(corr))
            text_f.write("\n")

            start_num += 1
        text_f.close()

if __name__ == "__main__" :
    Myo_analysis_filename = "../data/20161219/6/analysis/myo_analysis"
    Audio_analysis_v_filename = "../data/20161219/6/analysis/Audio_velocity_analysis"
    #Audio_analysis_i_filename = "../data/20161219/1/analysis/Audio_interval_analysis"
    MyoAudio_correl_filename = "../data/20161219/6/analysis/MyoAudio_correl.txt"

    start_num = 1
    end_num = 6

    MyoAudio_correl(Myo_analysis_filename, Audio_analysis_v_filename, MyoAudio_correl_filename, start_num, end_num)
