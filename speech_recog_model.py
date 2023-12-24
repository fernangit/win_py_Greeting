from abc import ABCMeta, abstractclassmethod
import importlib

###音声認識モデルの継承クラス

class speech(metaclass=ABCMeta):
    @abstractclassmethod
    def import_lib(self):
        pass
    @abstractclassmethod
    def init(self):
        pass
    @abstractclassmethod
    def kill(self):
        pass
    @abstractclassmethod
    def get_message(self, asr):
        pass

class GOOGLE_model(speech):
    def import_lib(self):
        self.model = importlib.import_module('google_streaming')
    def init(self):
        self.model.init()
        return True
    def kill(self):
        self.model.kill()
    def get_message(self, asr):
        return self.model.get_message()

class JULIUS_model(speech):
    def import_lib(self):
        self.model = importlib.import_module('julius_streaming')
    def init(self):
        self.model.init()
        return True
    def kill(self):
        self.model.kill()
    def get_message(self, asr):
        return self.model.get_message()
    
class VOSK_model(speech):
    def import_lib(self):
        self.model = importlib.import_module('vosk_streaming')
    def init(self):
        vosk_asr = self.model.init()
        return vosk_asr
    def kill(self):
        self.model.kill()
    def get_message(self, asr):
        return self.model.get_message(asr)    

if __name__ == '__main__':
    # speech_model = GOOGLE_model()
    # speech_model.import_lib()
    # ret = speech_model.init()
    # print(speech_model.get_message(ret))

    # speech_model = JULIUS_model()
    # speech_model.import_lib()
    # ret = speech_model.init()
    # print(speech_model.get_message(ret))

    speech_model = VOSK_model()
    speech_model.import_lib()
    ret = speech_model.init()
    print(speech_model.get_message(ret))
