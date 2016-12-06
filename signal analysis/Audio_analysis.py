# -*- coding: utf-8 -*-
import wave
import scipy as sp
import pylab

if __name__ == "__main__" :
    wf = wave.open("../data/Audio/sine.wav" , "r" ) #file name
    fs = wf.getframerate()  #サンプリング周波数
    x = wf.readframes(wf.getnframes())
    #x = frombuffer(x, dtype= "int16") / 32768.0  # -1 - +1に正規化
    wf.close()

    start = 0 #サンプリングする開始位置
    N = 256 #FFTのサンプル数

    X = sp.fftpack.fft(x[start:start+N]) #fft
    freqList = sp.fftpack.fftfreq(N, d=1.0/ fs) #周波数軸の値を計算

    amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]  # 振幅スペクトル
    phaseSpectrum = [np.arctan2(int(c.imag), int(c.real)) for c in X]    # 位相スペクトル

    # 振幅スペクトルを描画
    pylab.plot(freqList, amplitudeSpectrum, marker= 'o', linestyle='-')
    pylab.axis([0, fs/2, 0, 50])
    pylab.xlabel("frequency [Hz]")
    pylab.ylabel("amplitude spectrum")
