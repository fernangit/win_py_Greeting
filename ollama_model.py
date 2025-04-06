# import ollama

# response = ollama.chat(model='gemma3:12b', messages=[
#   {
#     'role': 'user',
#     'content': 'なんでもいいから話して',
#   },
# ])
# print(response['message']['content'])

# ollama pull gemma3:12b
# ollama run gemma3:12b

from transformers import AutoModelForCausalLM, AutoTokenizer

# モデルとトークナイザーの指定 (Gemma 2B など)
#model_name = "google/gemma-12b"
model_name = r"C:\Users\morio\model\ollama"

# モデルとトークナイザーのロード
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# プロンプトの準備
prompt = "Pythonで簡単な挨拶文を表示するプログラムを書いてください。"

# 入力テキストをトークン化
input_ids = tokenizer.encode(prompt, return_tensors="pt")

# テキスト生成
output = model.generate(input_ids, max_length=100, num_return_sequences=1)

# 生成されたテキストをデコード
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

# 結果の表示
print(generated_text)