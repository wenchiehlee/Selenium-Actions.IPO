from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

from pathlib import Path
import pandas as pd
import time
import os
from os.path import exists
import shutil
import csv

# The following 3 lines are for ubuntu only. If windows, please comments then to work well..
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path


def getDownLoadedFileNameClose():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
def getDownLoadedFileName():
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get('chrome://downloads')
    #driver.get_screenshot_as_file("page.png")
    return driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
 
  
downloadDir = f"{os.getcwd()}//"
preferences = {"download.default_directory": downloadDir,
                "download.prompt_for_download": False,
                "directory_upgrade": True,
                "safebrowsing.enabled": True}
chrome_options = webdriver.ChromeOptions()  

chrome_options.add_experimental_option("prefs", preferences)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--window-size=1200,1200")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--no-sandbox")

    
driver = webdriver.Chrome(options = chrome_options)

#driver.get('http://github.com')
#print(driver.title)
#with open('./GitHub_Action_Results.txt', 'w') as f:
#    f.write(f"This was written with a GitHub action {driver.title}")

# 打開目標網頁
driver.get("https://www.tpex.org.tw/zh-tw/mainboard/applying/status/company.html")

# 等待按鈕加載並按 data-format 屬性為 csv-u8 定位按鈕
wait = WebDriverWait(driver, 10)  # 等待按鈕的時間
download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-format='csv-u8']")))

# 滾動到按鈕並點擊
driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
ActionChains(driver).move_to_element(download_button).click(download_button).perform()


# 等待下載完成
time.sleep(2)  # 視下載速度調整時間
print("CSV 文件下載完成！")

            
#driver.get_screenshot_as_file("page.png")
latestDownloadedFileName = getDownLoadedFileName() 
time.sleep(2)
#driver.get_screenshot_as_file("page1.png")
getDownLoadedFileNameClose()
DownloadedFilename=''.join(latestDownloadedFileName).encode().decode("utf-8")

if DownloadedFilename != "TPEX-IPO-utf8.csv":
    # Copy the file to "OTC.csv"
    shutil.copy(DownloadedFilename, "TPEX-IPO-utf8.csv")
    print(f"File '{DownloadedFilename}' copied to 'TPEX-IPO-utf8.csv'.")
    print("Download completed...",downloadDir+'TPEX-IPO-utf8.csv')
    # 移除原始檔案
    os.remove(DownloadedFilename)
