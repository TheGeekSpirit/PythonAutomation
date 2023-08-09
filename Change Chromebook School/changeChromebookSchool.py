from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


import time
import csv
import sys
import maskpass


# set Chrome to run in the background
addOptions = webdriver.ChromeOptions()
addOptions.add_argument("--headless")

username = input("Enter username:")
password = maskpass.askpass()

# verifying what school the chromebooks are being moved to
verifyInput = 0
while verifyInput == 0:
    whatSchool = input("What school are you moving the chromebooks to?").upper()
    schoolLetter = whatSchool[0]
    
    # verifying the school is valid
    if schoolLetter == "K" or schoolLetter == "E" or schoolLetter == "M" or schoolLetter == "H" or schoolLetter == "R":
        verifyInput = 1
    else:
        print("""Invalid input. Please enter "k" for K4, "e" for Elementary, "m" for Middle School, "h" for High School, or "r" for Retired. """)
        

fileData = list(csv.reader(open("DeviceSerials.csv")))
serialList = []
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version="114.0.5735.90").install()), options=addOptions)


# loop for each line in the csv and get serial numbers
for data in fileData:
    serialList.append(data[0])

# go to Google Admin
driver.get("https://admin.google.com/ac/chrome/devices/")
driver.implicitly_wait(10)

# enter username and password
driver.find_element(By.ID, "identifierId").send_keys(username)
driver.find_element(By.ID, "identifierNext").click()
driver.implicitly_wait(10)

driver.find_element(By.NAME, "Passwd").send_keys(password)
driver.find_element(By.ID, "passwordNext").click()
time.sleep(5)


# look up each chromebook serial
changedDevices = open("ChangedDevices.txt", "w")
for code in serialList:

    # open menu to change the status of Chromebooks being looked for from "Provisioned" to "All"
    #driver.find_elements(By.CSS_SELECTOR, "span.r44Dm")[0].click()
    driver.find_element(By.CSS_SELECTOR, "span.r44Dm").click()
    time.sleep(2)

    # switch view to all Chromebooks
    driver.find_elements(By.CSS_SELECTOR, "div.SCWude")[0].click()
    time.sleep(2)

    # apply changes
    driver.find_element(By.CSS_SELECTOR, """div[class="U26fgb O0WRkf oG5Srb HQ8yf C0oVfc M9Bg4d"]""").click()
    time.sleep(2)


    # search for chromebook serial
    driver.find_elements(By.CSS_SELECTOR, """input[class="Ax4B8 ZAGvjd"]""")[1].send_keys(code, Keys.ENTER)
    time.sleep(2)

    # select chromebook to change schools
    driver.find_elements(By.CSS_SELECTOR, """div[class="uVccjd"]""")[-1].click()
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, """div[class="uVccjd"]"""[-1]))).click()
    time.sleep(2)

    # select "Move" to move the chromebook
    driver.find_elements(By.CSS_SELECTOR, """div[class="U26fgb O0WRkf oG5Srb HQ8yf C0oVfc LbgMnd M9Bg4d"]""")[3].click()
    time.sleep(2)


    # select K4 chromebooks
    if schoolLetter == "K":
        driver.find_elements(By.CSS_SELECTOR, """input[class="whsOnd zHQkBf"]""")[1].send_keys("K4 Chromebooks")
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, """input[class="whsOnd zHQkBf"]""")[1].send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER, Keys.TAB, Keys.TAB, Keys.ENTER)

    # select Elementary chromebooks
    elif schoolLetter == "E":
        driver.find_elements(By.CSS_SELECTOR, """input[class="whsOnd zHQkBf"]""")[1].send_keys("Elementary Chromebooks")
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, """input[class="whsOnd zHQkBf"]""")[1].send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER, Keys.TAB, Keys.TAB, Keys.ENTER)

    # select Middle School chromebooks
    elif schoolLetter == "M":
        driver.find_elements(By.CSS_SELECTOR, """input[class="whsOnd zHQkBf"]""")[1].send_keys("MS Chromebooks")
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, """input[class="whsOnd zHQkBf"]""")[1].send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER, Keys.TAB, Keys.TAB, Keys.ENTER)

    # select High School chromebooks
    elif schoolLetter == "H":
        driver.find_elements(By.CSS_SELECTOR, """input[class="whsOnd zHQkBf"]""")[1].send_keys("HS Chromebooks")
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, """input[class="whsOnd zHQkBf"]""")[1].send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER, Keys.TAB, Keys.TAB, Keys.ENTER)

    # select Retired chromebooks
    elif schoolLetter == "R":
        driver.find_elements(By.CSS_SELECTOR, """input[class="whsOnd zHQkBf"]""")[1].send_keys("Retired Chromebooks")
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, """input[class="whsOnd zHQkBf"]""")[1].send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER, Keys.TAB, Keys.TAB, Keys.ENTER)

    time.sleep(2)


# try to clear filter, but if the chromebook is already in the selected school, cancel the operationthen clear filter   
    try:
        driver.find_element(By.CSS_SELECTOR, """div[class="U26fgb O0WRkf oG5Srb C0oVfc fAqvFb M9Bg4d"]""").click()
    except ElementClickInterceptedException:
        ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
        time.sleep(2)
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        driver.find_element(By.CSS_SELECTOR, """div[class="U26fgb O0WRkf oG5Srb C0oVfc fAqvFb M9Bg4d"]""").click()

    time.sleep(2)

    # put serial code of moved device into a file in case the process fails partway through the list
    changedDevices.write(str(code) + "\n")

changedDevices.close()
driver.quit()