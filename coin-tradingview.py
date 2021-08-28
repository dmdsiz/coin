# tradingview
import schedule
import requests
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from slacker import Slacker
from time import sleep
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "C:/Users/황길연/Desktop/html/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver, options=chrome_options)
driver.get('https://kr.tradingview.com/chart/?symbol=BINANCE%3AAVAXUSDT')
sleep(15)                                       # 홈페이지가 늦게 열려서 15초 기다림
token = "token"
slack = Slacker(token)

def post_message(token, channel, text):         # 슬랙으로 알람을 보내기 위한 준비
  response = requests.post("https://slack.com/api/chat.postMessage",
      headers={"Authorization": "Bearer "+token},
      data={"channel": channel,"text": text})
  print(response)
myToken = "token"

def job():
  macd = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[3]/td[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div').text
  ma60 = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div').text
  ma120 = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[2]/div').text
  k = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[5]/td[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div').text
  d = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[5]/td[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div').text
  j = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[5]/td[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[3]/div').text
  macd = macd.replace('−','-')                   # 문자열 − 에서 음수를 뜻하는 - 로 치환함
  k = k.replace('−','-')
  d = d.replace('−','-')
  j = j.replace('−','-')
  if float(ma60) < float(ma120):
    if float(macd) < 0:
      if float(j) < float(k) < float(d):
        post_message(myToken,"#5","숏")
        print('숏',datetime.datetime.now(),macd,ma60,ma120,k,d,j)    
  elif float(ma120) < float(ma60):
    if float(macd) >= 0:
      if float(d) < float(k) < float(j):
        post_message(myToken,"#5","롱")
        print('롱',datetime.datetime.now(),macd,ma60,ma120,k,d,j)
schedule.every(10).seconds.do(job)
while True:
  schedule.run_pending()
  time.sleep(1)
