# -*- coding: utf-8 -*-
from datetime import datetime
import time
import random
import copy

import cv2 as cv
import numpy as np
import threading
import pyautogui

import pose_detect
import face_recog_model
import motion
import talk
import regist_detected
import send_receive_server
import image_filter
import hand_gesture
import LLM_chat
import CLS_chat
import read_code
import object_detection_mp
#import object_detection_rembg

#face recognition mode
FACE_RECOGNITION_FACENET = 0
FACE_RECOGNITION_INSIGHTFACE = 1

#時刻初期化
def initialize_time():
    #現在時刻読み取り
    d = datetime.now()
    nxt_h = d.hour
    nxt_m = random.randint(0, 59)
    t_st = time.time()
    
    return nxt_h, nxt_m, t_st

#デバイス初期設定
def initialize_devices(device_id):
    #カメラの設定　デバイスIDは0
    cap = cv.VideoCapture(device_id)
    #OpenPose用デバイス設定
    pose_detect.set_openpose_device('gpu')

    return cap

#モデル初期化
def initialize_model(face_recog_mode):
    #顔認識モデル
    if face_recog_mode == FACE_RECOGNITION_FACENET:
        face_model = face_recog_model.facenet_model()
    elif face_recog_mode == FACE_RECOGNITION_INSIGHTFACE:
        face_model = face_recog_model.insightface_model()
    face_model.import_lib()

    return face_model
           
#画像サイズ変換
def scale_to_resolation(img, resolation):
    h, w = img.shape[:2]
    scale = (resolation / (w * h)) **0.5
    
    return cv.resize(img, dsize = None, fx = scale, fy = scale)

#フレーム補正
def correct_frame(frame):
    #画像サイズ変換
    frame = scale_to_resolation(frame, 320 * 240)

    #画像シャープ化
    frame = image_filter.apply_sharp_filter(frame)
    
    return frame

#フレーム除外
def exclude_frame(frame):
    #score 100未満をピンボケ画像として除外
    score = image_filter.get_image_score(frame)
    if score < 100:
        return False

    '''
    #顔が検出できなければ除外
    faces = image_filter.detect_faces_dlib(frame)
    if len(faces) < 1:
        return False

    #顔が検出できなければ除外
    faces = image_filter.detect_faces(frame)
    if len(faces) < 1:
        return False

    #目が2つ検出できなければ除外
    eyes = image_filter.detect_eyes(frame)
    if len(eyes) < 2:
        return False

    #画像サイズが所定のサイズより小なら除外（カメラからの距離を推定）
    height, width = frame.shape[:2]
#    print("height:", height)
#    print("width:", width)
    '''
    return True

#起動セリフ＆モーション
def opening():
    #起動セリフ
    talk.opening()

    #起動モーション
    motion.set_first_motion()

#定期的セリフ＆モーション
def regulary(d, nxt_h, nxt_m, t_st):
    #30分でスリープ
    if (time.time() - t_st) > (60 * 30):
        #Sleepモーション
        motion.set_sleep_motion()
        t_st = time.time()

    #所定時刻の所定モーション呼び出し
    motion.set_default_motion(d)

    #独り言
    nxt_h, nxt_m = talk.monologue(d, nxt_h, nxt_m)

    #定時アナウンス
    talk.announce(d, nxt_h, nxt_m, 'sentences/announce.txt')

    return nxt_h, nxt_m, t_st

#骨格検出
def detect_point(hasFrame, frame, org_frame, greeting):
    cropped_face = False
    cropped_frame = org_frame
    
    #OpenPose呼び出し
    points = pose_detect.getpoints(hasFrame, frame)

    #有効Point取り出し
    v_points= [p for p in points if p != None]

    #有効ポイント10以上
    if (len(v_points) > 10):
        #挨拶する
        greeting = True
        #0：頭、1：首を取得できているか
        if points[0] != None and points[1] != None:
            print("detect face")
            cropped_face = True
            #0：頭、1：首を設定
            f_point = []
            f_point.append(points[0])
            f_point.append(points[1])
            #顔周辺の画像を切り出す             
            cropped_frame = pose_detect.crop_frame(f_point, org_frame)

    return greeting, cropped_face, cropped_frame

