#https://tsudango-tech.com/46/
from rembg import remove
from PIL import Image
import cv2
import numpy as np
import tkinter as tk
from tkinter import PhotoImage
import threading
import io
import pyautogui as pag

class ObjectDetection:
    def __init__(self, cap):
        self.root = tk.Tk ()
        self.root. overrideredirect (True) # タイトルバーを非表示にする
        self.cap = cap

        #カメラ解像度
        width = int (cap.get (cv2.CAP_PROP_FRAME_WIDTH))
        height = int (cap.get (cv2.CAP_PROP_FRAME_HEIGHT))

        # スプラッシュ画面の位置を画面の中央に設定
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x = (self.screen_width // 2) - (width // 2)
        y = (self.screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")  # スペースを削除
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
        #画像をPIL形式に変換
        img_pil = Image.fromarray (cv2.cvtColor (frame, cv2.COLOR_BGR2RGB))
        out_pil = remove (img_pil)

        #PIL画像をRGBA形式に変換
        out_pil = out_pil.convert ("RGBA")

        #PIL画像をバイナリデータに変換
        bio = io.BytesIO()
        out_pil.save (bio, format='PNG')
        bio.seek (0)

        #Photolmageに変換
        image = PhotoImage (data=bio.getvalue())

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