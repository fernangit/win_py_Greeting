import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
#https://github.com/kohya-ss/sd-scripts/blob/main/README-ja.md
#python -m pip install bitsandbytes==0.41.1 --prefer-binary --extra-index-url=https://jllllll.github.io/bitsandbytes-windows-webui

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = "あなたは20歳の受付の女性です。名前はまうです。"

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model_name = "elyza/ELYZA-japanese-Llama-2-7b-fast-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#CPUだとメモリオーバーなので
#device = "cpu"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", quantization_config=quantization_config)
#model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto").to(device)

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
#    output = output.replace('\n', '')
#    print(output)
#    return output
    outs = output.split('\n')
    print(outs[0])
    return outs[0]

if __name__ == '__main__':
    while(True):
        text = input('?(qで終了):')
        if text == 'q' or text == 'Q':
            print('finished')
            break

        elyza_response(text)