#顔検出
def detect_face(frame):
    #for debug
#    cv.imshow('Input', frame)
#    cv.moveWindow('window name', 100, 100)

    #ポーズ省略の場合
    cropped_frame = frame
    cropped_face = True
    
    return cropped_frame, cropped_face
    
#顔認証
def authenticate_face(face_recog_model, cropped_frame, greeting):
    max_sim = 0
    detect_name = ''

    #顔認証
    max_sim, detect_name, fv = face_recog_model.recognize_face(cropped_frame)
    
    #挨拶する
    if max_sim != 0.0:
        greeting = True

    #認証した？
    if(detect_name != ''):
        # 登録
        regist_detected.regist_detected(detect_name)
        #類似度80%以上で今回データで差し替え
        if max_sim > 0.8:
            vector = face_recog_model.get_facedb() + '/' + detect_name
            np.save(vector, fv.astype('float32'))

        #名前の抽出
        detect_name = detect_name.split('_')[0]
        #さん付け
        detect_name = detect_name + 'さん！'
        print('you are ', detect_name)

    return greeting, max_sim, detect_name

#挨拶
def greet_sub(d, url, max_sim, detect_name):
    #認識度レベル変換
    level = talk.percentage_to_level(max_sim, 0.7, motion.get_motion_num())
    if level > talk.len_utterance_op_lst() - 1:
        level = talk.len_utterance_op_lst() - 1

    #挨拶音声再生
    utter = talk.greeting(d, detect_name, talk.level_to_utterance(level))

    #挨拶モーション再生
    motion.set_level_motion(level)
    
    #発話内容をサーバーに送信
    send_receive_server.send_utterance(url, utter, str(max_sim), '', '')

    #発話内容をリセット
    threading.Thread(target=reset_utterance, args=(url,)).start()

#発話内容をリセット
def reset_utterance(url):
    time.sleep(7)
    send_receive_server.send_utterance(url, '', '0', '', '')

#フォト
def photo(chatmode, photomode, exitmode, phototime, frame, cls_chat, llm_chat, objdetect, intent, val, url):
    barcodeData = ''
    if exitmode == False:
        #バーコード／QRコード認識
        barcodeData, x, y, w, h = read_code.readCode (frame)
    #    barcodeData = 'aa' #for debug
        if photomode == False and barcodeData != '':
            #コード読み取り成功
            photomode = True
            print('photomode:True')

            #チャットモード抑制
            chatmode = False
            print('chatmode:False')

            #フォト画面最前面化
            objdetect.front()

            #フォトモード中の表示
            talk.read_text('さつえいちゅう。。。ピースサインでさつえいするよ')
            send_receive_server.send_utterance(url, '撮影中。。。ピースサインで撮影するよ', '0', '', '')
            phototime = time.time()
        
        if (photomode == True):
            objdetect.splash_image(frame)
            #フォトモードから30秒経過？
            if ((time.time() - phototime) > 30):
                #フォトモード終了
                objdetect.back() #後面に表示
                photomode = False
                print('photomode:False')

                #フォトモード中の表示を消す
                send_receive_server.send_utterance(url, '', '0', '', '')
    
    return photomode, phototime, barcodeData, chatmode, intent, val

