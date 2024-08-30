#Lang Chainを使ったRAGElyza7bを用いて試してみた
#https://note com/alexweberk/n/n3cffc010e9e9
from langchain.memory import ConversationBufferWindowMemory
from datetime import datetime as dt
import os

def initialize(k):
    #メモリの初期化
    #最新のK個のやり取りが保存される
    memory = ConversationBufferWindowMemory(k=k)
    return memory

def memorize(memory, user, system):
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y年%m月%d日％H時％M分'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
    #ユーザーメッセージとA1 メッセージの追加{
    memory.chat_memory.add_user_message(tstr+user)
    memory.chat_memory.add_ai_message(tstr+system)
    return memory

def load (memory):
    return memory.load_memory_variables({})

def clear (memory):
    memory.clear()

def save (memory, path):
    buffer = memory.load_memory_variables({})
    with open(path, mode = 'a', newline = '\n', encoding = 'UTF-8') as f:
        f.write(buffer['history']+'\n')

def read (path):
    if os.path.isfile (path):
        with open(path, mode = 'r', encoding = 'UTF-8') as f:
            return f.read()
    return ''

def remove(path):
    os.remove(path)