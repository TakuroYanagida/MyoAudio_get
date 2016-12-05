# -*- coding: utf-8 -*-
"""
import sys
import pyaudio

#インデックス番号の確認

p = pyaudio.PyAudio()
count = p.get_device_count()
devices = []
for i in range(count):
    devices.append(p.get_device_info_by_index(i))

for i, dev in enumerate(devices):
    print (i, dev['name'])

#octa-capture input num 1=1 2=9
"""
import pyaudio
import wave
from time import sleep
from winsound import Beep

input_num = 1 #マイク入力のデバイス番号

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2**11
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()
frames = []
def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)          #この中で別スレッドの処理
    return(None, pyaudio.paContinue)

raw_input("press Enter key")
print("4")
Beep(700,100)
sleep(0.9)
print("3")
Beep(700,100)
sleep(0.9)
print("2")
Beep(700,100)
sleep(0.9)
print("1")
Beep(700,100)
sleep(0.9)
print ("recording...")
#stream.start_stream()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    input_device_index=input_num,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)
sleep(RECORD_SECONDS)
print ("finished recording")

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

"""
import pyaudio
import wave
import time

imput_num1 = 1
imput_num2 = 9

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2**11
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME1 = "file1.wav"
WAVE_OUTPUT_FILENAME2 = "file2.wav"

audio = pyaudio.PyAudio()
frames1 = []
frames2 = []
def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)          #この中で別スレッドの処理
    return(None, pyaudio.paContinue)

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                input_device_index=input_num,
                frames_per_buffer=CHUNK,
                stream_callback=callback)

print ("recording...")
stream.start_stream()
time.sleep(RECORD_SECONDS)
print ("finished recording")

stream.stop_stream()
stream.close()
audio.terminate()

waveFile1 = wave.open(WAVE_OUTPUT_FILENAME1, 'wb')
waveFile2 = wave.open(WAVE_OUTPUT_FILENAME2, 'wb')

waveFile1.setnchannels(CHANNELS)
waveFile2.setnchannels(CHANNELS)

waveFile1.setsampwidth(audio.get_sample_size(FORMAT))
waveFile2.setsampwidth(audio.get_sample_size(FORMAT))

waveFile1.setframerate(RATE)
waveFile2.setframerate(RATE)

waveFile1.writeframes(b''.join(frames1))
waveFile2.writeframes(b''.join(frames2))

waveFile1.close()
waveFile2.close()
"""