#チャット
def chat(chatmode, exitmode, cls_chat, llm_chat, text, old_text, message, old_message, response, old_response, intent, val, url):
    exit = False
    #classification
    intent, val, text = cls_chat.get_user_intent()
    #前回と同じテキストなら更新なし
    if text == old_text:
        intent = ''
        val = 0

    if exitmode == False:
        #呼びかけ
        if  chatmode== False and val > 6.5:
            if intent == 'MAU' or intent == 'Greeting' or intent == 'CallOut':
                #呼びかけで会話モード開始
                print('＊＊＊会話モード開始＊＊＊')           
                talk.read_text('はいーなんでしょうかー')           
                chatmode = True
                print('chatmode:True')
                message = ''
                response = ''
                old_text = text
                #会話開始
                send_receive_server.send_utterance(url, '', '0', '', '')
                cls_chat.end()
                llm_chat.begin()
                print("chatmode ", chatmode)
            
        if chatmode == True:
            #30秒無言だと会話モード終了
            if ((time.time() - llm_chat.get_chat_time()) > 30):
                print('＊＊＊会話モード終了＊＊＊')           
                motion.set_byebye_motion()
                talk.talk('ばいばーい')
                chatmode = False
                print('chatmode:False')
                intent = ''
                val = 0
                cls_chat.reset_user_intent()
                #会話終了
                cls_chat.begin()
                llm_chat.end()
                send_receive_server.send_utterance(url, '', '0', '', '')
                print("chatmode ", chatmode)    

            #会話取得
            message = llm_chat.get_user_message()
            if message != old_message:
                old_message = message
                response = ''
                send_receive_server.send_utterance(url, '', '0', message, response)

            response = llm_chat.get_response()
            if response != old_response:
                old_response = response
                send_receive_server.send_utterance(url, '', '0', message, response)

    #終了モード
    else: # exitmode == True
        if val > 6.5 and intent == 'Positive':
            print('finished')
            talk.read_text('あいさつユニット終了します')
            exit = True
        elif val > 6.5 and intent != '':
            talk.read_text('あいさつユニット継続します')
            chatmode = False
            exitmode = False
            print('chatmode:False')
            cls_chat.reset_user_intent()
            #会話終了
            cls_chat.begin()
            llm_chat.end()
            send_receive_server.send_utterance(url, '', '0', '', '')
            print("chatmode ", chatmode)    

    return chatmode, exitmode, text, old_text, message, old_message, response, old_response, intent, val, exit

#挨拶
def greet(chatmode, photomode, exitmode, t_st, frame, hasFrame, face_model, mode, d, url):
    greeting = False
    if exitmode == False:
        #前回から8秒以上経過？
        if (chatmode == False) and (photomode == False) and ((time.time() - t_st) > 8):
            #元画像を保存
            org_frame = copy.copy(frame)

            if (mode == 0):
                #骨格検出
                greeting, cropped_face, cropped_frame = detect_point(hasFrame, frame, org_frame, greeting)

            elif (mode == 1):
                #顔検出
                cropped_frame, cropped_face = detect_face(org_frame)

            if cropped_face == True:
                #顔認証
                greeting, max_sim, detect_name = authenticate_face(face_model, cropped_frame, greeting)

            #挨拶する
            if greeting == True:
                greet_sub(d, url, max_sim, detect_name)
                t_st = time.time()

    return t_st

#ジェスチャ
def gesture(chatmode, photomode, exitmode, frame, barcodeData, objdetect, llm_chat, cls_chat, d, url):
    if exitmode == False:
        #OK gesture
        h_gesture = hand_gesture.detect_hand_gesture(frame)
        if chatmode == False:
            if h_gesture == hand_gesture.H_THUMBS_UP:
                #OK motion
                motion.set_goodjob_motion()
                talk.talk('グッッジョーーブ')   
                time.sleep(3)       

            #response
            elif h_gesture == hand_gesture.H_PAPER:
                #response1 motion
                res_key = motion.set_response1_motion()
                talk.talk(talk.level_to_utterance(motion.response1_dict[res_key]))        
                time.sleep(3)
            elif h_gesture == hand_gesture.H_PEACE:
                #response2 motion
                res_key = motion.set_response2_motion()
                talk.talk(talk.level_to_utterance(motion.response2_dict[res_key]))        
                time.sleep(3)

                ###### for photo
                if photomode == True:
                    #全画面のスクリーンショットを撮る
                    photofile = 'photo/' + d.strftime('%Y%m%d_%H%M%S') + barcodeData + '.png'
                    pyautogui.screenshot(photofile)
                    objdetect.back()
                    photomode = False
                    print('photomode:False')
                    #フォトモード中の表示を消す
                    send_receive_server.send_utterance(url, '', '0', '', '')
                ###### for photo

        if h_gesture == hand_gesture.H_THUMBS_DOWN:
            #システム終了
            talk.read_text('あいさつユニット終了します。よろしいですか？')
            #チャットモード抑制
            chatmode = False
            llm_chat.end()
            cls_chat.begin()
            #クラスタースレッドリセット
            cls_chat.reset_user_intent()
            exitmode = True

    return chatmode, photomode, exitmode

