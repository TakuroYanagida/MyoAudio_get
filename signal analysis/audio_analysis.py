# -*- coding: utf-8 -*-
import wave
import numpy as np
import scipy.fftpack
import pylab

if __name__ == "__main__" :
    wf = wave.open("../sine.wav" , "r" )
    fs = wf.getframerate()  # サンプリング周波数
    x = wf.readframes(wf.getnframes())
    #x = frombuffer(x, dtype= "int16") / 32768.0  # -1 - +1に正規化
    wf.close()

    start = 0 # サンプリングする開始位置
    N = 256 # FFTのサンプル数

    X = scipy.fftpack.fft(x[start:start+N]) #fft

    freqList = scipy.fftpack.fftfreq(N, d=1.0/ fs) #周波数軸の値を計算

    amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X] #振幅スペクトル
    #phaseSpectrum = [np.arctan2(int(c.imag), int(c.real)) for c in X] #位相スペクトル

    # 振幅スペクトルを描画
    #pylab.subplot(311)
    pylab.plot(freqList, amplitudeSpectrum, marker= 'o', linestyle='-')
    pylab.axis([0, fs/2, 0, 50])
    pylab.xlabel("frequency [Hz]")
    pylab.ylabel("amplitude spectrum")

    """
    # 位相スペクトルを描画
    pylab.subplot(312)
    pylab.plot(freqList, phaseSpectrum, marker= 'o', linestyle='-')
    pylab.axis([0, fs/2, -np.pi, np.pi])
    pylab.xlabel("frequency [Hz]")
    pylab.ylabel("phase spectrum")
    """

    show()
