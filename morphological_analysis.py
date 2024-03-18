#【チュートリアル】機械学習を使って30分で固有表現抽出器を作る
#https://qiita.com/Hironsan/items/326b66711eb4196aa9d4
#【超簡単】WindowsのPythonとMeCabで形態素解析しようぜ！
#https://resanaplaza.com/2022/05/07/%e3%80%90%e8%b6%85%e7%b0%a1%e5%8d%98%e3%80%91windows%e3%81%aepython%e3%81%a8mecab%e3%81%a7%e5%bd%a2%e6%85%8b%e7%b4%a0%e8%a7%a3%e6%9e%90%e3%81%97%e3%82%88%e3%81%86%e3%81%9c%ef%bc%81/

# ”環境変数の編集”で"Path"を選択し、”編集”の"新規"で
# (システムドライブ名):\Program Files\MeCab\bin
# などMeCabのインストール先のパスを追加します。
# (MeCabのインストール先)/bin
# にある"libmecab.dll"というファイルを
# \venv\Lib\site-packages
# にコピー＆ペーストしてください。

#MeCabでオリジナル辞書を作成する
#https://qiita.com/nnahito/items/16c8e214d71fbc23ed8e
#mecab-dict-index -d D:\work\win_py_Greeting\venv\Lib\site-packages\ipadic\dicdir -u original.dic -f utf-8 -t utf-8 original.csv

import MeCab

def extract_proper_nouns(text):
    tagger = MeCab.Tagger()
    words = []
    node = tagger.parseToNode(text)
    while node:
        tkn = node.feature.split(',')
        if tkn[2] in ['人名']:
            words.append(node.surface)
        node = node.next
        
    print(words)
    return words

if __name__ == '__main__':
    words = extract_proper_nouns('すみません、つなきさんと本廣さんと植田さん呼んでください')