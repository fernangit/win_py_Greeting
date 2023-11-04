import transfer
import jtalk
import time
import random
import utterance
import pyautogui

motionlist = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']

#ブラウザ起動しておく

jtalk.jtalk('おはようございます')
#モーションズレ補正
time.sleep(0.5)
transfer.transfer_utterance('おはようございます')
time.sleep(1)

jtalk.jtalk('こんにちわ')
#モーションズレ補正
time.sleep(0.5)
transfer.transfer_utterance('こんにちわ')
time.sleep(1)

jtalk.jtalk('こんばんわ')
#モーションズレ補正
time.sleep(0.5)
transfer.transfer_utterance('こんばんわ')
time.sleep(1)

jtalk.jtalk('おつかれさまです')
#モーションズレ補正
time.sleep(0.5)
transfer.transfer_utterance('おつかれさまです')
time.sleep(1)

jtalk.jtalk('わたしじつわいろいろしゃべれるんです')
#モーションズレ補正
time.sleep(0.5)
transfer.transfer_utterance('わたしじつわいろいろしゃべれるんです')
time.sleep(1)

while(True):
    #独り言再生
    monologue = random.randint(0, len(utterance.mono_lst) - 1)
    jtalk.jtalk(utterance.mono_lst[monologue])
    print(monologue, utterance.mono_lst[monologue])
    #モーションズレ補正
    time.sleep(0.5)
    #口パク
    transfer.transfer_utterance(utterance.mono_lst[monologue])

    time.sleep(1)
