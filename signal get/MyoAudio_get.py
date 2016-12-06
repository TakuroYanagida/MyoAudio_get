# -*- coding: utf-8 -*-
import pyaudio
import wave
from time import sleep
from winsound import Beep
import serial
import threading
from time import time

#settings
RECORD_SECONDS = 1 #rec time[sec]
bpm = 150 #beat per minute
beeptime = 100 #click time[msec]

bpm_time = 1000.0/(bpm / 60) #time/1click[msec]
minus_beeptime = (bpm_time - beeptime)/1000.0 #wait time between clicks[sec]

WAVE_OUTPUT_FILENAME = "../data/Audio/file.wav" #wav file name
MYO_OUTPUT_FILENAME = "../data/Myo/Myo_file.txt" #myo file name

#---audio setup---
input_num = 1 #マイク入力のデバイス番号

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2**11

audio = pyaudio.PyAudio()
Audio_Frames = []
Myo_Frames = []
def Audio_Callback(in_data, frame_count, time_info, status):
    Audio_Frames.append(in_data) #この中で別スレッドの処理
    return(None, pyaudio.paContinue)

#myoelectronical(arduino) setup
ser = serial.Serial("COM3",115200) #デバイス名とボーレートを設定しポートをオープン

def Myo_get():
    while stream.is_active():
        data = ser.read()
        Myo_Frames.append(data)

th_Myo = threading.Thread(target = Myo_get, name = "th_me")

#click set up
def click_output():
    Beep(700,beeptime)
    sleep(minus_beeptime)

th_click = threading.Thread()

if __name__ == "__main__":
    #---rec part---
    raw_input("press Enter key for rec start")

    #audio & myoelectronical stream start
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    input_device_index=input_num,
                    frames_per_buffer=CHUNK,
                    stream_callback=Audio_Callback)
    start_time = time()
    th_Myo.start()

    #countdown to rec start
    for count in [4,3,2,1]:
        print count
        Beep(700,beeptime)
        sleep(minus_beeptime)

    print ("recording...")
    #stream.start_stream()
    """
    click_count = 0
    while stream.is_active():
        if click_count/(bpm / 60) >= RECORD_SECONDS: #指定秒数でループ終了
            break
        Beep(700,beeptime)
        sleep(minus_beeptime)
        click_count += 1
    """
    #raw_imput("press enter key for rec end") #
    print ("finished recording")
    print ("wait...")
    #bottom margin
    for count in [4,3,2,1]:
        sleep(minus_beeptime)

    #---output part---
    stream.stop_stream()
    stream.close()
    audio.terminate()

    th_Myo._Thread__stop()

    end_time = time()

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
    Myo_SR = len(Myo_Frames)//(end_time - start_time) #Myoelectronical sampling rate

    f.write(str(Myo_SR))
    for row in Myo_Frames:
        #write_data = row
        f.write("\n") #最初だけ改行無し
        f.write(row.translate(None, "・")) #外れ値削除しファイルに書き込み

        #print row
    print "finished"
