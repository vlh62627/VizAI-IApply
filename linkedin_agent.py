from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time

def linkedin_search(email, password, roles):

    driver = webdriver.Chrome()

    driver.get("https://www.linkedin.com/login")

    driver.find_element("id","username").send_keys(email)
    driver.find_element("id","password").send_keys(password)
    driver.find_element("xpath",'//button[@type="submit"]').click()

    time.sleep(5)

    query = f"Hiring gmail.com {roles}"

    url = f"https://www.linkedin.com/search/results/content/?keywords={query}"

    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source,"html.parser")

    text = soup.get_text()

    emails = re.findall(r"[A-Za-z0-9._%+-]+@gmail.com",text)

    results = []

    for e in emails:

        results.append({
            "email": e,
            "text": text[:500]
        })

    driver.quit()

    return results