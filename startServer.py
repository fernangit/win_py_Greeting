#https://aiacademy.jp/media/?p=57
#http://localhost:8000/
from flask import Flask, request

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/StreamingAssets/Utterance', methods=['POST'])
def updateUtter():
    print('post');
    
    filename = 'StreamingAssets/Utterance/utter.txt'
    utterance = request.form['utterance']
    print(filename);
    print(utterance);
    with open(filename, mode='w') as fout:
        fout.write(utterance.encode('utf-8'))

    filename = 'StreamingAssets/Utterance/score.txt'
    score = request.form['score']
    print(filename);
    print(score);
    with open(filename, mode='w') as fout:
        fout.write(score.encode('utf-8'))

    print('writed!');
        
    return utterance

def startServer(url, pnum):
    app.run(host=url, port=pnum, debug=True)

if __name__ == '__main__':
    startServer('localhost', 8000)
