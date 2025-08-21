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
    browser.add_cookie({"name": "MUSIC_U", "value": "00700D7554A4EF39587626B21DD8ED070814F0CF6C09626179F43B4ADF0490BAB69EDEE3DB690E3B93BCD898409891E4870AD69A9E1FE6B3D6F789CFF91433924D7E6377F8E0E4D51B3E5593D85007B1B78E162C02AD0F8F0AC4F79B789413E90B1CE0DAD7D151F0F6C45C4CA5B59678280BF9D8A1C0E2728DDBD591E18F52ABC306066FB327233F8C46A9EAAFED45C8AC9DE4CD94AF3E3DDA2EEE21FCB07E363488CC8D12C785A5C816634DAF7BD0E842B58F13934C50DF32C0D791E97F80291CD4F4A2F5E85D990C7F843302BAC7F43C51DAFB631A4A4097C5FC95106EA2CE129F576605A42591050718405FC51DAC67FD9C35FDBCFE4992CCACA0D9A42A0244C84AD8789CE659CE5391BF9CAE253BC3FEC350450D1FDA909FE722F5C5439F7AD24285A46101A091FC8E634A3EBF38454ABFA7822F6E9578924566B5971B2AEE4D544B2DCEFFA41007A6902B6A76DFDEA21AD19D69C976C77DD15AA22EF6B1ADBDE24994A5C488FAA1ACF83012A5F38257528F95510ED0E7E17E5ED5C354CE7ED70B3DCAD7ACAE2BF69FE21B5C18D609"})
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
