#https://qiita.com/hatt_takumi/items/d65c243294f250724c19
import json
import requests
import wave
import winsound
import subprocess
import threading

def init():
    result = subprocess.run(".\VOICEVOX\VOICEVOX.exe /a /b /c, capture_output=True, text=true")
    print(result)

def generate_wav(text, speaker=1, filepath='./audio.wav'):
    host = 'localhost'
    port = 50021
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    headers = {'Content-Type': 'application/json',}
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(response2.content)
    wf.close()

def vtalk(t, speaker=1, filepath='./audio.wav'):
#    for i in range(30):
#        print(i)
        speaker = 8
        generate_wav(t, speaker, filepath)
        winsound.PlaySound(filepath, winsound.SND_FILENAME)

x = threading.Thread(target=init)
x.start()

if __name__ == '__main__':
    text = 'サンキュー フォーリーディング マイ ブログ'
    vtalk(text)
