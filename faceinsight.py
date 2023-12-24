# -*- coding: utf-8 -*-
import sys
import torch
from PIL import Image, ImageDraw
import numpy as np
import glob
import os
import time
import insightface.app
import cv2 as cv

LEFT_EYE = 0
RIGHT_EYE = 1
NOSE = 2
MOUTH_LEFT = 3
MOUTH_RIGHT = 4

#### GPUチェック
device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
#LLM_chatを使用する時はCPUで動かす
device = 'cpu'
print('Using device:', device)

#### insightface のモデル読み込み
start = time.perf_counter()
#prepare face analysis
#face_analysis = insightface.app.FaceAnalysis(name = 'insightface/models/buffalo_l', providers = ['CUDAExcutionProvider', 'CPUExecutionProvider'])
face_analysis = insightface.app.FaceAnalysis(providers = ['CUDAExcutionProvider', 'CPUExecutionProvider'])
face_analysis.prepare(ctx_id=0, det_size=(640, 640))
print('モデル読み込み', time.perf_counter() - start)

##画像の読み込みと前処理
def read_image(file_path):
    image = Image.open(file_path).convert("RGB")
    image = np.array(image)
    image = image[:, :, [2, 1, 0]]  # RGB to BGR
    return image

### 顔切り出し
#def crop_face(img):
#    return faces, batch_boxes, batch_probs, batch_points

### 顔の特徴点を取得
# def detect_face_features(frame):
#     return left_eye, right_eye, nose, mouth_left, mouth_right

### 正面顔を取得
# def frontal_face(frame):
#     #顔の特徴点を取得
#     #顔の向きを判定
#     #目の位置関係をチェック
#     #口の位置関係をチェック
#     return is_frontal

### 顔サイズチェック
def check_face_size(img, face, th):
    w, h = img.size
    fw, fh = face.size
    
    if (fw/w < th) or (fh/w < th):
        return False
    
    return True

### ベクトルの保存
def save_feature_vector(inp, outp):
    # フォルダ内のファイルを検索
    print(inp + '/' + '*.jpg')
    jpg_files = glob.glob(inp + '/**/*.jpg', recursive=True)
    for jpg in jpg_files:
        # ファイル名取得
        basename = os.path.splitext(os.path.basename(jpg))[0]
        print(basename)
        face = read_image(jpg)
        if face is not None:
            faces = face_analysis.get(face)
            if len(faces) > 0:
                # numpy形式でベクトル保存
                fv = faces[0].embedding
                vector = outp + '/' + basename
                np.save(vector, fv.astype('float32'))

#### 画像ファイルから画像の特徴ベクトルを取得(ndarray 512次元)
def feature_vector(img_cropped):
    feature_vector_np = []
    faces = face_analysis.get(img_cropped)
    if len(faces) > 0:
        # numpy形式でベクトル保存
        feature_vector_np = faces[0].embedding

    return feature_vector_np

#### 2つのベクトル間のコサイン類似度を取得(cosine_similarity(a, b) = a・b / |a||b|)
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

#### 2枚の画像間の類似度を取得
### img = Image.open(image)
def similarity(img_cropped1, img_cropped2):
    #特徴ベクトル算出
    img1_fv = feature_vector(img_cropped1)
    img2_fv = feature_vector(img_cropped2)
    #コサイン類似度を算出
    sim = cosine_similarity(img1_fv, img2_fv)
#    print(sim)
    return sim

#### フォルダ内の画像との類似度を比較
### img = Image.open(image)
def compare_similarity(img_cropped, path):
    maxsim = 0.0
    detect = ''

    #特徴ベクトル算出
    start = time.perf_counter()
    in_fv = feature_vector(img_cropped)
#    print('特徴ベクトル算出', time.perf_counter() - start)
    if len(in_fv) == 0:
        return maxsim, detect, in_fv

    # フォルダ内のファイルを検索
    start = time.perf_counter()
    npy_files = glob.glob(path + '/' + '*.npy')
    print('glob作成', time.perf_counter() - start)
    start = time.perf_counter()
    for npy in npy_files:
        # ファイル名取得
        basename = os.path.splitext(os.path.basename(npy))[0]
#        print(basename)
        # 比較numpyデータ取得
        cp_fv = np.load(npy)
        # 類似度を計算
        sim = cosine_similarity(in_fv, cp_fv)
#        print(sim)
        if sim > maxsim:
            maxsim = sim
            detect = basename
    print('フォルダ内のファイルを検索', time.perf_counter() - start)

    #類似度が所定値以下なら認証不可
    print(detect, maxsim)
    if maxsim <= 0.7:
        detect = ''

    return maxsim, detect, in_fv

# def draw_boxes(img, boxes, probs, landmarks):
#     img_draw = img.copy()
#     draw = ImageDraw.Draw(img_draw)
#     for i, (box, landmark) in enumerate(zip(boxes, landmarks)):
#         draw.rectangle(box.tolist(), width=5)
#         for p in landmark:
#             draw.rectangle((p - 10).tolist() + (p + 10).tolist, width=10)
#     return img_draw

def recognize_face(frame, dbpath):
    max_sim = 0
    detect_name = ''
    fv = []

    #顔検出
    max_sim, detect_name, fv = compare_similarity(frame, dbpath) 

    return max_sim, detect_name, fv

if __name__ == '__main__':
    # args = sys.argv
    # if 2 <= len(args):
    #     print(args[1], args[2])
    #     similarity(read_image(args[1]), read_image(args[2]))
    # else:
    #     print('Arguments are too short')
    print(similarity(read_image('images\しゅんすけ\しゅんすけ0.jpg'), read_image('images\しゅんすけ\しゅんすけ1.jpg')))
