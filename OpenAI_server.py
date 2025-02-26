import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from flask import Flask, request
import os
from os.path import splitext
import re
from openai import AzureOpenAI

DEFAULT_SYSTEM_PROMPT = 'あなたの名前はまうです。あなたの年齢は20歳です。 受付をしている女性です。 特に指示が無い場合は、「まう」というキャラクターとして常に日本語で親しい間柄のフレンドリーな感じで回答してください。\n'
BASE_INFORMATION = '以下の基本情報も参照して回答してください。\n基本情報：'

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type = 'nf4',
    bnb_4bit_compute_dtype= torch.bfloat16,    
)

class OPENAI_srv:
    def __init__(self):
        # self.model_name = 'gpt-4o'
        # self.model_name = 'gpt-4o-turbo'
        # self.model_name = 'gpt-35-turbo'
        self.model_name = 'gpt-4o-mini'
        # self.model_name = 'text-embedding-3-large'

        self.client = AzureOpenAI(
            azure_endpoint='https://openai.azure-api.net',
            api_key = '',
            api_version = '2021-09-01',
        )

        #基本情報読み込み
        self.base_info = ''
        dir = 'basedata'
        for file in os.listdir(dir):
            root, ext = splitext(file)
            if ext == '.txt':
                with open(dir+'/'+file, 'r', encoding='utf-8') as f:
                    self.base_info += (f.read() + '\n')

    def base_response(self, def_prompt, text):
        messages = [
            {'role' : 'system', 'content' : def_prompt},
            {'role' : 'user', 'content' : text},
        ]

        response = self.client.chat.completions.create(
            model = self.model_name,
            messages = messages
        )
        print(response.choices[0].message.content)

        output = response.choices[0].message.content
        return output

    def response (self, prompt, text):
        system_prompt = DEFAULT_SYSTEM_PROMPT + '\n' + prompt
        system_prompt += (BASE_INFORMATION + self.base_info + '\n"""')
        output = self.base_response (system_prompt, text) 
        # 2行改行を1行に変換
        output = re.sub(r'\n\n', '\n', output)
        print(output)
        return output

llm_model = OPENAI_srv()
app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/Utterance', methods=['POST'])
def updateUtter():
    print('post')

    prompt = request.form['prompt']
    print(prompt)
    text = request.form['text']
    print(text)

    #response
    res = llm_model.response(prompt, text)

    filename = 'Utterance/utter.txt'
    with open(filename, mode='w', encoding='utf-8') as fout:
        fout.write(res)
        print('writed!')

    return res

def startServer(url, pnum):
    app.run(host=url, port=pnum, debug=True, use_reloader=False)

import sys
if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print("Usage: python ELYZA_server.py <url> <port>")
    #     sys.exit(1)

    # url = sys.argv[1]
    # port = sys.argv[2]

    # startServer(url, port)
    startServer('127.0.0.1', '8000')
