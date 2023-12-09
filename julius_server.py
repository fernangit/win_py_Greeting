# -*- coding: utf-8 -*-
import subprocess
import os

path = os.getcwd()

# 日本語のパスはエラーがでる
julius      = path + "/julius/dictation-kit/bin/windows/julius.exe"
main        = path + "/julius/dictation-kit/main.jconf"
am_dnn      = path + "/julius/dictation-kit/am-dnn.jconf"
julius_dnn  = path + "/julius/dictation-kit/julius.dnnconf"
am_gmm      = path + "/julius/dictation-kit/am-gmm.jconf"

command = julius + ' -C ' + main + ' -C ' + am_gmm + ' -module -charconv utf-8 sjis'
p = subprocess.run(command, shell=True)