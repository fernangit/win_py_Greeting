#https://ichi.pro/pyttsx-3-no-shokai-pythonyo-no-tekisuto-yomiage-konba-ta-81905511310787
import pyttsx3

# エンジンの初期化
engine = pyttsx3.init()
engine.setProperty('rate', 150)

voices = engine.getProperty('voices')
for voice in voices:
    print("Voice: %s" % voice.name)
    print(" - ID: %s" % voice.id)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)
    print("\n")

engine.setProperty("voice", voices[2].id)

# 読み上げるテキスト
engine.say("Hello, I am reading this text.")

# 読み上げ実行
engine.runAndWait()