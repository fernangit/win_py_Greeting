# -*- coding: utf-8 -*-
import sys
import os
import time
import random
import keyboard
import pyautogui
import winsound
import threading

motion_list = ['c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x']
response1_list = ['d', 'f', 'g', 'q', 'r', 'v', 'w']
response1_dict = {'d':1, 'f':2, 'g':3, 'q':10, 'r':11, 'v':14, 'w':15}
response2_list = ['h', 'j', 'k']
response2_dict = {'h':4, 'j':5, 'k':6}
#注：dance_listとsound_listの配列番号は対応させること
dance_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
sound_list = ['./source/sound1.wav',
              './source/sound2.wav',
              './source/sound3.wav',
              './source/sound4.wav',
              './source/sound5.wav',
              './source/sound6.wav',
              './source/sound7.wav',
              './source/sound8.wav',
              './source/sound9.wav']

#起動時モーション
def set_first_motion():
    keyboard.send('b')
#    print("keyboard.send('b')")

#Sleepモーション
def set_sleep_motion():
    keyboard.send('y')

#Response1モーション
def set_response1_motion():
    res_key = response1_list[random.randint(0, len(response1_list)-1)]
    keyboard.send(res_key)
    return res_key

#Response2モーション
def set_response2_motion():
    res_key = response2_list[random.randint(0, len(response2_list)-1)]
    keyboard.send(res_key)
    return res_key

#所定時刻の所定モーション呼び出し
def set_default_motion(now_time):
    global thread
    if thread.is_alive() == False:
        if now_time.hour == 8 and now_time.minute == 26 and now_time.second == 21:
            #8:26 ラジオ体操
            if os.path.isfile(sound_list[0]) == True:
                #BGM再生
                thread = threading.Thread(target=playSound, args=(sound_list[0],))
                thread.start()
                #モーションズレ補正
                time.sleep(0.2)
            keyboard.send('1')
            if os.path.isfile(sound_list[0]) == True:
                #音声終了待ち
                thread.join()
        if now_time.hour == 12 and now_time.minute == 30 and now_time.second == 0:
            #12:30 昼休み
            keyboard.send('b')
            winsound.PlaySound('昼休み.wav',  winsound.SND_FILENAME)
        if now_time.hour == 17 and now_time.minute == 00 and now_time.second == 0:
            #17:00 ダンスの時間
            motion = random.randint(1, len(dance_list) - 1)
            if os.path.isfile(sound_list[motion]) == True:
                #BGM再生
                thread = threading.Thread(target=playSound, args=(sound_list[motion],))
                thread.start()
                #モーションズレ補正
                time.sleep(0.2)
            keyboard.send(dance_list[motion])
            if os.path.isfile(sound_list[motion]) == True:
                #音声終了待ち
                thread.join()

#レベル対応モーション呼び出し
def set_level_motion(level):
    print('level:', level)
    if level > len(motion_list) - 1:
        level = len(motion_list) - 1
    keyboard.send(motion_list[level])
#    print("keyboard.send(motion_list[level])")

#GOOD JOBモーション呼び出し
def set_goodjob_motion():
    keyboard.send(motion_list[16])
#    print("keyboard.send(motion_list[16])")

#バイバイモーション呼び出し
def set_byebye_motion():
    keyboard.send(motion_list[2])
#    print("keyboard.send(motion_list[2])")

#モーション数
def get_motion_num():
    return len(motion_list)

def playSound(soundPath):
    winsound.PlaySound(soundPath,  winsound.SND_FILENAME)

#スレッドの二重起動防止用
thread = threading.Thread(target=playSound, args=(sound_list[0],))

if __name__ == '__main__':
    args = sys.argv
    if 1 <= len(args):
        print("sound " + sound_list[int(args[1])])
        time.sleep(1)
        if os.path.isfile(sound_list[int(args[1])]) == True:
            thread = threading.Thread(target=playSound, args=(sound_list[int(args[1])],))
            thread.start()
            #モーションズレ補正
            time.sleep(0.2)
            keyboard.send(dance_list[int(args[1])])
            print("key press " + dance_list[int(args[1])])
            time.sleep(0.1)
            #ブラウザ最大化
            keyboard.send('F11')
            print("key press F11")
            time.sleep(1.0)
            keyboard.send('z')
            print("key press z")
            time.sleep(1.0)
            pyautogui.click()
            thread.join()
        else:
            print(sound_list[int(args[1])] + " is not exist.")
