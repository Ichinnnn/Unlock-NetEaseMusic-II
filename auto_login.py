# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "006653FD15F25F5DC58016D86CCAB20759852967DC2C21E3551A2F2B79EAC53EE203E7E8CFB2270D0EA3128E5B90BD90E3A11EA0DAD67AA973D097E5C608359459BEFBB548BB07C2235F491C5305D8A9A09E2FA51AA8CFD0D1EBABFA4E979FD2B470279C007EEDEF2637877A4031FD0E98FECD0D3F5469D04A03187F9BE3012368AA1AA768AE63EE1AF62C73D750C8D15A40F88DB1D942C2FABA913EEE69C1ED113D51414FD8724D2DC278DDCCBD60E3EBF85F502DAF364E7948897B78EDDBD1AC54CCEF330451EB96157BCAA416F1B8625765BB9A0487A50B78D76857F7465D1634B39CBE4DDAAF08259EC707A2EEA30F1215C2B3460D319E7F0A45F4F313C72372532AFF08A4F093FCF84421B62B0533904365B7A3C999A4393E06C0AD0F194B7A8CE4F961799DA5FBB398E47EBDCF25004BCF58493989A3A7CA982B50F47AA8D243C685C4E77F33D1763630FC2F8F7CB15351DBF497D2CFF85C3DA32E702B2E"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
