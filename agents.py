from linkedin_agent import linkedin_search
from coverletter_agent import generate_cover
from email_agent import send_application

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

def run_agents(job_roles, li_email, li_pass, user_email, cv):

    posts = linkedin_search(li_email, li_pass, job_roles)

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


    return results

