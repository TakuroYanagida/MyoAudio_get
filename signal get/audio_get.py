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

#countdown to rec start
for count in [4,3,2,1]:
    print count
    Beep(700,beeptime)
    sleep(minus_beeptime)

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
