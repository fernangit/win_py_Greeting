#https://alicia-ing.com/programming/python/pyttsx3-text-to-speech/
import pyttsx3
import rvc
import winsound

engine = pyttsx3.init()

# 音量の設定（0.0 から 1.0）
engine.setProperty('volume', 0.9)

# 速度（WPM: words per minute）
engine.setProperty('rate', 150)

# 音声（性別）の変更
voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[0].id)  # 男性の声
engine.setProperty('voice', voices[1].id)  # 女性の声

def etalk(t):
    engine.say(t)
    engine.runAndWait()

def ectalk(t, wfile='eread.wav', output='convert.wav'):
    ewrite(t, wfile)
    rvc.convert(wfile, output)
    winsound.PlaySound(output,  winsound.SND_FILENAME)

def ewrite(t, wfile='eread.wav'):
    engine.save_to_file(t, wfile)
    engine.runAndWait()

if __name__ == '__main__':
    etalk('pyttsx3 is a text-to-speech conversion library in Python. Unlike alternative libraries, it works offline, and is compatible with both Python 2 and 3.')
    ectalk('pyttsx3 is a text-to-speech conversion library in Python. Unlike alternative libraries, it works offline, and is compatible with both Python 2 and 3.', wfile='eread.wav', output='convert.wav')
