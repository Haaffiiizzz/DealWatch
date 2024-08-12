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

job_companies = soup.find_all('span', {'data-testid': 'company-name'})

job_locations = soup.find_all('div', {'data-testid': 'text-location'})


for title, company, location in zip(job_titles, job_companies, job_locations):
    print(f"{title.text.strip()} | {company.text.strip()} | {location.text.strip()}")
   


