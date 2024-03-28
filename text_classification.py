import torch
from transformers import BertJapaneseTokenizer, AutoModelForSequenceClassification

# ラベル
labels = ['Dailylife', 'Schoollife', 'Travel', 'Health', 'Entertainment', 'ReserveMeetingroom', 'Call', 'Praise', 'Encouragement', 'SetPlan', 'MAU', 'Greeting', 'CallOut']

# モデルとトークナイザーの準備
model = AutoModelForSequenceClassification.from_pretrained('text-classification_ja/')    
tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking') 

# テンソルに変換
def change_tensor(text):
    tokenized_text = tokenizer.tokenize(text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])
    return tokens_tensor

# 推論の実行
def predict(tokens_tensor):
    model.eval()
    with torch.no_grad():
        outputs = model(tokens_tensor)[0]
#        print(labels[torch.argmax(outputs)])
        return outputs
    
# ラベル取得
def get_label(text):
    #分類
    output = predict(change_tensor(text))
    print(output)
    # 降順並べ替え
    sorted, idx = torch.sort(output, descending = True)
    print(sorted)
    return labels[idx[0, 0].item()], sorted[0, 0].item()

if __name__ == '__main__':
    before = ''
    while(True):
        text = input('?(qで終了)：')
        if text == 'q' or text == 'Q':
            print('finished')
            break
        
        label, val = get_label(text)
        print(label, val)
