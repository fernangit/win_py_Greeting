import threading
import talk
import time
from datetime import datetime, timedelta
import speech_recog_model
import text_classification

#speech mode
SPEECH_RECOGNITION_GOOGLE = 0
SPEECH_RECOGNITION_JULIUS = 1
SPEECH_RECOGNITION_VOSK = 2
SPEECH_RECOGNITION_FWHISPER = 3

class clsChat():          
    def __init__(self, speech_mode):
        self.started = threading.Event()
        self.alive = True
        self.chat_time = time.time()
        #speech model
        self.select_speech_model(speech_mode)
        self.speech_model.import_lib()
        self.speech_ret = self.speech_model.init()

        self.user_intent = ''
        self.val = 0.0
        self.user_message = ''

        self.thread = threading.Thread(target=self.chat_sentence_thread)
        self.thread.start()

    def select_speech_model(self, speech_mode):
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
        elif speech_mode == SPEECH_RECOGNITION_FWHISPER:
            ### for faster whisper
            self.speech_model = speech_recog_model.FWHISPER_model()

    def __del__(self):
        self.kill()

    def begin(self):
        print("cls begin")
        self.chat_time = time.time()
        self.started.set()

    def end(self):
        self.started.clear()
        print("cls end")

    def kill(self):
        self.started.set()
        self.alive = False
        self.thread.join()
        self.speech_model.kill()

    def get_chat_time(self):
        return self.chat_time

    def cls_chat(self):
        try:
            self.user_message = self.speech_model.get_message(self.speech_ret)
            print('user_message=', self.user_message)
            label, val = text_classification.get_label(self.user_message)
            print(label, val)
        except:
            label = ''
            val = 0.0

        return label, val

    def chat_sentence_thread(self):
        self.started.wait()
        while self.alive:
            self.user_intent, self.val = self.cls_chat()
            self.started.wait()
            self.chat_time = time.time()

    def get_user_intent(self):
        return self.user_intent, self.val, self.user_message

    def reset_user_intent(self):
        self.user_intent = ''
        self.val = 0
        self.user_message = ''

if __name__ == '__main__':
    test = clsChat(SPEECH_RECOGNITION_VOSK)
    test.begin()
    while True:
        time.sleep(1)
        if(time.time() - test.get_chat_time()) > 60:
            test.end()
            break

    test.kill()
