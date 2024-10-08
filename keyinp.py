import keyboard

#debug
DEBUG = True

def send(key):
    if DEBUG != True:
        keyboard.send(key)
