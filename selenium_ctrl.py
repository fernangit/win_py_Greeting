# -*- coding: utf-8 -*-
from selenium import webdriver 
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from msedge.selenium_tools import Edge, EdgeOptions

import os

path = os.getcwd()
service = Service(executable_path=path + "/msedgedriver.exe")
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
