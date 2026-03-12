from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.parse
import re
import time


def linkedin_search(driver, email, password, roles):

    results = []

    # Open login page
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    # Login
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(5)

    # Build search query
    query = f"Hiring gmail.com {roles}"
    encoded_query = urllib.parse.quote(query)

    url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_query}"

    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    text = soup.get_text()

    emails = re.findall(r"[A-Za-z0-9._%+-]+@gmail\.com", text)

    for e in set(emails):

        results.append({
            "email": e,
            "text": text[:500]
        })

    return results
