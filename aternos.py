from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from time import sleep as wait

load_dotenv()
ATERNOS_USER = os.environ["ATERNOS_USERNAME"]
ATERNOS_PASS = os.environ["ATERNOS_PASSWORD"]

def create_driver():
    return uc.Chrome(use_subprocess=True)

def open_server_log(driver:uc.Chrome):
    driver.get("https://aternos.org/log/")

    driver.find_element(By.CLASS_NAME, "username").send_keys(ATERNOS_USER)
    driver.find_element(By.CLASS_NAME, "password").send_keys(ATERNOS_PASS)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/div[4]/button").click()

    #WebDriverWait(driver, 30).until(EC.url_to_be("https://aternos.org/servers/"))
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div[2]/div[2]/div[2]/div[2]/button[1]")))

    driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/div[2]/div[2]/div[2]/button[1]").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/section/div[1]/div/div[3]/div[2]/div/div[1]/div[1]/div[1]/div").click()


def get_log_content(driver:uc.Chrome):
    # Assumes the driver already has the log page opened

    driver.refresh()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/section/div[3]/div[2]/table/tbody")))

    return driver.find_element(By.XPATH, "/html/body/div[3]/main/section/div[3]/div[2]/table/tbody").text
