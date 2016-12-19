# -*- coding: utf-8 -*-
import wave
import numpy as np
import scipy.fftpack
import pylab
import csv
import math #math.floor(x) 小数点以下切り捨て
import pylab

#wavファイル名　midiファイル名 ファイル繰り返しスタート番号　エンド番号
def WavAnalysis(Wav_filename, Audio_analysis_filename_v, Audio_analysis_filename_i, Onset_filename, start_num, end_num):
    while start_num <= end_num:
        wf = wave.open(Wav_filename + str(start_num) + ".wav" , "r" )
        rate = wf.getframerate()  # サンプリング周波数
        x = wf.readframes(wf.getnframes())
        x = pylab.frombuffer(x, dtype= "int16")
        wf.close()

        onset_data = np.loadtxt(Onset_filename + str(start_num) + ".txt")
        text_v = open(Audio_analysis_filename_v + str(start_num) + ".txt", "w")
        text_i = open(Audio_analysis_filename_i + str(start_num) + ".txt", "w")

        j = 0

        while j < (onset_data.size)-1:
            start = int(math.floor(onset_data[j]*rate)) #サンプリングする開始位置
            end = int(math.floor(onset_data[j+1]*rate)) #サンプリングする終了位置
            N = end - start #FFTのサンプル数

            row_sum = 0
            for row in x[start:end]:
                row_sum += abs(row)

            text_v.write(str(row_sum/len(x[start:end]))) #振幅平均
            text_v.write("\n")
            text_i.write(str(onset_data[j+1] - onset_data[j])) #インターバル
            text_i.write("\n")

            j += 1

        text_v.close()
        text_i.close()

        start_num += 1

if __name__ == "__main__" :
    start_num = 1
    end_num = 6

    Wav_filename = "../data/20161219/1/audio/audio_file"
    #Midi_filename = "../data/Midi_data/Midi_file"
    Onset_filename = "../data/20161219/1/analysis/onset_"
    Audio_analysis_filename_v = "../data/20161219/1/analysis/Audio_velocity_analysis"
    Audio_analysis_filename_i = "../data/20161219/1/analysis/Audio_interval_analysis"

    WavAnalysis(Wav_filename, Audio_analysis_filename_v, Audio_analysis_filename_i, Onset_filename, start_num, end_num)
