import cv2
import cv2pil
import facenet
from PIL import Image

#カメラの設定　デバイスIDは0
cap = cv2.VideoCapture(0)

#繰り返しのためのwhile文
while True:
    #カメラからの画像取得
    ret, frame = cap.read()

    #OpenCV→Pill変換
    pill = cv2pil.cv2pil(frame)

    #顔検出
    face = facenet.detect_face(pill, 'out.jpg')
#    face = facenet.detect_face(pill, '')
    print(face)
    #顔が見つかれば認証
    if (face != None):
        #similarity
#        detectname = facenet.compare_similarity(Image.open('out.jpg'), 'facedb2') 
        detectname = facenet.compare_similarity(pill, 'facedb') 
        print('you are ', detectname)

    #カメラの画像の出力
    cv2.imshow('camera' , frame)
#    pill.show()

    #繰り返し分から抜けるためのif文
    key =cv2.waitKey(10)
    if key == 27:
        break

#メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()
