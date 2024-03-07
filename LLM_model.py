from abc import ABCMeta, abstractclassmethod
import importlib

###大規模自然言語モデルの継承クラス

class llm(metaclass=ABCMeta):
    @abstractclassmethod
    def import_lib(self):
        pass

    @abstractclassmethod
    def response(self, text, before):
        pass

class ELYZA_model(llm):
    def import_lib(self):
        self.model = importlib.import_module('ELYZA_res')

    def response(self, text, before=""):
        return self.model.response(text, before)

class RINNA_youri_model(llm):
    def import_lib(self):
        self.model = importlib.import_module('rinna_youri_res')

    def response(self, text, before=""):
        return self.model.response(text)

class RINNA_nekomata_model(llm):
    def import_lib(self):
        self.model = importlib.import_module('rinna_nekomata_res')

    def response(self, text, before=""):
        return self.model.response(text)

class RINNA_GPTQ_model(llm):
    def import_lib(self):
        self.model = importlib.import_module('rinna_gptq_res')

    def response(self, text, before):
        return self.model.response(text, before)

class LINE_model(llm):
    def import_lib(self):
        self.model = importlib.import_module('LINE_res')

    def response(self, text, before=""):
        return self.model.response(text)

class SWALLOW_model(llm):
    def import_lib(self):
        self.model = importlib.import_module('Swallow_res')

    def response(self, text, before=""):
        return self.model.response(text)
    
if __name__ == '__main__':
    llm_model = ELYZA_model()
    llm_model.import_lib()
    print(llm_model.response('こんにちは', 'ありがとう'))

    # llm_model = RINNA_model()
    # llm_model.import_lib()
    # print(llm_model.response('こんにちは'))    

    # llm_model = RINNA_GPTQ_model()
    # llm_model.import_lib()
    # print(llm_model.response('こんにちは', 'ありがとう'))

    # llm_model = LINE_model()
    # llm_model.import_lib()
    # print(llm_model.response('こんにちは'))

    # llm_model = SWALLOW_model()
    # llm_model.import_lib()
    # print(llm_model.response('こんにちは'))
