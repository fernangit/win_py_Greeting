#https://giita.com/tinymouse/items/a34960e8942ba2827c58
from PIL import Image
import transformers
import torch
import os

prompt = 'これは何の画像ですか。'

#モデルとプロセッサの準備
model = transformers.LlavaForConditionalGeneration.from_pretrained (
    'llava-hf/llava-1.5-7b-hf',
    device_map = 'auto',
    torch_dtype = torch.float16, 
    low_cpu_mem_usage = True,
)

processor = transformers.AutoProcessor.from_pretrained(
    'llava-hf/llava-1.5-7b-hf',
)

# #パイプラインの準備
# pipe = transformers.pipeline(
#     'image-to-text',
#     model = 'llava-hf/lava-1.5-7b-hf',
#     device = 0
# )

def analyze_image(img_path):
    image = Image.open(img_path)

    #プロセッサとモデルで推論
    inputs = processor(
        'USER: <image>\n' + prompt + '\nASSISTANT: \n',
        image,
        return_tensors = 'pt'
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens = 200,
        do_sample = False
    )

    comment = processor.decode(outputs[0] [1:], skip_special_tokens = True)
    comment = comment.replace('USER: \n' + prompt + '\nASSISTANT: \n', '')

    # #パイプラインで推論
    # outputs = pipe (
    #     image,
    #     prompt = 'USER: <image>\n' prompt + 'ASSISTANT: \n',
    #     generate_kwargs=['max_new_tokens': 200]
    # )
    # comment = outputs [0]['generated_text']
    # comment = comment.replace('USER: \n' + prompt + '\nASSISTANT: \n')
    # print (comment)

    return comment

if __name__ == '__main__':
    img_path = 'image/img1.jpg'
    comment = analyze_image(img_path)
    print (comment) 