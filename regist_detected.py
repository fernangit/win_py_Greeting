import os
import sys
import datetime

def regist_detected(detect_name, path='./date/'):
    #### 日時を取得
    dt_now = datetime.datetime.now()
    print(dt_now)
    today = str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2)
    now_time = str(dt_now.hour).zfill(2) + str(dt_now.minute).zfill(2) + str(dt_now.second).zfill(2)
    print(today, now_time)

    ### 検出名からPIN Numberを取得する
    detect_pin_number = detect_name.split('_')[1]

    path = path + today + '.csv'
    print(path)

    if os.path.isfile(path) == True:
        ### 本日ファイルあり
        with open(path, 'r') as f:
            ### 本日ファイルを検索
            regist = ''
            replace = False
            for text in f.readlines():
                text = text.strip()
                pin_number = text.split(',')[0]
                start_time = text.split(',')[1]
                end_time = text.split(',')[2]
                ### PIN Numberがあれば終了時間のみ更新
                if detect_pin_number == pin_number:
                    changes = pin_number + ',' + start_time + ',' + now_time
                    replace = True
                else:
                    changes = text

                regist = regist + changes + '\n'

        if replace == False:
            ### PIN Numberがなければ行追加して開始・終了時間に現在時間を設定
            regist = regist + detect_pin_number + ',' + now_time + ',' + now_time + '\n'
    else:
        ### 開始・終了時間に現在時間を設定
        regist = detect_pin_number + ',' + now_time + ',' + now_time + '\n'

    ### 本日ファイルを作成
    with open(path, 'w') as f:
        f.write(regist)

if __name__ == '__main__':
    args = sys.argv
    if 1 <= len(args):
        regist_detected(args[1])
    else:
        print('Arguments are too short')
