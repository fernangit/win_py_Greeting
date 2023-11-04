import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def frontal_face(frame):
    #dummy
    is_frontal = True
    
    if is_frontal == True:
        print('frontal face')
    
    return is_frontal

def detect_face(img, path=''):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # グレースケール変換
#    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 顔領域の探索
#    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    # ===== 初期検出実行 ======
    faces = face_cascade.detectMultiScale(img_gray, minSize=(100,100), minNeighbors=1)
    eyes = eye_cascade.detectMultiScale(img_gray, minSize=(50,50))
    # =========================

    # 検出されなかった
    if len(faces) == 0:
        return None
    
    # 目の位置を検出することによる傾き補正
    if len(eyes) == 2: # 目を合計３個以上誤検出した場合はスキップ
    
        w_ = abs((eyes[0][0] + eyes[0][2] / 2) - (eyes[1][0] + eyes[1][2] / 2))
        h_ = abs((eyes[0][1] + eyes[0][2] / 2) - (eyes[1][1] + eyes[1][2] / 2)) 
        tan_rad = np.arctan(h_ / w_)
        tan_deg = np.rad2deg(tan_rad)
    
        if 5 <= tan_deg < 30: # 顔が傾いていると判別する角度の判定
            center = (int(img_gray.shape[1]/2), int(img_gray.shape[0]/2))
            trans = cv2.getRotationMatrix2D(center, tan_deg, 1)
            img = cv2.warpAffine(img, trans, (img_gray.shape[1],img_gray.shape[0]))
            img_gray = cv2.warpAffine(img_gray, trans, (img_gray.shape[1],img_gray.shape[0]))

            # 傾き補正後再検出
            faces_ = face_cascade.detectMultiScale(img_gray, minSize=(100,100), minNeighbors=2)
        
            if len(faces_) > 0:
                faces = faces_

# ========================================

    (x, y, w, _) = faces[-1] # 複数検出時の対策

    pad_width = int(w / 3.5) # パディング量の調整
    h_adjast = int(w / 10) # 縦位置調整

    # 目の位置を考慮したトリミング調整
    eyes_distance = 0
    if len(eyes) == 2:
        eyes_distance = abs((eyes[0][0] + eyes[0][2] / 2) - (eyes[1][0] + eyes[1][2] / 2))

        if int(eyes_distance * 2.5) < w:
            w_new = int(eyes_distance * 2.5)

            x = int(x + (w-w_new) / 2)
            y = int(y + (w-w_new) / 2)
            w = w_new

    if x - pad_width < 0:
        pad_width = x
    if y - pad_width < 0:
        pad_width = y
    if y - pad_width - h_adjast < 0:
        h_adjast = 0

    face_crop = img[y-pad_width-h_adjast:y+w+pad_width-h_adjast, x-pad_width:x+w+pad_width]
    face_crop = cv2.resize(face_crop, dsize=(160, 160))

    if path != "":
        cv2.imwrite(path, face_crop)

    return face_crop

def detect_face_main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow("detect face", frame)
        key = cv2.waitKey(1) & 0xFF
        detect_face(frame, "out.jpg")

if __name__ == '__main__':
    detect_face_main()