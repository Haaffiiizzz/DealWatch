from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

job = input("What kind of job you want to search: \n")
location = input("Enter the location for the job: \n")

driver = webdriver.Chrome()
link = f"https://ca.indeed.com/jobs?q={job}&l={location}"
driver.get(link)


time.sleep(2)

soup = BeautifulSoup(driver.page_source, 'html.parser')

job_titles = soup.find_all('h2', {'class': 'jobTitle'})

job_locations = soup.find_all('div', {'data-testid': 'text-location'})

print("this is job titles", job_titles)
print("this is job location", job_locations)

for title, location in zip(job_titles, job_locations):
    print(title.text.strip())
    print(location.text.strip())


