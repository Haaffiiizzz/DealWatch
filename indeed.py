from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

# job = input("What kind of job you want to search: \n")
# location = input("Enter the location for the job: \n")

# link = f"https://ca.indeed.com/jobs?q={job}&l={location}"

# moreParam = input("Do you want to add more parameters? (Y/N):\n")
# if moreParam.upper() == "Y": 
#     radius = int(input("What radius do you want in KM?: (0, 5, 10, 15, 25, 35, 50, 100) \n").upper())
#     duration = int(input("What duration do you want in days?: {1, 3, 7, 14}\n"))
    
#     link += f"&radius={radius}&fromage={duration}"


link = f"https://ca.indeed.com/jobs?q=server&l=edmonton"

driver = webdriver.Chrome()
driver.get(link)

time.sleep(2)

job = driver.find_element(By.ID, "job_1fb81916d084cfa7")
job.click()

time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')

print(soup)

# sliders = soup.find_all("li", {"class":"css-5lfssm eu4oa1w0"})

# print(sliders.text)

# job_titles = soup.find_all('h2', {'class': 'jobTitle'})
# job_companies = soup.find_all('span', {'data-testid': 'company-name'})
# job_locations = soup.find_all('div', {'data-testid': 'text-location'})


# for title, company, location in zip(job_titles, job_companies, job_locations):
#     print(f"{title.text.strip()} | {company.text.strip()} | {location.text.strip()}")
   


