import os
import random
import json
from datetime import datetime, timedelta, time
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyautogui
import time

# Directory containing images
image_directory = r'C:\Users\ahmed\Programming Valey\Content\Images'

# Load JSON data
with open('scheduled_posts.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

chrome_user_data_dir = r'C:\Users\ahmed\AppData\Local\Google\Chrome\User Data'
chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={chrome_user_data_dir}")
chrome_options.add_argument(f"profile-directory=Default")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--ignore-certificate-errors")

chromedriver_path = r'C:\\Program Files (x86)\\chromedriver.exe'
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def UploadImage(image_path):
    upload_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/section/div[2]/ul/li[1]/div/div/span/button')))
    upload_button.click()
    time.sleep(2)
    pyautogui.write(image_path)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(4)
    confirm_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div/div[2]/div/button[2]')))
    confirm_button.click()
    

def NavigateWindow():
    driver.get("https://www.linkedin.com/company/90214971/admin/page-posts/published/?share=true")
    time.sleep(3)  

def writeDescription(title, description, recommended_courses, hashtags):
    container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div[1]')))
    container.click()
    time.sleep(0.5)
    
    full_text = title + "\n\n" + description + "\n\n"
    for course in recommended_courses:
        full_text += course['title'] + "\n" + course['link'] + "\n"
    full_text += "\n"
    for hashtag in hashtags:
        full_text += hashtag + " "
    driver.execute_script("arguments[0].innerText = arguments[1];", container, full_text)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", container)
    time.sleep(0.5)

def schedulePost(Pdate, Ptime):
    schedule_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[1]/span/div[1]/button')))
    schedule_button.click()
    time.sleep(0.5)
    date_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[1]/form/div[1]/div[1]/div/input')))
    date_input.click()
    date_input.send_keys(Keys.CONTROL, 'a')
    date_input.send_keys(Keys.BACKSPACE)
    time.sleep(0.5)
    date_input.send_keys(Pdate)
    time.sleep(1)
    date_input.click()

    time_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/div/input')))
    time_input.click()
    time_input.send_keys(Keys.CONTROL, 'a')
    time_input.send_keys(Keys.BACKSPACE)
    time.sleep(0.5)
    time_input.send_keys(Ptime)
    time.sleep(1)
    time_input.send_keys(Keys.TAB)
    time.sleep(0.5)

    next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[2]/div/button[2]')))
    next_button.click()

def pressSchedule():
    schedule_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[2]/button')))
    schedule_button.click()

def schedulePosts():
    for post in data:
        success = False
        while not success:
            try:
                NavigateWindow()
                UploadImage(post["Image Path"])
                time.sleep(1)
                writeDescription(post['Title'], post['Description'], post['Recommended Courses'], post['Hashtags'])
                time.sleep(2)
                schedulePost(post['Date'], post['Time'])
                time.sleep(1)
                pressSchedule()
                time.sleep(5)
                success = True
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Retrying...")
                time.sleep(5)

schedulePosts()
