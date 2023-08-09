from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

import time
import csv
import os
import sys
import maskpass

# set Chrome to run in the background
addOptions = webdriver.ChromeOptions()
addOptions.add_argument("--headless")

username = input("Enter username:")
password = maskpass.askpass()
directory = "G:\My Drive\Parent Folder\Project Folder"
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version="114.0.5735.90").install()), options=addOptions)

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

completedDevices = open("AssignedCarts.txt", "w")

# going through every file in 
for file in os.listdir(directory):
        filePath = os.path.join(directory, file)
        fileData = csv.reader(open(filePath))
        roomNum = f"PARKER {file[:3]}"


        # move to "Update Resources"
        driver.find_element(By.ID, "Update Resources").click()
        driver.implicitly_wait(10)

        # move to "Batch Update"
        driver.find_element(By.ID, "batchUpdate").click()
        driver.implicitly_wait(10)


        # assigning room number
        driver.find_element(By.NAME, "changeLocation").click()
        location = Select(driver.find_element(By.ID, "location"))
        location.select_by_visible_text(roomNum)
        driver.find_element(By.ID, "buttonNext").click()
        driver.implicitly_wait(10)

        # upload file of barcodes
        driver.find_element(By.XPATH, """//input[@type="file"]""").send_keys(filePath)
        driver.find_element(By.ID, "updateButton").click()
        driver.implicitly_wait(10)

        # show finished rooms
        
        completedDevices.write(f"{file} \n")

driver.quit()
