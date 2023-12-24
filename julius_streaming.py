# -*- coding: utf-8 -*-
import socket
import re
import time

# ローカル環境のIPアドレス
host = '127.0.0.1'
# Juliusとの通信用ポート番号
port = 10500
# 正規表現で認識された言葉を抽出
extracted_word = re.compile('WORD="([^"]+)"')
# Juliusにソケット通信で接続
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
time.sleep(2)

def init():
    pass

def kill():
    print('PROCESS END')
    client.send("DIE".encode('shift_jis'))
    client.close()

def get_message():
    while (data.find("</RECOGOUT>\n.") == -1):
        data += str(client.recv(1024).decode('shift_jis'))
    # 単語を抽出
    user_message = ""
    for word in filter(bool, extracted_word.findall(data)):
        user_message += word

    return user_message

if __name__ == '__main__':
    print('音声認識開始')
    recog_result = get_message()
    print('音声認識結果 ', recog_result)
    print('音声認識終了')
