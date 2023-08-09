from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

import time
import csv
import sys
import maskpass

# set Chrome to run in the background
addOptions = webdriver.ChromeOptions()
addOptions.add_argument("--headless")

username = input("Enter username:")
password = maskpass.askpass()
resourceType = input("Enter device type:")
deviceModel = input("Enter device model:")
#warrantyInfo = input("Enter warranty info and expiration:")

fileData = list(csv.reader(open("DeviceSerials.csv")))
serialList = []
warrantyExpiration = []
warrantyType = []
increment = 0
#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=addOptions)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version="114.0.5735.90").install()), options=addOptions)


# loop for each line in the csv and get serial numbers, warranty expiration date, and warranty coverage
for data in fileData:
    serialList.append(data[0])
    warrantyExpiration.append(data[1])
    warrantyType.append(data[2])

# go to Destiny
driver.get("https://legacycharter.follettdestiny.com/common/welcome.jsp?context=saas112_3902358")
driver.implicitly_wait(10)

driver.find_element(By.LINK_TEXT, "Legacy Early College - Parker").click()
driver.implicitly_wait(10)

# go to login page and enter info
driver.find_element(By.ID, "Login").click()
driver.implicitly_wait(10)

driver.find_element(By.ID, "ID_userLoginName").send_keys(username)
driver.find_element(By.ID, "ID_userLoginPassword").send_keys(password)
driver.find_element(By.NAME, "submit").click()
driver.implicitly_wait(10)

# moving to "Catalog" in top navigation bar
driver.find_element(By.ID, "TopLevelCatalog").click()
driver.implicitly_wait(10)

# moving to "Browse Resources" in resource search
driver.find_element(By.ID, "browseAssets").click()
driver.implicitly_wait(10)


# search for device type in case-insensitive manner
findResource = f"""//*[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{resourceType.lower()}")]"""

# check if device type exists; exit the program if it does not
try:
    resourceElement = driver.find_element(By.XPATH, findResource).send_keys("", Keys.ENTER)
except NoSuchElementException:
    driver.quit()
    print("\n That device type does not exist. \n")
    exit()
driver.implicitly_wait(10)

# search for device model in case-insensitive manner
findModel = f"""//*[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{deviceModel.lower()}")]"""

# check if device model exists; exit the program if it does not
try:
    modelElement = driver.find_element(By.XPATH, findModel).click()
except NoSuchElementException:
    driver.quit()
    print("\n That device model does not exist. \n")
    exit()
driver.implicitly_wait(10)


# add devices to list
completedDevices = open("CompletedDevices.txt", "w")
for code in serialList:

    driver.find_element(By.ID, "AddItem").click()
    driver.implicitly_wait(10)

    driver.find_element(By.CSS_SELECTOR, """input[value="radioUseExplicit"]""").click()
    driver.find_element(By.CSS_SELECTOR, """input[name="copyBarcode"]""").send_keys(code)
    driver.implicitly_wait(10)

    driver.find_element(By.NAME, "UDFIELD_9").send_keys("", Keys.RETURN, "I", Keys.RETURN)
    driver.find_element(By.NAME, "UDFIELD_18").send_keys(str(code))
    driver.find_element(By.ID, "addNote").click()
    driver.implicitly_wait(10)

    driver.find_element(By.NAME, "note").send_keys(f"{warrantyType[increment]} - expires {warrantyExpiration[increment]}")
    driver.find_element(By.ID, "saveNote").click()
    driver.implicitly_wait(10)

    driver.find_element(By.ID, "saveCopy").click()
    driver.implicitly_wait(10)

    completedDevices.write(str(code) + "\n")
    increment += 1

completedDevices.close()

driver.quit()