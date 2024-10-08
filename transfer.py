import keyinp
import time
import math

a = 'あかさたなはまやらわがざだばぱぁゃアカサタナハマヤラワガザダバパァャｱｶｻﾀﾅﾊﾏﾔﾗﾜｶﾞｻﾞﾀﾞﾊﾞﾊﾟｧｬ'
i = 'いきしちにひみりぎじぢびぴぃイキシチニヒミリギジヂビピィｲｷｼﾁﾆﾋﾐﾘｷﾞｼﾞﾁﾞﾋﾞﾋﾟｨ'
u = 'うくすつぬふむゆるぐずづぷぶぅゅっウクスツヌフムユルグズヅブプゥュッｳｸｽﾂﾇﾌﾑﾕﾙｸﾞｽﾞﾂﾞﾌﾞﾌﾟｩｭｯ'
e = 'えけせてねへめれげぜでべぺぇエケセテネヘメレゲゼデベペェｴｹｾﾃﾈﾍﾒﾚｹﾞｾﾞﾃﾞﾍﾞﾍﾟｪ'
o = 'おこそとのほもよろごぞどぽぼぉょオコソトノホモヨロゴゾドボポォョｵｺｿﾄﾉﾎﾓﾖﾛｺﾞｿﾞﾄﾞﾎﾞﾎﾟｫｮ'
n = 'んンﾝ'

talkend = True

def transfer_utterance(utterance):
    list(utterance)
    bkey = 'n'
    talkend = False
    for num in range(len(utterance)):
        utt = utterance[num]
        if utt in a:
#            print('あ')
            key = 'a'
        elif utt in i:
#            print('い')
            key = 'i'
        elif utt in u:
#            print('う')
            key = 'u'
        elif utt in e:
#            print('え')
            key = 'e'
        elif utt in o:
#            print('お')
            key = 'o'
        elif utt in n:
#            print('ん')
            key = 'n'
        else:
            #一つ前の音にする
            key = bkey

        keyinp.send(key)
        time.sleep(0.1)
        bkey = key
    talkend = True

def is_talkend():
    return talkend

def transfer_percentage(per, thresh, motion_num):
    #小数点以下は切り捨て
    base = math.floor((per - thresh) * 100)
    print('level base:', base)
    if base <= 0:
        #0以下(類似度がthreshより小)
        level = 0
    elif base <= 5:
        #5以下(71%〜75％)
        level = 1
    elif base <= 10:
        #10以下(76%〜80％)
        level = 2
    elif base <= 15:
        #15以下(81%〜85％)
        level = 3
    else:
        #15より大(86%〜100%)
        level = base - 12
        #高レベルの補正
        if level > motion_num - 1:
            level = motion_num - 1

    return level

if __name__ == "__main__":
    transfer_utterance('あいうえおーかきくけこん')

