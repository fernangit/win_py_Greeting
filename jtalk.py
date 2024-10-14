#coding: utf-8
import subprocess
from datetime import datetime
import winsound

def jtalk(t):
    open_jtalk=['open_jtalk/open_jtalk.exe']
    mech=['-x','open_jtalk/dic']
    htsvoice=['-m','open_jtalk/voice/mei/mei_happy.htsvoice']
#    htsvoice=['-m','open_jtalk/voice/mei/mei_normal.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)

    #convert text encodeing from utf-8 to shift-jis
    try:
        t = t.replace('～', 'ー')
        c.stdin.write(t.encode('shift-jis'))
        c.stdin.close()
        c.wait()
    except:
        print('encode error')
        
    winsound.PlaySound('open_jtalk.wav',  winsound.SND_FILENAME)

def say_datetime():
    d = datetime.now()
    text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
    jtalk(text)

if __name__ == '__main__':
    say_datetime()
