import os
import json
from datetime import datetime, time as dtime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as t
import schedule

# Configurations
chrome_user_data_dir = r'C:\Users\ahmed\AppData\Local\Google\Chrome\User Data'
chromedriver_path = r'C:\\Program Files (x86)\\chromedriver.exe'
json_file = 'repost_state.json'

# Initial Setup
chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={chrome_user_data_dir}")
chrome_options.add_argument(f"profile-directory=Default")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--ignore-certificate-errors")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load or Initialize State
if not os.path.exists(json_file):
    state = {
        "number_of_reposts": 0,
        "last_group": 0,
        "number_of_groups": 10  # Default number of groups to share in
    }
    with open(json_file, 'w') as file:
        json.dump(state, file)
else:
    with open(json_file, 'r') as file:
        state = json.load(file)

def save_state():
    with open(json_file, 'w') as file:
        json.dump(state, file)

def navigateWindow():
    driver.get("https://www.linkedin.com/company/programmingvalley/?viewAsMember=true")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

def repost():
    navigateWindow()
    
    second_post = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-carousel__item:nth-of-type(2)"))
    )
    
    repost_button = second_post.find_element(By.CSS_SELECTOR, "button.artdeco-button.social-reshare-button")
    repost_button.click()
    
    select_groups = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.share-unified-settings-entry-button"))
    )
    select_groups.click()
    
    group_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sharing-shared-generic-list__item-button#CONTAINER[role='radio']"))
    )
    group_button.click()
    
    groups_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sharing-shared-generic-list"))
    )
    
    group_buttons = groups_list.find_elements(By.CSS_SELECTOR, "button.sharing-shared-generic-list__item-button")
    
    group_index = state['last_group'] % state['number_of_groups']
    if group_buttons:
        if group_index < len(group_buttons):
            selected_group_button = group_buttons[group_index]
            selected_group_button.click()
        else:
            print("No more groups to share with.")
            return
    else:
        print("No groups found or unable to locate group buttons.")
        return  # Exit the function if no groups are found

    # Locate and click the "Save" button
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.share-box-footer__primary-btn.artdeco-button--primary"))
    )
    save_button.click()

    # Wait for 1.5 seconds
    t.sleep(1.5)

    # Locate and click the "Done" button
    done_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.share-box-footer__primary-btn.artdeco-button--primary"))
    )
    done_button.click()
    t.sleep(1)

    post_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".share-actions__primary-action.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view"))
    )
    post_button.click()
    
    print("Post has been reposted to the selected group.")
    
    # Update state
    state['number_of_reposts'] += 1
    state['last_group'] = (state['last_group'] + 1) % state['number_of_groups']
    save_state()
    
    t.sleep(5)
    driver.quit()

def should_run_now():
    now = datetime.now().time()
    start_time = dtime(20, 0)  # 12:02 PM
    end_time = dtime(21, 0)    # 11:02 PM
    return start_time <= now <= end_time

# Schedule the repost function
def scheduled_repost():
    if should_run_now():
        repost()

schedule.every().hour.at(":18").do(scheduled_repost)

# Main Loop
while True:
    schedule.run_pending()
    t.sleep(60)  # Check every minute
