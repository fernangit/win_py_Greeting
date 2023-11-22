import threading
import speech_recognition as sr
#import ELYZA_res
import talk

r = sr.Recognizer()
mic = sr.Microphone(device_index = 0)

def elyza_chat():
    response = ''
    with mic as source:
        r.adjust_for_ambient_noise(source)  #雑音対策
        audio = r.listen(source)

    try:
        user_message = r.recognize_google(audio, language='ja-JP')
        print(user_message)
#        response = ELYZA_res.elyza_response(user_message)
    except:
        response = '声が聞き取れませんでしたー'

    return response

def chat_sentence():
    thread = threading.Thread(target = chat_sentence_thread)
    thread.start()

def chat_sentence_thread():
    while(True):
        talk.read_text(elyza_chat())

if __name__ == '__main__':
    chat_sentence()