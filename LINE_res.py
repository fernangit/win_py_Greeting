import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = "あなたは20歳の受付の女性です。名前はまうです。"

model_name = "line-corporation/japanese-large-lm-3.6b"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#CPUだとメモリオーバーなので
#device = "cpu"
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

def line_response(text):
    prompt = DEFAULT_SYSTEM_PROMPT + text
    output = generator(
        prompt,
        max_length=30,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
        num_return_sequences=5,
    )
    
    print(output)

if __name__ == '__main__':
    while(True):
        text = input('?(qで終了):')
        if text == 'q' or text == 'Q':
            print('finished')
            break

        line_response(text)