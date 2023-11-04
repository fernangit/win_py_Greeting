import os
import sys
import cv2
from PIL import Image, ImageDraw
import numpy as np
import glob

import cv2pil
import facenet
import keyinput

class featureRegister:
    #初期化
    mode = 0
    skip = False
    count = 0
    registnum = 0

#カメラの設定　デバイスIDは0
cap = cv2.VideoCapture(0)

def save_faceFeature(dbpath):
    fr = featureRegister()
    keywait = True

    #ダミー
    img_crop(cap, False)

    #名前の入力
    name = input('名前_Numberを入力してください：')
    #名前の重複チェック
    fr.count = check_name(dbpath, name)
    print('count:', fr.count)

    key = input('データ登録を開始しますか？　Yes:y：')
    #ビデオ入力開始
    while(True):
        ret, face = img_crop(cap, keywait)
        cv2.waitKey(1)
        #ord：文字を10進数で表記されるアスキーコードへ変換する
        if keywait == True and key == 'y':
            print('顔データ登録開始')
            keywait = False
        elif key == 'n':
            print('顔データ登録終了')
            break

        #顔データ登録開始
        if keywait == False:
            #顔が見つかなれば継続
            if (face == None):
                continue

            #マスクなしモード設定
            if fr.mode == 0:
                fr.mode = 1

            #データ登録
            if fr.mode == 1 or fr.mode == 2:
                regist_faceFeature(face, dbpath, name, fr)

            #データチェック
            if fr.mode == 3:
                check_faceFeature(face, dbpath, name, fr)

            if fr.skip == True or fr.mode == 3:
                key = input('登録終了しますか？　Yes:y No:n：')
                if key == 'y':
                    print('登録終了')
                    break
                else:
                    #名前の入力
                    name = input('名前_Numberを入力してください：')
                    #名前の重複チェック
                    fr.count = check_name(dbpath, name)
                    print('count:', fr.count)

                    key = input('データ登録を開始しますか？ Yes:y：')
                    fr.mode = 0
                    fr.skip = False
                    fr.count = 0
                    fr.registnum = 0
                    keywait = True

def regist_faceFeature(face, dbpath, name, fr):
    if fr.mode == 1:
        print('マスクなしモードを設定しますか？ Yes:y Skip:s', fr.registnum + 1)
    elif fr.mode == 2:
        print('マスクありモードを設定しますか？ Yes:y Skip:s', fr.registnum + 1)
    else:
        return

    key = input()

    regist_skip(fr, key)
#    print(fr.skip, fr.mode)
    if fr.skip == False:
        #データ登録
#        print('データ登録')
        regist_dbx3(face, dbpath, name, fr)
    else:
        fr.skip = False
        fr.mode = fr.mode + 1

def check_faceFeature(face, dbpath, name, fr):
    #テスト
    key = input('顔認証テストをしますか？ Yes:y Skip:s')
    regist_skip(fr, key)
    detect = ''
    if fr.skip == False:
        maxsim, detect, in_fv = facenet.compare_similarity(face, dbpath)
        if detect == '':
            print('顔認証テスト　NG')
        else:
            print('you are ', detect)

def check_name(dbpath, name):
    maxnum = 0
    count = 0
    #dbpathにある同じ名前のファイルを検索
    for file in glob.glob(dbpath + '/' + name + '*.npy'):
#        print(file)
        fname = os.path.splitext(os.path.basename(file))[0]
        num = int(fname.split('_')[2])
#        print('num:', num)
        #番号の二桁目以上を取得
        num = int(num / 10)
        #番号の最大値を取得
        if num > maxnum:
            maxnum = num
    print('maxnum:', maxnum)
    #カウントアップしてcountを返す
    count = (maxnum + 1) * 10

    return count

def img_crop(cap, keywait):
    #初期化
    ret = True
    face = None
    #カメラからの画像取得
    ret, frame = cap.read()
    #画像表示
    cv2.imshow('camera', frame)

    if keywait == False:
        #OpenCV→Pill変換
        pill = cv2pil.cv2pil(frame)
        #顔検出
        face = facenet.detect_face(pill, 'out.jpg')
        print(face)
        #顔が見つかれば認証
        if (face != None):
            print('顔検出OK')
            # 画像ファイルの読み込み(カラー画像(3チャンネル)として読み込まれる)
            img = cv2.imread('out.jpg')
            # 画像の表示
            cv2.imshow('face', img)
            ret = True
        else:
            print('顔検出NG')
            ret = False

    return ret, face

def regist_dbx3(img_cropped, dbpath, name, fr):
    #データ登録
    regist_db(img_cropped, dbpath, name + '_' + str(fr.count))
    fr.count = fr.count + 1
    fr.registnum = fr.registnum + 1
    #3枚登録
    if fr.registnum >= 3:
        fr.skip = False
        fr.mode = fr.mode + 1
        fr.registnum = 0

def regist_db(img_cropped, dbpath, name):
    #切り出し画像でデータ作成
    fv = facenet.feature_vector(img_cropped)
    #DB登録
    vector = dbpath + '/' + name
    np.save(vector, fv.astype('float32'))

def regist_skip(fr, key):
    if key == 's':
        #スキップする
        skip = True
    else:
        #スキップしない
        skip = False

if __name__ == '__main__':
    #args[1] = dbpath
    args = sys.argv
    if 1 <= len(args):
        print(args[1])
        save_faceFeature(args[1])
    else:
        print('Arguments are too short')

