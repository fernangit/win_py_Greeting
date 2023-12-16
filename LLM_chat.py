import threading
import ELYZA_res
#import LINE_res
#import rinna_res
#import rinna_gptq_res
import talk
import time
from datetime import datetime, timedelta
### for speach recognition
import speech_recognition as sr
### for julius
import socket
import re
import vosk_streaming

SPEECH_RECOGNITION_GOOGLE = 0
SPEECH_RECOGNITION_JULIUS = 1
SPEECH_RECOGNITION_VOSK = 2

class chat():
    def __init__(self, mode):
        self.mode = mode
        self.started = threading.Event()
        self.alive = True
        self.chat_time = time.time()

        if self.mode == SPEECH_RECOGNITION_GOOGLE:
            ### for speach recognition
            self.r = sr.Recognizer()
            self.mic = sr.Microphone(device_index = 0)

        elif self.mode == SPEECH_RECOGNITION_JULIUS:
            ### for julius
            # ローカル環境のIPアドレス
            self.host = '127.0.0.1'
            # Juliusとの通信用ポート番号
            self.port = 10500
            # 正規表現で認識された言葉を抽出
            self.extracted_word = re.compile('WORD="([^"]+)"')
            # Juliusにソケット通信で接続
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            time.sleep(2)

        elif self.mode == SPEECH_RECOGNITION_VOSK:
            ### for vosk
            self.vosk_asr =vosk_streaming.init()

        self.user_message = ''
        self.response = ''
        self.before = ''
        self.data = ''

        self.thread = threading.Thread(target=self.chat_sentence_thread)
        self.thread.start()

    def __del__(self):
        self.kill()

    def begin(self):
        print("begin")
        self.chat_time = time.time()
        self.before = ''
        self.started.set()

    def end(self):
        self.started.clear()
        print("\nend")

    def kill(self):
        self.started.set()
        self.alive = False
        self.thread.join()
        if self.mode == SPEECH_RECOGNITION_JULIUS:
            ### for julius
            print('PROCESS END')
            self.client.send("DIE".encode('shift_jis'))
            self.client.close()

    def get_chat_time(self):
        return self.chat_time

    def llm_chat(self):
        self.response = '声が聞き取れませんでしたー'
        if self.mode == SPEECH_RECOGNITION_GOOGLE:
            ### for speach recognition
            with self.mic as source:
                self.r.adjust_for_ambient_noise(source)  #雑音対策
                audio = self.r.listen(source)

        try:
            self.data = ""
            t1 = time.time()
            if self.mode == SPEECH_RECOGNITION_GOOGLE:
                ### for speach recognition
                self.user_message = self.r.recognize_google(audio, language='ja-JP')

            if self.mode == SPEECH_RECOGNITION_JULIUS:
                ### for julius
                while (self.data.find("</RECOGOUT>\n.") == -1):
                    self.data += str(self.client.recv(1024).decode('shift_jis'))
                # 単語を抽出
                self.user_message = ""
                for word in filter(bool, self.extracted_word.findall(self.data)):
                    self.user_message += word

            if self.mode == SPEECH_RECOGNITION_VOSK:
                self.user_message = vosk_streaming.get_message(self.vosk_asr)

            t2 = time.time()
            print(self.user_message)
            self.response = ELYZA_res.elyza_response(self.user_message)
    #        self.response = LINE_res.line_response(user_message)
    #        self.response = rinna_res.rinnna_response(user_message)
    #        self.response = rinna_gptq_res.rinna_gptq_response(user_message, self.before)
            t3 = time.time()
            self.before = self.response
            print('talk recognize:', t2 - t1)
            print('response create:', t3 - t2)
        except:
            self.response = 'すみません、もういちどおねがいしますー'

        return self.response

    def chat_sentence_thread(self):
        self.started.wait()
        while self.alive:
            talk.read_text(self.llm_chat())
            self.started.wait()
            self.chat_time = time.time()

    def get_user_message(self):
        return self.user_message

    def get_response(self):
        return self.response

if __name__ == '__main__':
    test = chat(SPEECH_RECOGNITION_VOSK)
    test.begin()
    while True:
        time.sleep(1)
        if(time.time() - test.get_chat_time()) > 60:
            test.end()
            break

    test.kill()
