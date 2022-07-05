'''My python test playground'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd

# Add the link to the website you want to scrape
website = "https://www.thesun.co.uk/"
path = "/Users/timl/Desktop/chromedriver"

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
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
df_headlines.to_excel('spreadsheets/headlines.xlsx', sheet_name='The Sun')

driver.quit()
