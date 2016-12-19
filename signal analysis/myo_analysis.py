# --- coding:utf-8 ---

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy import hamming
import csv
import math #math.floor(x) 小数点以下切り捨て

Myo_filename = "../data/20161219/6/myo/myo_file"
Myo_analysis_filename = "../data/20161219/6/analysis/myo_analysis"
Midi_filename = "../data/20161219/6/analysis/onset_"

def do_fft(sig):
    win = hamming(sig.size)
    sig_spectrum = fft(sig * win)
    return abs(sig_spectrum[: sig.size / 2 + 1])

start_num = 1
end_num = 6

while start_num <= end_num:
    #file read
    Myo_f = open(Myo_filename + str(start_num) + ".txt", "r")
    Myo_fdata = Myo_f.read()
    Myo_f.close()

    Myo_wdata = np.array(Myo_fdata.split()) #\n \t \s split to array
    Midi_vdata = np.loadtxt(Midi_filename + str(start_num) + ".txt")

    proces_time = Myo_wdata[0].astype(np.float64) #処理時間

    data = Myo_wdata[1:].astype(np.int16) #strings 2 float
    data = data - 430
    abs_data = np.absolute(data) #for signal mean

    rate = int(data.size // proces_time) #sampling rate   rate = int(Myo_wdata[0].astype(np.float64)//4)
    j = 0

    #shift_size = rate * 1 #窓幅を秒数で指定

    f = open(Myo_analysis_filename + str(start_num) + ".txt", "w")
    #csvWriter = csv.writer(f)

    #while j <= data.size:
    while j < (Midi_vdata.size)-1:
        start_point = int(math.floor((Midi_vdata[j])*rate))
        end_point = int(math.floor((Midi_vdata[j+1])*rate))

        spectrum = do_fft(data[start_point:end_point])
        #spectrum = do_fft(data[j:j+shift_size])

        power_spectrum = spectrum ** 2
        spectrum_sum = np.sum(power_spectrum)

        find_mid = 0
        i = 0

        while find_mid < spectrum_sum/2:
            find_mid += power_spectrum[i]
            i += 1

        mid_f = i - 1

        freqList = fftfreq(data[start_point:end_point].size, d=1.0/ rate)  #周波数の分解能計算

        #print freqList.size,power_spectrum.size
        #plt.plot(power_spectrum, color = "green")
        #write_data = [0,0]

        #write_data[0] = j+1
        #write_data[1] = np.mean(abs_data[start_point:end_point])
        #write_data[2] = freqList[mid_f]
        #csvWriter.writerow(write_data)
        f.write(str(freqList[mid_f]))
        f.write("\n")


        #j += shift_size

        j += 1

    f.close()
    start_num += 1
