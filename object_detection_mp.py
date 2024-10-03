#https://zenn.dev/ykesamaru/articles/e0380990465d34
import cv2
import mediapipe as mp
import numpy as np
import io
from PIL import Image
import tkinter as tk
from tkinter import PhotoImage 
import threading

class ObjectDetection:
    def __init__(self, cap):
        # MediaPipeのSelfie Segmentation モデルを読み込み
        mp_selfie_segmentation = mp.solutions.selfie_segmentation
        #selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation (model_selection=0)
        self.selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation (model_selection=1)
        self.root = tk.Tk ()
        self.root. overrideredirect (True) # タイトルバーを非表示にする
        self.cap = cap

        #カメラ解像度
        width = int (cap.get (cv2.CAP_PROP_FRAME_WIDTH))
        height = int (cap.get (cv2.CAP_PROP_FRAME_HEIGHT))

        # スプラッシュ画面の位置を画面の中央に設定(少しずらす)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x = (self.screen_width // 2) - (width // 2)
        y = (self.screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x-100}+{y}")  # スペースを削除
        self.root.wm_attributes('-transparentcolor', "white")  # 背景色を透明に

        # 画像表示用ラベル
        self.image_label = tk. Label (self. root, bg='white')
        self.image_label.pack (expand=True)
        self.running = True

    def front (self):
        self.root.wm_attributes ('-topmost', True) #常に最前面に表示

    def back (self):
        self.root.wm_attributes ('-topmost', False) #後面に表示
        self.root.lower ()

    def splash_image (self, frame) :
        #フレームの前処理と推論
        frame = frame_rgb = cv2.cvtColor (frame, cv2.COLOR_BGR2RGB)
        result = self.selfie_segmentation. process (frame_rgb)
        
        # 推論結果をマスクとして用い、 元のフレームから人物部分だけを切り出す
        mask = result.segmentation_mask > 0.1
        
        # アルファチャンネルの作成
        alpha = np.ones (mask.shape, dtype=np. uint8) * 255 #すべてのピクセルを不透明にする
        alpha[~mask] = 0 #マスクが0の部分(人物以外の部分)を透明にする

        #元のフレームとアルファチャンネルを結合
        frame_bgra = cv2.cvtColor (frame, cv2.COLOR_BGR2BGRA)
        frame_bgra[..., 3] = alpha

        # 結果をPNGに変換
        result = cv2.resize (frame_bgra, (self.screen_width, self.screen_height)) #結果のサイズをウィンドウのサイズに合わせて変更
        img = Image. fromarray (result)
        bio = io.BytesIO()
        img.save (bio, format='PNG')
        imgbytes = bio.getvalue()

        #Photolmageに変換
        image = PhotoImage (data=imgbytes)

        # 画像を表示する
        self.image_label.config (image=image)
        self.image_label.image = image #参照を保持
        self.root.update_idletasks()
        self.root.update()

    def update_image (self):
        while self.running:
            #カメラから画像を読み込む
            ret, frame = self.cap.read()
            self.splash_image (frame)

    def show (self):
        threading.Thread (target=self.update_image, daemon=True).start () #スレッドで画像更新を開始
        self.root.mainloop ()

    def close (self):
        self.running = False
        self.cap.release () #カメラを解放
        self.root.destroy ()

#メインアプリケーション
if __name__ == '__main__':
    #USBカメラのindex番号を指定
    camera_index = 0
    cap = cv2.VideoCapture (camera_index)
    objedetect = ObjectDetection (cap)
    try:
        objedetect.show ()
    except KeyboardInterrupt:
        objedetect.close () 