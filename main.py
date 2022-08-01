'''My python test playground'''

import time
import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd

application_path = os.path.dirname(sys.executable)

# Gets the current time
now = datetime.now()
# Converts time to string format
# Creating a format that is dd/mmm/yyyy
day_month_year = now.strftime("%d%m%Y")

# Add the link to the website you want to scrape
WEBSITE = "https://www.zomato.com/wellington/wellington-central-restaurants"
PATH = "/Users/timl/Desktop/chromedriver"

options = Options()
# options.headless = True

service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.get(WEBSITE)

time.sleep(2)  # Allow 2 seconds for the web page to open
SCROLL_PAUSE_TIME = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
SCREEN_HEIGHT = driver.execute_script("return window.screen.height;") # get screen height
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script(f'window.scrollTo(0, {SCREEN_HEIGHT}*{i});')
    i += 1
    time.sleep(SCROLL_PAUSE_TIME)
    # update scroll height each time after scrolled,
    # as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")

    # Get the XPath for the container that holds the information you would like.
    containers = driver.find_elements(by='xpath',value='//div[@class="jumbo-tracker"]//a[2]')

    restaurants = []
    links = []
    cuisineTypes = []
    location = []

    for container in containers:
        # Going through each individual container extracting each piece of data you
        # want into their respective lists
        restaurant = container.find_element(by='xpath', value='./div/h4').text
        link =  container.find_element(by='xpath', value='.').get_attribute('href')
        cuisine =  container.find_element(by='xpath', value='./div[2]/p').text

        restaurants.append(restaurant)
        links.append(link)
        cuisineTypes.append(cuisine)
        location.append('Wellington')

    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (SCREEN_HEIGHT) * i > scroll_height:
        break


my_dict= {'Restaurant': restaurants, 'Link': links, 'Cuisine': cuisineTypes, 'Location': location}

# Converts all the lists into columns in an excel spreadsheet.
df_headlines = pd.DataFrame(my_dict)
FILE_NAME = 'wellington-restaurants.xlsx'

final_path = os.path.join(application_path, FILE_NAME)
df_headlines.to_excel(final_path)

# Local Path
df_headlines.to_excel('report_generation/xl_spreadsheets/' + FILE_NAME)

driver.quit()
