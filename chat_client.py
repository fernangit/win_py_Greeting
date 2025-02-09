import rag
import mem
import datetime
import atexit
import requests
import configparser

#曜日の名前をリストで定義
WEEKDAYS = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']

#DEFAULT_SYSTEM_PROMPT = 'あなたの名前はまうです。あなたの年齢は20歳です。 受付をしている女性です。 特に指示が無い場合は、「まう」というキャラクターとして常に日本語で親しい間柄の感じで回答してください。\n'
DEFAULT_SYSTEM_PROMPT2 = '以下のコンテキストも参照して回答してください。\nコンテキスト：'
DEFAULT_SYSTEM_PROMPT3 = '以下の会話履歴も参考に回答してください。 \n会話：'

class chat_clt:
    def __init__(self):
        # self.ELYZA_srv = ELYZA_server.ELYZA_srv()        
        self.memory = mem.initialize(100)
        self.memory.human_prefix = 'あなた'
        self.memory.ai_prefix = 'まう'

        # パスを設定ファイルから取得
        config = configparser.ConfigParser()
        config.read('settings.ini')

        # 設定値の取得
        dbpath = config['Directory']['DBPath']
        commondir = config['Directory']['Common']
        privatedir = config['Directory']['Private']

        # retriever = rag.initialize(dbpath, commondir, privatedir)
        retriever, vectorstore = rag.initialize_ParentDocumentRetriever(dbpath, commondir, privatedir)

        #終了時メモリ書き込みを登録
        atexit.register(self.memorize)
    
    def llm_response(self, def_prompt, text):
        output = self.base_response(def_prompt, text)
        print (output)
        return output

    def response_with_rag (self, memory, retriever, text, url=''):
        today = datetime.datetime.today()
        #曜日を取得
        weekday = WEEKDAYS[today.weekday()]

        dt_now = datetime.datetime.now()
        tstr = dt_now.strftime('%Y年%m月%d日%H時%M分'.encode('unicode-escape').decode()).encode().decode('unicode-escape')

        def_prompt = '現在時刻は' + tstr + weekday + ' です。'
#        def_prompt += DEFAULT_SYSTEM_PROMPT

        #検索したコンテキストをプロンプトに設定する
        context = rag.create_context(retriever, text)
        if context != '':
            def_prompt += (DEFAULT_SYSTEM_PROMPT2 + context + '\n')

        #会話履歴をプロンプトに設定する
        buffer = mem.load(memory)
        def_prompt += (DEFAULT_SYSTEM_PROMPT3 + buffer['history'])

        #回答を得る
#        output = self.ELYZA_srv.base_response(def_prompt, text)
        output = self.send_receive(url, def_prompt, text)
        print (output)

        #メモリに書き込む
        memory = mem.memorize(memory, text, output)

        return output

    def response (self, url, text, before = ''):
        r = self.response_with_rag (self.memory, self.retriever, text, url) 
        return r

    def memorize (self):
        #メモリに書き込む
        mem.save(self.memory, './mem/memory.txt')

    def send_receive(self, url, prompt, text):
        self.send_message(url, prompt, text)
        response = self.receive_response(url+'/utter.txt')
        return response
    
    def send_message(self, url, prompt, text):
        print(url)
        print(text)
        payload = {'prompt':prompt, 'text':text}
        response = requests.post(url, data = payload)
        print(response)

    def receive_response(self, url):
        print(url)
        # utterance = requests.get(url).content.decode('cp932')
        response = requests.get(url).content.decode('utf_8')
        return response

import sys

if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print("Usage: python ELYZA_client.py <url> <port>")
    #     sys.exit(1)

    # url = sys.argv[1]
    # port = sys.argv[2]

    llm_model = ELYZA_clt()
    while(True):
        text = input('?(qで終了):')
        if text == 'q' or text == 'Q':
            print('finished')
            break
#        r = llm_model.response('http://'+url+':'+port+'/Utterance', text)
        r = llm_model.response('http://127.0.0.1:8000/Utterance', text)

