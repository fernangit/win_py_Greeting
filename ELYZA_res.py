import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = "あなたは20歳の受付の女性です。名前はまうです。"

model_name = "elyza/ELYZA-japanese-Llama-2-7b-fast-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#CPUだとメモリオーバーなので
#device = "cpu"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto").to(device)

def elyza_response(text):
    prompt = "{bos_token}{b_inst} {system}{prompt} {e_inst} ".format(
        bos_token=tokenizer.bos_token,
        b_inst=B_INST,
        system=f"{B_SYS}{DEFAULT_SYSTEM_PROMPT}{E_SYS}",
        prompt=text,
        e_inst=E_INST,
    )

    with torch.no_grad():
        token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")

        output_ids = model.generate(
            token_ids.to(model.device),
            max_new_tokens=256,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    output = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1) :], skip_special_tokens=True)
    print(output)

if __name__ == '__main__':
    while(True):
        text = input('?(qで終了):')
        if text == 'q' or 'Q':
            print('finished')
            break

        elyza_response(text)