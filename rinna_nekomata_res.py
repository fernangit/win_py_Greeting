import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_name = "rinna/nekomata-7b-instruction"
#model_name = "rinna/japanese-gpt2-xsmall"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
#tokenizer.do_lower_case = True ### for rinna/japanese-gpt2-xsmall
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#CPUだとメモリオーバーなので
#device = "cpu"
model = AutoModelForCausalLM.from__pretrained(model_name, device_map="auto", trust_remote_code=True)

instruction = "あなたは20歳の受付の女性です。名前はまうです。優しく、わかりやすく、丁寧に解答してください。"

def response(text):
    ### for rinna/youri-7b-chat"
    context = [
        {"speaker": "設定", "text": instruction},
        {"speaker": "ユーザー", "text": text}
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
    ### for rinna/youri-7b-chat"

    # ### for rinna/japanese-gpt2-xsmall
    # text = instruction + text
    # input = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt")
    # output = model.generate(
    #     input,
    #     max_length=50,
    #     min_length=10,
    #     do_sample=True,
    #     top_k=40,
    #     temperature=1.5,
    #     pad_token_id=tokenizer.pad_token_id,
    #     bos_token_id=tokenizer.bos_token_id,
    #     eos_token_id=tokenizer.eos_token_id
    # )
    # output = tokenizer.batch_decode(output)
    # output = output[0].replace(text, '')
    # ### for rinna/japanese-gpt2-xsmall

    print(output)
    return output

if __name__ == '__main__':
    while(True):
        text = input('?(qで終了):')
        if text == 'q' or text == 'Q':
            print('finished')
            break

        response(text)