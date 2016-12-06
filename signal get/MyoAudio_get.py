# -*- coding: utf-8 -*-
import pyaudio
import wave
from time import sleep
from winsound import Beep
import serial
import threading
from time import time

#---settings---
#RECORD_SECONDS = 1 #rec time[sec]
bpm = 150 #beat per minute
beeptime = 100 #click time[msec]

bpm_time = 1000.0/(bpm / 60) #time/1click[msec]
minus_beeptime = (bpm_time - beeptime)/1000.0 #wait time between clicks[sec]

WAVE_OUTPUT_FILENAME = "../Audio_file.wav" #wav file name
MYO_OUTPUT_FILENAME = "../Myo_file.txt" #myo file name

Myo_Frames = [] #Myoelectronical signal colums
Audio_Frames = [] #Audio signal colums

#define thread class
class control_th():

    def __init__(self):
        self.stop_event = threading.Event() #停止させるかのフラグ

        #スレッドの作成と開始
        self.thread_Myo = threading.Thread(target = self.Myo_get)
        self.thread_click = threading.Thread(target = self.click_output)
        self.thread_Myo.start()

        #head margin countdown to rec start
        for count in [4,3,2,1]:
            print count
            Beep(700,beeptime)
            sleep(minus_beeptime)

        self.thread_click.start()

    def Myo_get(self):
        count = 1
        step = 1
        while not self.stop_event.is_set():
            data = ser.read()
            Myo_Frames.append(data)

    def click_output(self):
        while not self.stop_event.is_set():
            Beep(700,beeptime)
            sleep(minus_beeptime)

    def stop(self):
        """スレッドを停止させる"""
        self.stop_event.set()
        self.thread_Myo.join()    #スレッドが停止するのを待つ
        self.thread_click.join()    #スレッドが停止するのを待つ

#---audio setup---
input_num = 1 #マイク入力のデバイス番号

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2**11

def Audio_Callback(in_data, frame_count, time_info, status):
    Audio_Frames.append(in_data) #この中で別スレッドの処理
    return(None, pyaudio.paContinue)

#myoelectronical(arduino) setup
ser = serial.Serial("COM3",115200) #デバイス名とボーレート（arduino側も同じ数値に要設定）を設定しポート

if __name__ == "__main__":
    audio = pyaudio.PyAudio()

    #---rec part---
    raw_input("press Enter key for rec start")

    #audio & myoelectronical stream start
    stream = audio.open(format = FORMAT, channels = CHANNELS,
                        rate = RATE, input = True,
                        input_device_index = input_num,
                        frames_per_buffer = CHUNK,
                        stream_callback = Audio_Callback)
    th_start_time = time() #thread start time

    #thread start
    thread_do = control_th()

    #th_Myo.start()
    print ("recording...")
    #stream.start_stream()
    """
    #指定秒数で録音終了
    click_count = 0
    while stream.is_active():
        if click_count/(bpm / 60) >= RECORD_SECONDS: #指定秒数でループ終了
            break
        Beep(700,beeptime)
        sleep(minus_beeptime)
        click_count += 1
    """
    raw_input("press enter key for rec end") #rec end by press enter
    print ("finished recording")
    print ("wait...")

    #bottom margin
    for count in [4,3,2,1]:
        sleep(minus_beeptime)

    #thread end
    thread_do.stop()
    th_end_time = time() #thread end time

    #---output part---
    stream.stop_stream()
    stream.close()
    audio.terminate()

    ser.close() #ポートのクローズ

    #Audio output
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Audio_Frames))
    waveFile.close()

    #Myoelectronical output
    f = open(MYO_OUTPUT_FILENAME, "w")

    outliers = "・" #外れ値群　""の中にどんどん追加していく書式

    #f.write(Myo_Frames[0].translate(None, outliers))
    Myo_SR = len(Myo_Frames)//(th_end_time - th_start_time) #Myoelectronical sampling rate

    f.write(str(Myo_SR)) #write sampling rate
    for row in Myo_Frames:
        #write_data = row
        f.write("\n")
        #f.write(row)
        f.write(row.translate(None, "・")) #外れ値削除しファイルに書き込み

        #print row
    print "finished"
