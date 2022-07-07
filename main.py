'''My python test playground'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import os 
import sys

application_path = os.path.dirname(sys.executable)

# Gets the current time 
now = datetime.now()
# Converts time to string format
# Creating a format that is dd/mmm/yyyy
day_month_year = now.strftime("%d%m%Y")

# Add the link to the website you want to scrape
website = "https://www.thesun.co.uk/"
path = "/Users/timl/Desktop/chromedriver"

options = Options()
options.headless = True

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)

# Get the XPath for the container that holds the information you would like. 
containers = driver.find_elements(by='xpath',value='//div[@class="teaser__copy-container"]/a')

titles = []
subtitles = []
links = []

for container in containers:
    # Going through each individual container extracting each piece of data you 
    # want into their respective lists
    title = container.find_element(by='xpath', value='./h2').text
    subtitle =  container.find_element(by='xpath', value='./p').text
    link =  container.find_element(by='xpath', value='.').get_attribute('href')

    titles.append(title)
    subtitles.append(subtitle) 
    links.append(link)

my_dict= {'title': titles, 'subtitle': subtitles, 'link': links}

# Converts all the lists into columns in an excel spreadsheet.
df_headlines = pd.DataFrame(my_dict)
file_name = f'headline-{day_month_year}.xlsx'
final_path = os.path.join(application_path, file_name)
df_headlines.to_excel(final_path)

driver.quit()
