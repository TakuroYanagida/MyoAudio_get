# --- coding:utf-8 ---

import serial
ser = serial.Serial("COM3",115200)  # デバイス名とボーレートを設定しポートをオープン

print (ser.portstr)
a = ser.read()

print a

ser.close() # ポートのクローズ
