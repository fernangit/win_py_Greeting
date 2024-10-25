# -*- coding: utf-8 -*-
import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone(device_index = 0)

def init():
    pass

def kill():
    pass

def get_message():
    with mic as source:
        r.adjust_for_ambient_noise(source)  #雑音対策
        audio = r.listen(source)

    user_message = r.recognize_google(audio, language='ja-JP')

    return user_message, '', 0.0

if __name__ == '__main__':
    print('音声認識開始')
    recog_result = get_message()
    print('音声認識結果 ', recog_result)
    print('音声認識終了')
