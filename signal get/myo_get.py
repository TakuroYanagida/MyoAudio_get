# --- coding:utf-8 ---
import serial
import threading
from time import time

ser = serial.Serial("COM3",115200)  # デバイス名とボーレートを設定しポートをオープン
MYO_OUTPUT_FILENAME = "../Myo_test.txt" #myo file name
Myo_Frames = [] #Myoelectronical signal colums

#define thread class
class control_th():

    def __init__(self):
        self.stop_event = threading.Event() #停止させるかのフラグ
        #スレッドの作成と開始
        self.thread_Myo = threading.Thread(target = self.Myo_get)
        self.thread_Myo.start()

    def Myo_get(self):
        while not self.stop_event.is_set():
            data = ser.read()
            Myo_Frames.append(data)

    def Click_output(self):
        while not self.stop_event.is_set():
            Beep(700,beeptime)
            sleep(minus_beeptime)

    def stop(self):
        #スレッドを停止させる
        self.stop_event.set()
        self.thread_Myo.join() #スレッドが停止するのを待つ

#---main program---
if __name__ == "__main__":
    #---rec part---
    raw_input("press Enter key for rec start")

    #thread start
    i = 0

    th_start_time = time() #thread start time
    print ("recording...")
    while i < 10000:
        data = ser.read()
        Myo_Frames.append(data)
        i += 1
    print ("finished recording")
    print ("wait...")

    #thread end
    th_end_time = time() #thread end time

    ser.close() # ポートのクローズ

    #Myoelectronical output
    f = open(MYO_OUTPUT_FILENAME, "w")

    Myo_getTime = th_end_time - th_start_time #Myoelectronical's time while Myo get

    outliers = "鈎b魔ﾁiｊｂﾊﾙ" #外れ値群　""の中にどんどん追加していく書式
    f.write(str(Myo_getTime)) #write time while Myo get
    for row in Myo_Frames:
        if row in ",":
            f.write("\n")
        else:
            f.write(row.translate(None, outliers)) #外れ値削除しファイルに書き込み""".translate(None, "・")"""
    f.close()

    print "finished"
