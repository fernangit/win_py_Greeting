import requests

def send_utterance(url, utterance, score, message, response):
    print(url)
    print(utterance)
    payload = {'utterance':utterance,'score':score,'message':message,'response':response}
    response = requests.post(url, data = payload)
    print(response)

def receive_utterance(url):
    print(url)
#    utterance = requests.get(url).content.decode('cp932')
    utterance = requests.get(url).content.decode('utf_8')
    print(utterance)
    return utterance

if __name__ == '__main__':
    send_utterance('http://localhost:8000/StreamingAssets/Utterance', 'テスト', 0, 'こんにちは', 'お疲れ様です')
    utterance = receive_utterance('http://localhost:8000/StreamingAssets/Utterance/utter.txt')
    print(utterance)
