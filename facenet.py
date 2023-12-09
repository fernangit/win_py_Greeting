# -*- coding: utf-8 -*-
import sys
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageDraw
import numpy as np
import glob
import os
import time
import math
#from torch2trt import torch2trt

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

#### MTCNN ResNet のモデル読み込み
start = time.perf_counter()
#顔を検出して切り取る GPU使用
mtcnn = MTCNN(device=device, margin=10)
#mtcnn = MTCNN()
print('MTCNN読み込み', time.perf_counter() - start)
time.sleep(5)
start = time.perf_counter()
resnet = InceptionResnetV1(pretrained='vggface2').to(device).eval()
#resnet = InceptionResnetV1(pretrained='vggface2', device=device).eval()
#resnet = InceptionResnetV1(pretrained='vggface2').eval()
'''
# convert to TensorRT feeding sample data as input
#x = torch.ones((1, 3, 224, 224)).to(device)
img_cropped = Image.open('out.jpg')
x = img_cropped.unsqueeze(0).to(device)
resnet_trt = torch2trt(resnet, [x])
'''
print('モデル読み込み', time.perf_counter() - start)

### 顔切り出し
### imgはpill形式
#def crop_face(img):
#    batch_boxes, batch_probs, batch_points = mtcnn.detect(img, landmarks=True)
#    batch_boxes, batch_probs, batch_points = mtcnn.select_boxes(batch_boxes, batch_probs, batch_points, img, method=mtcnn.selection_method)
#    faces = mtcnn.extract(img, batch_boxes, None)
#    return faces, batch_boxes, batch_probs, batch_points

def detect_face_features(frame):
    #顔の特徴点を取得
    boxes, probs, landmarks = mtcnn.detect(frame, landmarks=True)
#    print(landmarks)

    keypoints = landmarks[0]
    left_eye = keypoints[LEFT_EYE]
    right_eye = keypoints[RIGHT_EYE]
    nose = keypoints[NOSE]
    mouth_left = keypoints[MOUTH_LEFT]
    mouth_right = keypoints[MOUTH_RIGHT]

    return left_eye, right_eye, nose, mouth_left, mouth_right

def frontal_face(frame):
    #顔の特徴点を取得
    left_eye, right_eye, nose, mouth_left, mouth_right = detect_face_features(frame)

    #顔の向きを判定
    is_frontal = True
    
    #目の位置関係をチェック
    left_eye_nose = math.sqrt(((left_eye[0] - nose[0])**2) + ((left_eye[1] - nose[1])**2))
    right_eye_nose = math.sqrt(((right_eye[0] - nose[0])**2) + ((right_eye[1] - nose[1])**2))
    print('distance ratio LReyes-nose:', (left_eye_nose / right_eye_nose))
    if (left_eye_nose / right_eye_nose > 1.05) or (left_eye_nose / right_eye_nose < 0.95):
        is_frontal = False

    #口の位置関係をチェック
    mouth_left_nose = math.sqrt(((mouth_left[0] - nose[0])**2) + ((mouth_left[1] - nose[1])**2))
    mouth_right_nose = math.sqrt(((mouth_right[0] - nose[0])**2) + ((mouth_right[1] - nose[1])**2))
    print('distance ratio mouthLR-nose:', (mouth_left_nose / mouth_right_nose))
    if (mouth_left_nose / mouth_right_nose > 1.05) or (mouth_left_nose / mouth_right_nose < 0.95):
        is_frontal = False

    if is_frontal == True:
        print('frontal face')
    
    return is_frontal

### 顔検出
def detect_face(img, path=''):
    if path == '':
        return mtcnn(img)
    else:
        return mtcnn(img, save_path=path)

### 顔検出
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
    jpg_files = glob.glob(inp + '/' + '*.jpg')
    for jpg in jpg_files:
        # ファイル名取得
        basename = os.path.splitext(os.path.basename(jpg))[0]
        print(basename)
        # ベクトル化
#        fv = feature_vector(Image.open(jpg))
        try:
            fv = feature_vector(mtcnn(Image.open(jpg)))
        except:
            print('feature_vector error')
            continue
        # numpy形式でベクトル保存
        vector = outp + '/' + basename
        np.save(vector, fv.astype('float32'))

#### 画像ファイルから画像の特徴ベクトルを取得(ndarray 512次元)
### img_croppedはmtcnnで抽出したもの
def feature_vector(img_cropped):
    feature_vector = resnet(img_cropped.unsqueeze(0).to(device))
#    feature_vector = resnet_trt(img_cropped.unsqueeze(0).to(device))
#    feature_vector = resnet(img_cropped.unsqueeze(0))
    feature_vector_np = feature_vector.squeeze().to('cpu').detach().numpy().copy()
    return feature_vector_np

#### 2つのベクトル間のコサイン類似度を取得(cosine_similarity(a, b) = a・b / |a||b|)
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

#### 2枚の画像間の類似度を取得
### img = Image.open(image)
### imgはmtcnnで抽出したもの
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
### imgはmtcnnで抽出したもの
def compare_similarity(img_cropped, path):
    #特徴ベクトル算出
    start = time.perf_counter()
    in_fv = feature_vector(img_cropped)
    print('特徴ベクトル算出', time.perf_counter() - start)
    maxsim = 0.0
    detect = ''
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

def draw_boxes(img, boxes, probs, landmarks):
    img_draw = img.copy()
    draw = ImageDraw.Draw(img_draw)
    for i, (box, landmark) in enumerate(zip(boxes, landmarks)):
        draw.rectangle(box.tolist(), width=5)
        for p in landmark:
            draw.rectangle((p - 10).tolist() + (p + 10).tolist, width=10)
    return img_draw

if __name__ == '__main__':
    args = sys.argv
    if 2 <= len(args):
        print(args[1], args[2])
        similarity(Image.open(args[1]), Image.open(args[2]))
    else:
        print('Arguments are too short')
