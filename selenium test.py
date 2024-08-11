from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Setup the webdriver (make sure you have downloaded the correct driver for your browser)
driver = webdriver.Chrome()  # You can also use Firefox or another supported browser
driver.get("https://www.indeed.com/q-Data-Scientist-l-New-York,-NY-jobs.html")

# Wait for the page to fully load
time.sleep(5)

# Get the page source and create a BeautifulSoup object
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Now you can proceed with scraping as usual
job_titles = soup.find_all('h2', {'class': 'jobTitle'})

for title in job_titles:
    print(title.text.strip())

# Close the browser
driver.quit()
