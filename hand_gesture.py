# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import time
import math

#ジェスチャー種類
H_NO_GESTURE = 0
H_THUMBS_UP = 1
H_THUMBS_DOWN = 2
H_PAPER = 3
H_PEACE = 4

fingertop = [5, 9, 13, 17, 21]
fingerbot = [3, 6, 10, 14, 18]
thumbs = [2, 3, 4, 5]
parm = 1

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

#ハンド座標配列の初期化
p = [[[0] * 3 for i in range(25)] for j in range(2)]

#３次元２点間距離
def calculate_distance(point1, point2):
    distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2 + (point1[2] - point2[2]) ** 2)

    return distance

#指先ー手のひら相対距離
def relative_distance(hand, finger):
    fdis = []
    for i in range(len(finger)):
        fdis.append(calculate_distance(hand[parm - 1], hand[finger[i] - 1]))

    return fdis

#いいね
def detect_tumbs(fdis):
    #親指以外の指先が手のひらと近い、親指が手のひらから遠い
    if fdis[0] > 150:
        for i in range(len(fdis) - 1):
            if fdis[i + 1] > 150:
                return False
    else:
        return False

    return True

def detect_thumbs_updown(hand):
    #親指が手のひらより上かしたか
    if hand[parm - 1][1] > hand[thumbs[3]][1]:
        return True
    else:
        return False

#パー
def detect_paper(hand):
    #すべての指先が第三関節より上
    for i in range(len(fingertop)):
        if hand[fingertop[i]-1][1] > hand[fingerbot[i]-1][1]:
            return False
    #すべての指先が手のひらより上
    for i in range(len(fingertop)):
        if hand[fingertop[i]-1][1] > hand[0][1]:
            return False
    #親指以外の指先が親指先より上
    for i in range(len(fingertop)-1):
        if hand[fingertop[i+1]-1][1] > hand[fingertop[0]-1][1]:
            return False
    
    return True

#ピース
def detect_peace(hand):
    #人差し指、中指の指先が第三関節より上
    for i in range(2):
        if hand[fingertop[i+1]-1][1] > hand[fingerbot[i+1]-1][1]:
            return False
    #薬指、小指の指先が第三関節より上
    for i in range(2):
        if hand[fingertop[i+3]-1][1] < hand[fingerbot[i+3]-1][1]:
            return False
    
    return True

def get_landmark(hand_landmarks, hand):
    for i, lm in enumerate(hand_landmarks.landmark):
        p[hand][i][0] = lm.x
        p[hand][i][1] = lm.y
        p[hand][i][2] = lm.z

def display_landmark(img, hand_landmarks):
    for i, lm in enumerate(hand_landmarks.landmark):
        height, width, channel = img.shape
        cx, cy = int(lm.x * width), int(lm.y * height)
        cv2.putText(img, str(i + 1), (cx + 10, cy + 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

    mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

def detect_hand_gesture(img):
    #BGR -> RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #ハンドトラッキング
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hl, hand_landmarks in enumerate(results.multi_hand_landmarks):
            display_landmark(img, hand_landmarks)

            if hl < 2:
                get_landmark(hand_landmarks, hl)
                #指の第一関節と手のひらとの距離
                fdis = relative_distance(p[hl], fingerbot)
                avefdis = sum(fdis) / len(fdis)
                fdis = relative_distance(p[hl], fingertop)
                fdis = [(x / avefdis) * 100 for x in fdis]
#                print(hl, fdis[0], fdis[1], fdis[2], fdis[3], fdis[4])

                #hand gesture検出
                if detect_tumbs(fdis) == True and detect_thumbs_updown(p[hl])  == True:
                    print('thumbs up!')
                    return H_THUMBS_UP
                elif detect_tumbs(fdis) == True and detect_thumbs_updown(p[hl]) == False:
                    print('thumbs down!')
                    return H_THUMBS_DOWN
                elif detect_paper(p[hl]) == True:
                    print('paper!')
                    return H_PAPER
                elif detect_peace(p[hl]) == True:
                    print('peace!')
                    return H_PEACE

    return H_NO_GESTURE

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()

        #ジェスチャー検出
        ret = detect_hand_gesture(img)

        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

