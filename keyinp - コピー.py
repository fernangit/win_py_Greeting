from pynput.keyboard import Key, Listener

inpkey = '????'

def print_something():
    print('hi tohu!')

def on_press(key):
    #この関数が呼ばれているかどうかチェックするための処理
    print_something()

    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        inpkey = key.char
        print('key:', inpkey)
        # Stop listener
        return False
    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):
    print('{0} released'.format(key))

    if key == Key.esc:
        # Stop listener
        return False

if __name__ == '__main__':

    with Listener(
        on_press = on_press,
        on_release= on_release
    ) as listener:
        listener.join()
    print('key:', inpkey)
    print('end')
