# -*- coding: utf-8 -*-
import pyaudio
import wave
from time import sleep
from winsound import Beep
import serial
import threading
from time import time
import pygame.midi

#---settings---
MYO_OUTPUT_FILENAME = "../data/20161219/5/myo/myo_file1.txt" #myo file name

Myo_Frames = [] #Myoelectronical signal colums

th_start_time = time() #thread start time

#myoelectronical(arduino) setup
ser = serial.Serial("COM3",115200) #デバイス名とボーレート（arduino側も同じ数値に要設定）

#define thread class
class control_th():

    def __init__(self):
        self.stop_event = threading.Event() #停止させるかのフラグ

        #スレッドの作成と開始
        th_start_time = time() #thread start time
        #print "time = " + str(time())
        self.thread_Myo = threading.Thread(target = self.Myo_get)
        self.thread_Myo.start()

    def Myo_get(self):
        count = 0
        while not self.stop_event.is_set():
            if count >= 10000:
                #print "time = " + str(time())
                print (10000/4)/(time() - th_start_time)
                count = 0
            else:
                count += 1
            data = ser.read()
            Myo_Frames.append(data)

    def stop(self):
        #スレッドを停止させる
        self.stop_event.set()
        self.thread_Myo.join() #スレッドが停止するのを待つ
        #self.thread_Midi.join() #スレッドが停止するのを待つ


#---main program---
if __name__ == "__main__":
    audio = pyaudio.PyAudio()

    #---rec part---
    raw_input("press Enter key for rec start")

    th_start_time = time() #thread start time

    #thread start
    thread_do = control_th()

    print ("recording...")
    raw_input("press enter key for rec end") #rec end by press enter
    print ("finished recording")
    print ("wait...")

    #thread end
    thread_do.stop()
    th_end_time = time() #thread end time
    print (len(Myo_Frames)/4)/(th_end_time - th_start_time)

    #---output part---
    ser.close() #シリアルポートのクローズ

    #Myoelectronical output
    f = open(MYO_OUTPUT_FILENAME, "w")

    Myo_getTime = th_end_time - th_start_time #Myoelectronical's time while Myo get

    outliers = "鈎b魔ﾁiｊｂﾊﾙ" #外れ値群　""の中にどんどん追加していく書式
    f.write(str(Myo_getTime)) #write time while Myo get
    f.write("\n")
    for row in Myo_Frames:
        if row in ",":
            f.write("\n")
        else:
            f.write(row.translate(None, outliers)) #外れ値削除しファイルに書き込み""".translate(None, "・")"""
    f.close()

    print "finished"
