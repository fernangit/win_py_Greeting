import keyboard

#debug
DEBUG = False

def send(key):
    if DEBUG != True:
        keyboard.send(key)
