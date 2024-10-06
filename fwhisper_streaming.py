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
                self.audio = self.recognizer.listen(source, timeout=1000.0, phrase_time_limit=3)
                print("録音終了")
        except:
            print('mic error')

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
        segments, info = model.transcribe(WAVE_OUTPUT_FILENAME, beam_size=5, language='ja')

        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        text = ''
        for segment in segments:
            if segment.text == 'ご視聴ありがとうございました' :
                continue
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            text += segment.text

        return text

    def get_message(self, model):
        while(True):
            recog_result = self.get_asr_result(model)
            if recog_result != '':
                break

        return recog_result

    def kill(self):
        pass

def main():
    fwhisper = FWhisper()

    print("＜認識開始＞")
    recog_result = fwhisper.get_asr_result(fwhisper.init())
    print(f"認識結果: {recog_result}")
    print("＜認識終了＞")

if __name__ == "__main__":
    main()