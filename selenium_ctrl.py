# -*- coding: utf-8 -*-
from selenium import webdriver 
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os

path = os.getcwd()
#「Microsoft Edgeは自動テストソフトウェアによって制御されています」を消す
# installed selenium-4.15.2
# service = Service(executable_path=path + "/msedgedriver.exe")
# 最新ドライバーを自動インストール
service = Service(EdgeChromiumDriverManager().install())
options = Options()
options.use_chromium = True
options.add_experimental_option("excludeSwitches", ['enable-automation'])

# Initialize Edge WebDriver
driver = webdriver.Edge(service=service, options=options)

# ブラウザを起動
def open_browser(url):
    driver.get(url)

# ブラウザを終了
def close_browser():
    driver.quit()
