import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from auto_gptq import AutoGPTQForCausalLM
#pip install https://github.com/PanQiWei/AutoGPTQ/releases/download/v0.4.2/auto_gptq-0.4.2+cu118-cp310-cp310-win_amd64.whl

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = "あなたは20歳の受付の女性です。名前はまうです。優しく、わかりやすく、丁寧に解答してください。"

model_name = "rinna/youri-7b-chat-gptq"
tokenizer = AutoTokenizer.from_pretrained(model_name)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = AutoGPTQForCausalLM.from_quantized(model_name, use_safetensors=True)

def rinna_response(text, before):
    context = [
        {"speaker": "設定", "text": DEFAULT_SYSTEM_PROMPT},
        {"speaker": "ユーザー", "text": text},
        {"speaker": "システム", "text": before}
    ]
    prompt = "\n".join([f"{uttr['speaker']}: {uttr['text']}" for uttr in context])
    prompt += "\nシステム: "
    token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    with torch.no_grad():
        output_ids = model.generate(
            input_ids=token_ids.to(model.device),
            max_new_tokens=200,
            do_sample=True,
            temperature=0.5,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    output = tokenizer.decode(output_ids.tolist()[0])
    output = output[len(prompt):-len("</s>")].strip()   
    print(output)

    return output

if __name__ == '__main__':
    before = ''
    while(True):
        text = input('?(qで終了):')
        if text == 'q' or text == 'Q':
            print('finished')
            break

        rinna_response(text, before)