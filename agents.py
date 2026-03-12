from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from linkedin_agent import linkedin_search
from coverletter_agent import generate_cover
from email_agent import send_application


def create_driver():

    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    return driver


def run_agents(job_roles, li_email, li_pass, user_email, cv):

    driver = create_driver()

    posts = linkedin_search(driver, li_email, li_pass, job_roles)

    results = []

    for post in posts:

        email = post["email"]
        text = post["text"]

        cover = generate_cover(text)

        send_application(
            email,
            user_email,
            cover,
            cv
        )

        results.append({
            "Recruiter Email": email,
            "Status": "Sent"
        })

    driver.quit()

    return results
