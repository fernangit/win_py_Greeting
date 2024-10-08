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
SPEECH_RECOGNITION_FWHISPER = 3

#llm mode
LLM_ELYZA = 0
LLM_youri_RINNA = 1
LLM_nekomata_RINNA = 2
LLM_RINNA_GPTQ = 3
LLM_LINE = 4
LLM_SWALLOW = 5

class chat():          
    def __init__(self, speech_mode, llm_mode):
        self.started = threading.Event()
        self.alive = True
        self.chat_time = time.time()
        #speech model
        self.select_speech_model(speech_mode)
        self.speech_model.import_lib()
        self.speech_ret = self.speech_model.init()

        #LLM model
        self.select_llm_model(llm_mode)
        self.llm_model.import_lib()

        self.user_message = ''
        self.response = ''
        self.mesbefore = ''
        self.resbefore = ''
        self.data = ''

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

    def select_llm_model(self, llm_mode):
        #LLM model
        if llm_mode == LLM_ELYZA:
            ### for ELYZA
            self.llm_model = LLM_model.ELYZA_model()
        elif llm_mode == LLM_youri_RINNA:
            ### for youri RINNA
            self.llm_model = LLM_model.RINNA_youri_model()
        elif llm_mode == LLM_nekomata_RINNA:
            ### for nekomata RINNA
            self.llm_model = LLM_model.RINNA_nekomata_model()
        elif llm_mode == LLM_RINNA_GPTQ:
            ### for RINNA GPTQ
            self.llm_model = LLM_model.RINNA_GPTQ_model()
        elif llm_mode == LLM_RINNA_GPTQ:
            ### for LINE
            self.llm_model = LLM_model.LINE_model()
        elif llm_mode == LLM_SWALLOW:
            ### for LINE
            self.llm_model = LLM_model.SWALLOW_model()

    def __del__(self):
        self.kill()

    def begin(self):
        print('llm begin')
        self.mesbefore = ''
        self.resbefore = ''
        self.started.set()
        self.chat_time = time.time()

    def end(self):
        self.started.clear()
        self.filler_alive = False
        print('llm end')

    def kill(self):
        self.started.set()
        self.alive = False
        self.thread.join()
        self.speech_model.kill()

    def get_chat_time(self):
        return self.chat_time

    def llm_chat(self):
        self.response = self.resbefore
        try:
            self.data = ''
            self.user_message = self.speech_model.get_message(self.speech_ret)
            print('llm_user_message=', self.user_message)
            self.filler = threading.Thread(target=self.chat_filler_thread)
            self.filler.start()
            self.filler_alive = True
            self.response = self.llm_model.response(self.user_message, self.resbefore)
            self.filler_alive = False
            if len(self.resbefore) >= 10 and self.resbefore in self.response:
                # レスポンスに前回と同一文章（10文字以上）を含む場合はリセット
                raise Exception
            # 3センテンスのみ前回文章として読み込ませる
            self.resbefore = '。'.join(self.response.split('。')[:3])
            print('resbefore:', self.resbefore)
        except:
            self.response = 'すみません、もういちどおねがいしますー'
            self.resbefore = ''

        return self.response

    def chat_sentence_thread(self):
        self.started.wait()
        while self.alive:
            talk.read_text(self.llm_chat())
            self.started.wait()
            self.chat_time = time.time()

    def chat_filler_thread(self):
        time.sleep(6)
        while(self.filler_alive):
            talk.filler()
            self.chat_time = time.time()
            time.sleep(3)

    def get_user_message(self):
        return self.user_message

    def get_response(self):
        return self.response

if __name__ == '__main__':
    test = chat(SPEECH_RECOGNITION_VOSK, LLM_ELYZA)
    test.begin()
    while True:
        time.sleep(1)
        if(time.time() - test.get_chat_time()) > 30:
            test.end()
            break
        # text = input('?(qで終了):')
        # if text == 'q' or text == 'Q':
        #     print('finished')
        #     break
        
    test.kill()
