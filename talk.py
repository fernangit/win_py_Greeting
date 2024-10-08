import sys
import random
import time
import jtalk
import utterance
import transfer
import threading
import glob
import os

#起動時
def opening():
    jtalk.jtalk('えむず　あいさつユニット　しどうっ')

#独り言
def monologue(now_time, nxt_h, nxt_m):
    if now_time.hour == nxt_h and now_time.minute == nxt_m:
        #独り言再生
        mono = random.randint(0, len_utterance_mono_lst() - 1)
        talk(utterance.mono_lst[mono])
        #モーションズレ補正
        time.sleep(2.0)
        #口パク
        transfer.transfer_utterance(utterance.mono_lst[mono])
        time.sleep(3)
        nxt_h = now_time.hour + 1
        nxt_m = random.randint(0, 59)

    return nxt_h, nxt_m

#フィラー
def filler():
    fill = random.randint(0, len_utterance_filler_lst() - 1)
    talk(utterance.filler_lst[fill])

#定時アナウンス
def announce(now_time, nxt_h, nxt_m, sentence_file):
    if now_time.hour == nxt_h and now_time.minute == nxt_m:
        read_sentence_file(sentence_file)
        time.sleep(3)

#挨拶
def greeting(now_time, name, op):
    if (now_time.hour > 5) and (now_time.hour < 11):
        #午前
        lst_len = len(utterance.mng_lst)
        rnd = random.randint(0, lst_len + 5)
        if rnd > (lst_len - 1):
            utter = name + '　' + utterance.morning + '　' + op
        else:
            utter = name + '　' + utterance.mng_lst[rnd] + '　' + op
    else:
        #午後
        lst_len = len(utterance.evg_lst)
        rnd = random.randint(0, lst_len + 5)
        if rnd > (lst_len - 1):
            utter = name + '　' + utterance.evening + '　' + op
        else:
            utter = name + '　' + utterance.evg_lst[rnd] + '　' + op

    talk(utter)
    return utter

#読み上げ
def read_sentence():
#    print("read_sentence")
    thread = threading.Thread(target = read_sentence_thread)
    thread.start()

def read_sentence_thread():
    #sentenceフォルダ読み込み
    sentence_files = glob.glob('sentences/*.txt')
    while(True):
        for sentence_file in sentence_files:
            read_sentence_file(sentence_file)
            time.sleep(5)
        time.sleep(180)

def read_sentence_file(sentence_file):
    #ファイル有無チェック
    if os.path.isfile(sentence_file):
        with open(sentence_file, encoding="utf-8") as f:
            read_text(f.read())

def read_text(text):
    print(text)
    talk(text)
    #モーションズレ補正
    time.sleep(0.2)
    #口パク
    transfer.transfer_utterance(text)
    #読み上げ終了待ち
    while(True):
        if transfer.is_talkend():
            break
        time.sleep(1)

#発話
def talk(sentence):
    #発話再生
    thread = threading.Thread(args=(sentence, ), target = jtalk_thread)
    thread.start()

def jtalk_thread(sentence):
    jtalk.jtalk(sentence)

def percentage_to_level(per, thresh, motion_num):
    return transfer.transfer_percentage(per, thresh, motion_num)

def level_to_utterance(level):
    return utterance.op_lst[level]

def len_utterance_mng_lst():
    return len(utterance.mng_lst)

def len_utterance_evg_lst():
    return len(utterance.evg_lst)

def len_utterance_mono_lst():
    return len(utterance.mono_lst)

def len_utterance_op_lst():
    return len(utterance.op_lst)

def len_utterance_filler_lst():
    return len(utterance.filler_lst)

if __name__ == '__main__':
#    #args[1] = sentence
#    args = sys.argv
#    if 1 <= len(args):
#        speak(args[1])
#    else:
#        print('Arguments are too short')
    read_sentence()

