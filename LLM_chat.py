import threading
import speech_recognition as sr
#import ELYZA_res
#import LINE_res
import talk
import time
from datetime import datetime, timedelta

class chat():
    def __init__(self):
        self.started = threading.Event()
        self.alive = True
        self.chat_time = time.time()
        self.r = sr.Recognizer()
        self.mic = sr.Microphone(device_index = 0)

        self.thread = threading.Thread(target=self.chat_sentence_thread)
        self.thread.start()

    def __del__(self):
        self.kill()

    def begin(self):
        print("begin")
        self.started.set()

    def end(self):
        self.started.clear()
        print("\nend")

    def kill(self):
        self.started.set()
        self.alive = False
        self.thread.join()

    def get_chat_time(self):
        return self.chat_time

    def llm_chat(self):
        response = '声が聞き取れませんでしたー'
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)  #雑音対策
            audio = self.r.listen(source)

        try:
            user_message = self.r.recognize_google(audio, language='ja-JP')
            print(user_message)
    #        response = ELYZA_res.elyza_response(user_message)
    #        response = LINE_res.elyza_response(user_message)
        except:
            response = 'すみません、もういちどおねがいしますー'

        return response

    def chat_sentence_thread(self):
        self.started.wait()
        while self.alive:
            self.chat_time = time.time()
            talk.read_text(self.llm_chat())
            self.started.wait()
              
if __name__ == '__main__':
    test = chat()
    test.begin()
    while True:
        time.sleep(1)
        if(time.time() - test.get_chat_time()) > 60:
            test.end()
            break

    test.kill()
