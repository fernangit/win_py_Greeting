import requests

def send_utterance(url, utterance, score):
    print(url)
    print(utterance)
    payload = {'utterance':utterance,'score':score}
    response = requests.post(url, data = payload)
    print(response)

def receive_utterance(url):
    print(url)
    utterance = requests.get(url).content.decode('cp932')
#    utterance = requests.get(url).content.decode('utf_8')
    print(utterance)
    return utterance

if __name__ == '__main__':
    send_utterance('http://localhost:8000/StreamingAssets/Utterance', 'テスト', 0)
    utterance = receive_utterance('http://localhost:8000/StreamingAssets/Utterance/utter.txt')
    print(utterance)