#挨拶メイン関数
def greeting_main(url, mode = 0):
    #サーバ起動済み＆WebGL起動済みであること

    #時刻初期化
    nxt_h, nxt_m, t_st = initialize_time()

    #デバイス初期設定
    cap = initialize_devices(0)
    
    #モデル選択
    face_model = initialize_model(FACE_RECOGNITION_INSIGHTFACE)

    #起動セリフ＆モーション
    opening()
    time.sleep(7)
    
    #読み上げ開始
#    talk.read_sentence()
    
    # チャット
    llm_chat = LLM_chat.chat(LLM_chat.SPEECH_RECOGNITION_VOSK, LLM_chat.LLM_ELYZA)
    llm_chat.end()
    chatmode = False
    print('chatmode:False')
    message = old_message = ''
    response = old_response = ''
    
    # 意図抽出
    cls_chat = CLS_chat.clsChat(CLS_chat.SPEECH_RECOGNITION_VOSK)
    cls_chat.begin()
    text = old_text = ''
    intent = ''
    val = 0

    #フォトモード初期化
    photomode = False
    print('photomode:False')
    phototime = time.time()
    barcodeData = ''

    #スプラッシュスクリーン
#    pcap = cv.VideoCapture(1) #別カメラ使用
    pcap = cap
    objdetect = object_detection_mp.ObjectDetection(pcap)
#    objdetect = object_detection_rembg.ObjectDetection(pcap)
    objdetect.back()

    exitmode = False

    while True:
        cv.waitKey(1)
        
        #現在時刻読み取り
        d = datetime.now()

        #定期的セリフ＆モーション
        nxt_h, nxt_m, t_st = regulary(d, nxt_h, nxt_m, t_st)

        #画面キャプチャ
        hasFrame, frame = cap.read()
        if not hasFrame:
            print("Error reading frame. Reinitializing camera...")
            cap.release()
            cap = initialize_devices(0)
            continue

        #フォト
        photomode, phototime, barcodeData, chatmode, intent, val \
        = photo(chatmode, photomode, exitmode, phototime, frame, cls_chat, llm_chat, objdetect, intent, val, url)

        #チャット
        chatmode, exitmode, text, old_text, message, old_message, response, old_response, intent, val, exit \
        = chat(chatmode, exitmode, cls_chat, llm_chat, text, old_text, message, old_message, response, old_response, intent, val, url)
        if exit == True:
            cls_chat.kill()
            llm_chat.kill()
            return

        #挨拶
        t_st = greet(chatmode, photomode, exitmode, t_st, frame, hasFrame, face_model, mode, d, url)

        #ジェスチャ
        chatmode, photomode, exitmode = gesture(chatmode, photomode, exitmode, frame, barcodeData, objdetect, llm_chat, cls_chat, d, url)        

        #debug
        frame = correct_frame(frame) #入力フレーム補正
        cv.imshow('Image', frame)

if __name__ == '__main__':
    # #args[1] = server url ex.localhost:8000
    # #args[2] = mode 0:通常/1:ポーズ省略
    # args = sys.argv
    # if 2 <= len(args):
    #     print(args[1])
    #     print(args[2])
    #     url = 'http://' + args[1] + '/StreamingAssets/Utterance'
    #     print(url)
    #     greeting_main(url, int(args[2]))
    # else:
    #     print('Arguments are too short')
    greeting_main('http://localhost:8000/StreamingAssets/Utterance', 1)

