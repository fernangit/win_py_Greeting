#https://pypi.org/project/rvc-python/
from rvc_python.infer import RVCInference
import os

#変換モデルの配置
#rvc_models/モデルフォルダ/モデル.pth
#変換モデルの呼び出し
#rvc.load_model(モデルフォルダ)
#モデルフォルダ内の最初のpthが採用される

path = os.getcwd()
print(path)
rvc = RVCInference(device="cuda:0")
#rvc = RVCInference(models_dir=path, device="cuda:0")
rvc.load_model("甘_アマエ")

def convert(input='input.wav', output='output.wav'):
    rvc.infer_file(input, output)

if __name__ == '__main__':
    convert("input.wav", "convert.wav")