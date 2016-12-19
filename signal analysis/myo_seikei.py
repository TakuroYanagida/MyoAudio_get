# -*- coding: utf-8 -*-

MYO_OUTPUT_FILENAME = "../data/Myo_file.txt" #myo file name

#Myoelectronical output
content = open(MYO_OUTPUT_FILENAME).read()
Scontent = content.split()

Myo_getTime = Scontent[0] #th_end_time - th_start_time #Myoelectronical's time while Myo get

f = open("seikei data/Myo_file.txt", "w")

f.write(Myo_getTime) #write time while Myo get
for row in Scontent[1:]:
    if row in ",":
        f.write("\n")
    else:
        f.write(row)
f.close()
