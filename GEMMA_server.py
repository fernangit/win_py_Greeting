import torch
from transformers import AutoProcessor, Gemma3ForConditionalGeneration
#pip install git+https://github.com/huggingface/transformers@v4.49.0-Gemma-3
from flask import Flask, request
import os
from os.path import splitext

DEFAULT_SYSTEM_PROMPT = 'あなたの名前はまうです。あなたの年齢は20歳です。 受付をしている女性です。 特に指示が無い場合は、「まう」というキャラクターとして常に日本語で親しい間柄のフレンドリーな感じで回答してください。\n'
BASE_INFORMATION = '以下の基本情報も参照して回答してください。\n基本情報：'

class GEMMA_srv:
    def __init__(self):
        #https://huggingface.co/docs/transformers/main/en/model_doc/gemma3
        self.model_name = "google/gemma-3-4b-it"
#        self.model_name = "google/gemma-3-12b-it"
        self.model = Gemma3ForConditionalGeneration.from_pretrained(self.model_name, device_map="auto", use_auth_token=True)
        self.processor = AutoProcessor.from_pretrained(self.model_name, padding_side="left")

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
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": def_prompt}
                ]
            },
            {
                "role": "user", "content": [
#                    {"type": "image", "url": url},
                    {"type": "text", "text": text},
                ]
            },
        ]

        inputs = self.processor.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=True,
            return_dict=True, return_tensors="pt"
        ).to(self.model.device, dtype=torch.bfloat16)

        input_len = inputs["input_ids"].shape[-1]

        with torch.inference_mode():
            generation = self.model.generate(**inputs, max_new_tokens=100, do_sample=False)
            generation = generation[0][input_len:]

        decoded = self.processor.decode(generation, skip_special_tokens=True)
        print(decoded)
        #補正
        decoded.replace('\n\n', '\n')
        return decoded

    def response (self, prompt, text):
        system_prompt = DEFAULT_SYSTEM_PROMPT + '\n' + prompt
        system_prompt += (BASE_INFORMATION + self.base_info + '\n')
        output = self.base_response (system_prompt, text) 
        print(output)
        return output

llm_model = GEMMA_srv()
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
