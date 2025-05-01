import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from flask import Flask, request
import os
from os.path import splitext
import re

DEFAULT_SYSTEM_PROMPT = 'あなたの名前はまうです。あなたの年齢は20歳です。 受付をしている女性です。 特に指示が無い場合は、「まう」というキャラクターとして常に日本語で親しい間柄のフレンドリーな感じで回答してください。\n'
BASE_INFORMATION = '以下の基本情報も参照して回答してください。\n基本情報：'

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type = 'nf4',
    bnb_4bit_compute_dtype= torch.bfloat16,    
)

class QWEN3_srv:
    def __init__(self):
        #https://huggingface.co/collections/Qwen/qwen3-67dd247413f0e2e4f653967f
        self.model_name = "Qwen/Qwen3-4B"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype = 'auto',
            device_map = 'auto',
            quantization_config=quantization_config
        )
        self.model.eval()
        self.model = torch.compile(self.model) #高速化対応

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

        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize = False,
            add_generation_prompt = True,
            enable_thinking=True # Switch between thinking and non-thinking modes. Default is True.
        )

        token_ids = self.tokenizer.encode(
            prompt,
            add_special_tokens = False,
            return_tensors = 'pt'
        )

        with torch.no_grad():
            output_ids = self.model.generate(
                token_ids.to(self.model.device),
                max_new_tokens=1200, 
                temperature=0.6,
                top_p=0.9,
                top_k=50,
                repetition_penalty=1.10,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        output = self.tokenizer.decode(
            output_ids.tolist()[0] [token_ids.size(1):], skip_special_tokens=True
        )

        #補正
        # <think></think>で囲まれた部分を削除
        output = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL)
        # () で囲まれた部分を削除
        output = re.sub(r'（.*?）', '', output)
        # "**" を削除
        output = re.sub(r'\*\*', '', output)
        # 連続する改行 (\n\n) を単一の改行 (\n) に変換
        output = re.sub(r'\n+', '\n', output)
        # 「AI拶ユニット」を「まう」に置換
        output = re.sub(re.escape('「AI拶ユニット」'), 'まう', output)
        output.strip()  # 不要な前後の空白を削除
        return output

    def response (self, prompt, text):
        system_prompt = DEFAULT_SYSTEM_PROMPT + '\n' + prompt
        system_prompt += (BASE_INFORMATION + self.base_info + '\n')
        output = self.base_response (system_prompt, text) 
        print(output)
        return output

llm_model = QWEN3_srv()
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
