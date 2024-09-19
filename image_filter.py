#https://hiroki.jp/detect_blur
import cv2
import numpy as np
import sys
import time
import dlib

#Initialize face detector and shape predictor
detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor('dlib_mdl/shape_predictor_68_face_landmarks.dat')

#ピンぼけ度合をスコア化
def get_image_score(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian =  variance_of_laplacian(gray)
#    print('image_score = ', laplacian)
    return laplacian

#エッジ検出
def variance_of_laplacian(image):
    start = time.perf_counter()
    edge = cv2.Laplacian(image, cv2.CV_64F).var()
#    print('エッジ検出', time.perf_counter() - start)
    return edge

#シャープ化
def apply_sharp_filter(image):
    start = time.perf_counter()
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
#    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], np.float32)
    sharp = cv2.filter2D(image, -1, kernel)
#    print('シャープ化', time.perf_counter() - start)
    return sharp
    
#顔検出
def detect_faces(image):
    start = time.perf_counter()
    # 画像のグレースケール化
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 学習済みモデルの読み込み
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    # 顔を検出する
    lists = cascade.detectMultiScale(img_gray)
#    print('cv 顔検出', time.perf_counter() - start)
#    print('face lists = ', lists)
    return lists

#目検出
def detect_eyes(image):
    start = time.perf_counter()
    # 画像のグレースケール化
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 学習済みモデルの読み込み
    cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
    # 目を検出する
    lists = cascade.detectMultiScale(img_gray)
#    print('cv 目検出', time.perf_counter() - start)
#    print('eye lists = ', lists)
    return lists

#顔検出 dlib
def detect_faces_dlib(image):
    start = time.perf_counter()
    # 顔を検出する
    lists = detector(image)
#    print('dlib 顔検出', time.perf_counter() - start)
#    print('face lists = ', lists)
    return lists

if __name__ == '__main__':
    #args[1] = image_path
    args = sys.argv
    if 2 <= len(args):
        print(args[1])
        image = cv2.imread(args[1])
        get_image_score(image)
        faces = detect_faces(image)
        eyes = detect_eyes(image)
        print('eyes = ', len(eyes))
        for x, y, w, h in eyes:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imwrite('sample_after.png', image)
        sharp = apply_sharp_filter(image)
        get_image_score(sharp)
        cv2.namedWindow('window')
        cv2.imshow('window', sharp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('Arguments are too short')
