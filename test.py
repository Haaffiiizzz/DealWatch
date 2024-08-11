import requests
from bs4 import BeautifulSoup

# Set up the search parameters
job_title = "data scientist"
location = "new york"

# Create the URL based on search parameters
url = f"https://www.indeed.com/jobs?q={job_title}&l={location}"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Print the HTML to see if the structure matches what the script expects
print(soup.prettify())
