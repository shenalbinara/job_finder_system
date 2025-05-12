import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from config import insert_job


def scrape_linkedin(job, location, remote_status):
    # Automatically download and use the correct ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Construct LinkedIn job search URL
    url = f"https://www.linkedin.com/jobs/search?keywords={job}&location={location}"
    driver.get(url)

    time.sleep(5)  # Wait for page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.quit()  # Close the browser after page load

    jobs = soup.find_all('div', class_='base-card')

    for job in jobs:
        try:
            title = job.find('h3').text.strip()
            loc = job.find('span', class_='job-search-card__location').text.strip()
            link = job.find('a')['href']
            contact = "Apply via LinkedIn"

            # Determine if job matches user's remote/physical preference
            is_remote = "Remote" in loc
            if (remote_status == "Remote" and is_remote) or (remote_status == "Physical" and not is_remote):
                insert_job(title, loc, remote_status, contact, link)  # Insert into DB

        except AttributeError:
            continue  # Skip job entries that have missing data

    print("Scraping Completed!")