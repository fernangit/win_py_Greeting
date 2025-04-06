import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import os
import rag
import mem
#import img #VRAM不足
import threading
import datetime
import atexit
import configparser
import ollama

# 事前にモデルをダウンロードしておく
# ollama pull gemma3:12b
# ollama run gemma3:12b

#曜日の名前をリストで定義
WEEKDAYS = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']

DEFAULT_SYSTEM_PROMPT = '###あなたの名前はまうです。あなたの年齢は20歳です。 受付をしている女性です。 特に指示が無い場合は、「まう」というキャラクターとして常に日本語で親しい間柄のフレンドリーな感じで回答してください。\n'
DEFAULT_SYSTEM_PROMPT2 = '###以下のコンテキストも参照して回答してください。\nコンテキスト："""'
DEFAULT_SYSTEM_PROMPT3 = '###以下の会話履歴も参考に回答してください。 \n会話："""'
DEFAULT_SYSTEM_PROMPT4 = '###目の前に見えている景色も参考に回答してください。\n見えている景色："""'

class OLLAMA_model:
    def __init__(self):
        #https://huggingface.co/elyza/Llama-3-ELYZA-JP-8B
        self.model_name = 'gemma3:12b'

        #image thread  #VRAM不足
        self.img_comment = ''
        self.img_loop = True

        self.memory = mem.initialize(100)
        self.memory.human_prefix = 'あなた'
        self.memory.ai_prefix = 'まう'

        # パスを設定ファイルから取得
        config = configparser.ConfigParser()
        config.read('settings.ini')

        # 設定値の取得
        self.dbpath = config['Directory']['DBPath']
        self.commondir = config['Directory']['Common']
        self.privatedir = config['Directory']['Private']

        # self.retriever = rag.initialize(self.dbpath, self.commondir, self.privatedir)
        self.retriever = rag.initialize_ParentDocumentRetriever(self.dbpath, self.commondir, self.privatedir)

        #終了時メモリ書き込みを登録
        atexit.register(self.memorize)

    def base_response(self, def_prompt, text):
#         messages = [
#             {
#                 "role": "system",
#                 "content": [{"type": "text", "text": def_prompt}]
#             },
#             {
#                 "role": "user",
#                 "content": [
# #                    {"type": "image", "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg"},
#                     {"type": "text", "text": text}
#                 ]
#             }
#         ]

        messages = [
            # {'role' : 'system', 'content' : def_prompt},
            {'role' : 'user', 'content' : text},
        ]

        response = ollama.chat(model=self.model_name, messages=messages)
        output = response['message']['content']

        #補正
        output.replace('\n\n', '\n')
        return output
    
    def llm_response(self, def_prompt, text):
        output = self.base_response(def_prompt, text)
        print (output)
        return output

    def response_with_rag (self, memory, retriever, text):
        today = datetime.datetime.today()
        #曜日を取得
        weekday = WEEKDAYS[today.weekday()]

        dt_now = datetime.datetime.now()
        tstr = dt_now.strftime('%Y年%m月%d日%H時%M分'.encode('unicode-escape').decode()).encode().decode('unicode-escape')

        def_prompt = '現在時刻は' + tstr + weekday + ' です。'
        def_prompt += DEFAULT_SYSTEM_PROMPT

        #Hyde クエリから仮の回答を作成して、それに似たドキュメントを検索する方法
        output = self.base_response(def_prompt, text)

        #検索したコンテキストをプロンプトに設定する
        #context = rag.create_context(db, text)
        context = rag.create_context(retriever, output)
        if context != '':
            def_prompt += (DEFAULT_SYSTEM_PROMPT2 + context + '\n"""')

        #会話履歴をプロンプトに設定する
        buffer = mem.load(memory)
        def_prompt += (DEFAULT_SYSTEM_PROMPT3 + buffer['history'] + '\n"""')

        #画像コメントを読み込む
        if self.img_comment != '':
            def_prompt += (DEFAULT_SYSTEM_PROMPT4 + self.img_comment + '\n"""')

        #回答を得る
        output = self.base_response(def_prompt, text)
        print (output)

        #メモリに書き込む
        memory = mem.memorize(memory, text, output)

        return output

    def response (self, text, before = ''):
        r = self.response_with_rag (self.memory, self.retriever, text) 
        return r

    def memorize (self):
        #メモリに書き込む
        mem.save(self.memory, self.privatedir + '/memory.txt')

if __name__ == '__main__':
    llm_model = OLLAMA_model()
    while(True):
        text = input('?(qで終了):')
        if text == 'q' or text == 'Q':
            print('finished')
            break
        r = llm_model.response(text)

    img_loop = False