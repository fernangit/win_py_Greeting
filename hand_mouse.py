# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Mediapip初期化
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

#画面の幅と高さを取得
screen_width, screen_height = pyautogui.size()

#クリック状態を追跡するフラグ
is_clicking = False

hands = mp_hands.Hands(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)

def is_palm_facing_camera(hand_landmarks, handedness_label):
    #ランドマークの座標を取得
    landmarks = np.array([(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark])

    #手首（ランドマーク０）と中指の根元（ランドマーク９）のベクトルを計算
    wrist_to_middle_finger = landmarks[9] - landmarks[0]

    #手首（ランドマーク０）と人差指の根元（ランドマーク５）のベクトルを計算
    wrist_to_index_finger = landmarks[5] - landmarks[0]

    #２つのベクトルの外積を計算して法線ベクトルを求める
    normal = np.cross(wrist_to_middle_finger, wrist_to_index_finger)

    #右手の場合は法線ベクトルが負の方向を向いているかどうかを判断
    #左手の場合は法線ベクトルが正の方向を向いているかどうかを判断
    if handedness_label == 'Right':
        return normal[2] < 0
    else:
        return normal[2] > 0
    
def detect_hand_mouse(img):
    global screen_width, screen_height
    global is_clicking

    #画像を左右反転し、BGRからRGBに変換
    img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
    img.flags.writeable = False
    results = hands.process(img)

    #画像を再度BGRに変換
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    #手のランドマークが検出された場合
    if results.multi_hand_landmarks and results.multi_handedness:
        #一番大きなバウンディングボックスを持つ手を選ぶ
        largest_hand = None
        largest_hand_label = None
        max_area = 0
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            #バウンディングボックスの計算
            x_min = min([landmark.x for landmark in hand_landmarks.landmark])
            y_min = min([landmark.y for landmark in hand_landmarks.landmark])
            x_max = max([landmark.x for landmark in hand_landmarks.landmark])
            y_max = max([landmark.y for landmark in hand_landmarks.landmark])
            area = (x_max - x_min) * (y_max - y_min)
            if area > max_area:
                max_area = area
                largest_hand = hand_landmarks
                largest_hand_label = handedness.classification[0].label

        if largest_hand:
            mp_draw.draw_landmarks(img, largest_hand, mp_hands.HAND_CONNECTIONS)

            #画像の幅と高さを取得
            image_width, image_height = img.shape[1], img.shape[0]

            #人差し指の座標値を取得
            index_finger_tip_x = int(largest_hand.landmark[8].x * image_width)
            index_finger_tip_y = int(largest_hand.landmark[8].y * image_height)

            #親指の座標値を取得
            thumb_tip_x = int(largest_hand.landmark[4].x * image_width)
            thumb_tip_y = int(largest_hand.landmark[4].y * image_height)
            thumb_pip_x = int(largest_hand.landmark[3].x * image_width)
            thumb_pip_y = int(largest_hand.landmark[3].y * image_height)
            # print('thumb_tip_x', thumb_tip_x, 'thumb_pip_x', thumb_pip_x)
            # print('thumb_tip_y', thumb_tip_y, 'thumb_pip_y', thumb_pip_y)

             #人差し指の座標を画面全体にマッピング
            screen_x = int(index_finger_tip_x * screen_width / image_width)
            screen_y = int(index_finger_tip_y * screen_height / image_height)

            #手の内側か手の甲かを判定する
            if is_palm_facing_camera(largest_hand, largest_hand_label):
                #親指を曲げ伸ばしでクリック
                if thumb_tip_x < thumb_pip_x:
                    if not is_clicking:
                        pyautogui.mouseDown(button='left')
                        print('mouse down')
                        is_clicking = True
                elif thumb_tip_x >= thumb_pip_x:
                    if is_clicking:
                        pyautogui.mouseUp(button='left')
                        print('mouse up')
                        is_clicking = False

                #マウスを指の位置に移動
#                print('mouse x:', screen_x, 'mouse y:', screen_y)
                pyautogui.moveTo(screen_x, screen_y)

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()

        #ハンドマウス
        detect_hand_mouse(img)

        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break