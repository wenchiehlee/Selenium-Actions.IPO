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

chromedriver_autoinstaller.install()

downloadDir = os.path.abspath(".") + os.sep
preferences = {
    "download.default_directory": downloadDir,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options = webdriver.ChromeOptions()  
chrome_options.add_experimental_option("prefs", preferences)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--window-size=1200,1200")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)
try:
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": downloadDir
    })
except Exception as e:
    print(f"CDP setDownloadBehavior warning: {e}")

def wait_for_download(before_set, target_default, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        time.sleep(1)
        after_set = set(os.listdir(downloadDir))
        new_files = [f for f in (after_set - before_set) if not f.endswith('.crdownload') and not f.endswith('.tmp')]
        if new_files:
            return new_files[0]
    csvs = [f for f in os.listdir(downloadDir) if f.endswith('.csv')]
    if csvs:
        csvs.sort(key=lambda x: os.path.getmtime(os.path.join(downloadDir, x)), reverse=True)
        return csvs[0]
    return target_default

# 1. TPEX
print("Visiting TPEX...")
driver.get("https://www.tpex.org.tw/zh-tw/mainboard/applying/status/company.html")
wait = WebDriverWait(driver, 15)
download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-format='csv-u8']")))
before_files = set(os.listdir(downloadDir))
driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
ActionChains(driver).move_to_element(download_button).click(download_button).perform()

DownloadedFilename = wait_for_download(before_files, "TPEX-IPO-utf8.csv")
print(f"TPEX DownloadedFilename: {DownloadedFilename}")
if DownloadedFilename and DownloadedFilename != "TPEX-IPO-utf8.csv":
    shutil.copy(DownloadedFilename, "TPEX-IPO-utf8.csv")
    print(f"File '{DownloadedFilename}' copied to 'TPEX-IPO-utf8.csv'.")
    if os.path.exists(DownloadedFilename) and DownloadedFilename != "TPEX-IPO-utf8.csv":
        try:
            os.remove(DownloadedFilename)
        except Exception:
            pass

# 2. TWSE
print("Visiting TWSE...")
driver.get("https://www.twse.com.tw/zh/listed/listed/apply-listing.html")
wait = WebDriverWait(driver, 15)
download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='csv']")))
before_files = set(os.listdir(downloadDir))
driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
ActionChains(driver).move_to_element(download_button).click(download_button).perform()

DownloadedFilename = wait_for_download(before_files, "applylisting.csv")
print(f"TWSE DownloadedFilename: {DownloadedFilename}")
if DownloadedFilename and DownloadedFilename != "applylisting.csv":
    shutil.copy(DownloadedFilename, "applylisting.csv")
    print(f"File '{DownloadedFilename}' copied to 'applylisting.csv'.")
    if os.path.exists(DownloadedFilename) and DownloadedFilename != "applylisting.csv":
        try:
            os.remove(DownloadedFilename)
        except Exception:
            pass

driver.quit()
