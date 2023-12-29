import threading
import talk
import time
from datetime import datetime, timedelta
import LLM_model
import speech_recog_model

#speech mode
SPEECH_RECOGNITION_GOOGLE = 0
SPEECH_RECOGNITION_JULIUS = 1
SPEECH_RECOGNITION_VOSK = 2

#llm mode
LLM_ELYZA = 0
LLM_RINNA = 1
LLM_RINNA_GPTQ = 2
LLM_LINE = 3
LLM_SWALLOW = 4

class chat():
    def __init__(self, speech_mode, llm_mode):
        self.started = threading.Event()
        self.alive = True
        self.chat_time = time.time()
        #speech model
        if speech_mode == SPEECH_RECOGNITION_GOOGLE:
            ### for speach recognition
            self.speech_model = speech_recog_model.GOOGLE_model()
        elif speech_mode == SPEECH_RECOGNITION_JULIUS:
            ### for julius
            self.speech_model = speech_recog_model.JULIUS_model()
        elif speech_mode == SPEECH_RECOGNITION_VOSK:
            ### for vosk
            self.speech_model = speech_recog_model.VOSK_model()

        self.speech_model.import_lib()
        self.speech_ret = self.speech_model.init()

        #LLM model
        if llm_mode == LLM_ELYZA:
            ### for ELYZA
            self.llm_model = LLM_model.ELYZA_model()
        elif llm_mode == LLM_RINNA:
            ### for RINNA
            self.llm_model = LLM_model.RINNA_model()
        elif llm_mode == LLM_RINNA_GPTQ:
            ### for RINNA GPTQ
            self.llm_model = LLM_model.RINNA_GPTQ_model()
        elif llm_mode == LLM_RINNA_GPTQ:
            ### for LINE
            self.llm_model = LLM_model.LINE_model()
        elif llm_mode == LLM_SWALLOW:
            ### for LINE
            self.llm_model = LLM_model.SWALLOW_model()

        self.llm_model.import_lib()

        self.user_message = ''
        self.response = ''
        self.mesbefore = ''
        self.resbefore = ''
        self.data = ''

        self.thread = threading.Thread(target=self.chat_sentence_thread)
        self.thread.start()

    def __del__(self):
        self.kill()

    def begin(self):
        print("begin")
        self.chat_time = time.time()
        self.mesbefore = ''
        self.resbefore = ''
        self.started.set()

    def end(self):
        self.started.clear()
        print("\nend")

    def kill(self):
        self.started.set()
        self.alive = False
        self.thread.join()
        self.speach_model.kill()

    def get_chat_time(self):
        return self.chat_time

    def llm_chat(self):
        self.response = self.resbefore
        try:
            self.data = ""
            t1 = time.time()
            self.user_message = self.mesbefore + "\n" + self.speech_model.get_message(self.speech_ret)
            t2 = time.time()
            print(self.user_message)
            self.response = self.llm_model.response(self.user_message)
            t3 = time.time()
            self.resbefore = self.response
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
    test = chat(SPEECH_RECOGNITION_VOSK, LLM_ELYZA)
    test.begin()
    while True:
        time.sleep(1)
        if(time.time() - test.get_chat_time()) > 60:
            test.end()
            break

    test.kill()
