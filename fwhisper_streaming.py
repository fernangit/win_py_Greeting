# -*- coding: utf-8 -*-
import speech_recognition as sr
import wave
import pyaudio
from faster_whisper import WhisperModel
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# 録音設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

class FWhisper:
    def init(self):
        model_size = "large-v3"
        #model_size = "small"

        # Run on GPU with FP16
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
        # or run on GPU with INT8
        # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
        # or run on CPU with INT8
        # model = WhisperModel(model_size, device="cpu", compute_type="int8")  

        # 音声認識の初期化
        self.recognizer = sr.Recognizer()

        return model

    def open_stream(self):
        try:
            #マイクから音声を取得
            with sr.Microphone() as source:
                print("録音開始...")
                self.recognizer.adjust_for_ambient_noise(source)
                # timeout パラメーターは、フレーズが開始されるのを待つ最大秒数です。この時間を超えると、諦めて speech_recognition.WaitTimeoutError 例外を投げます。timeout が None の場合、待機タイムアウトはありません。
                # phrase_time_limit パラメーターは、フレーズが続行されるのを許容する最大秒数です。この時間を超えると、フレーズの一部を処理した後、フレーズの残りを切り捨てて返します。結果として得られる音声は、時間制限時に切り取られたフレーズになります。phrase_time_limit が None の場合、フレーズの時間制限はありません。
#                self.audio = self.recognizer.listen(source, timeout=1000.0, phrase_time_limit=3)
                self.audio = self.recognizer.listen(source, timeout=100.0, phrase_time_limit=None)
                print("録音終了")
        except:
            print('mic error')
            # 音声認識の初期化
            self.recognizer = sr.Recognizer()            

    def recording(self, output):
        # 音声データをwavファイルに保存
        with wave.open(output, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(self.audio.get_wav_data())

        print(f"音声が{output}に保存されました。")

    def get_asr_result(self, model):
        #録音
        self.open_stream()
        self.recording(WAVE_OUTPUT_FILENAME)
        #音声認識
#        segments, info = model.transcribe(WAVE_OUTPUT_FILENAME, beam_size=5, language='ja')
        segments, info = model.transcribe(WAVE_OUTPUT_FILENAME, beam_size=5)

        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        text = ''
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            text += segment.text

        return text, info.language, info.language_probability

    def get_message(self, model):
        while(True):
            recog_result, lang, pbabirilty = self.get_asr_result(model)
            if recog_result != '':
                break

        return recog_result, lang, pbabirilty

    def kill(self):
        pass

def main():
    fwhisper = FWhisper()
    model = fwhisper.init()

    while True:
        print("＜認識開始＞")
        recog_result = fwhisper.get_asr_result(model)
        print(f"認識結果: {recog_result}")
        print("＜認識終了＞")

if __name__ == "__main__":
    main()