# -*- coding: utf-8 -*-
import keyinp
import pyautogui
import time

def do():
    #ブラウザ最大化
    keyinp.send('F11')
    time.sleep(1.0)
    keyinp.send('z')
    time.sleep(1.0)
    pyautogui.click()

if __name__ == '__main__':
    do()