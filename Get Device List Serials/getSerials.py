from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import time
import csv
import sys
import maskpass

# check for output file name as command line argument
try:
    outputFile = sys.argv[1]
except (IndexError) as e:
    print( "\n" + """Enter info in the following format when running the file, replacing the info in the brackets with your filenames: "python getSerials.py" [outputFileName] """ + "\n")
    exit()

username = input("Enter username:")
password = maskpass.askpass()
resourceType = input("Enter device type:")
deviceModel = input("Enter device model:")

driver = webdriver.Chrome(executable_path = "G:\Shared drives\Parent Folder\Project Folder\chromedriver")


# go to Inventory Management System
driver.get("inventory_management_system_link_here")
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

# go to full list of items
driver.find_element(By.LINK_TEXT, "Items").click()
driver.implicitly_wait(15)


# get source code of device page
devicePage = driver.page_source

# create beautifulsoup object
soupPage = BeautifulSoup(devicePage, "html.parser")

# find all td elements
tdElements = soupPage.find_all('td', class_='ColRow')
textList = []
serialList = []

# go through all td elements and extract text from the td elements with <a name="anchorToGo"> in them
for td in tdElements:
    aElement = td.find('a', attrs={'name': lambda value: value and 'anchorToGo' in value})
    if aElement:
        text = aElement.find_next_sibling('br').next_sibling.strip()
        textList.append(text)

for code in textList:
    code = code.replace("(", "")
    code = code.replace(")", "")
    serialList.append(code)

# put each serial code into .csv file
with open(outputFile, mode="w") as csvFile:
    for serial in serialList:
        csvFile.write(serial + "\n")


driver.quit()