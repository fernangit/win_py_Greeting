from pynput import keyboard
import time

class MonKeyBoard:
    def __init__(self):
        self.inputkey = '???'
    def on_press(self,key):
        try:
            print('press: {}'.format(key.char))
            print('key.char', key.char)
            self.inputkey = key.char
            self.listener.stop()
            self.listener = None
        except AttributeError:
            print('spkey press: {}'.format(key))
    
    def on_release(self,key):
        print('release: {}'.format(key))
        print('key', key)
        self.inputkey = key
        self.listener.stop()
        self.listener = None
            
    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener.start()
        
    def getstatus(self):
        if(self.listener == None):
            print('inputkey:', self.inputkey)
            return False, self.inputkey
        return True, self.inputkey
        
def keyin():
    monitor = MonKeyBoard()
    monitor.start()
    while(True):
        status, inputkey = monitor.getstatus()
        if(status == False):
            print("break")
            break

    return inputkey

def keythrough(wait):
    monitor = MonKeyBoard()
    monitor.start()
    time.sleep(wait)
    status, inputkey = monitor.getstatus()

    return inputkey

if __name__ == '__main__':
#    ret = keyin()
    ret = keythrough(1)
    print('keyin:', ret)
