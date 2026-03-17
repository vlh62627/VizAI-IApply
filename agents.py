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
    # Adding a realistic user agent can help prevent LinkedIn blocks
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    return driver

def run_agents(job_roles, li_email, li_pass, user_email, cv):
    driver = create_driver()
    
    # FIX: Unpack both the results list and the screenshots dictionary
    # This ensures 'posts' is strictly the list of dictionaries
    posts, screenshots = linkedin_search(driver, li_email, li_pass, job_roles)

    results = []

    # Now 'posts' is a list, so 'post' is a dictionary
    for post in posts:
        # Match these keys to what linkedin_search actually returns:
        # In the previous update, we used "Email Address" and "Post Snippet"
        # I have adjusted them here to be safe:
        email = post.get("Email Address") or post.get("email")
        text = post.get("Post Snippet") or post.get("context") or post.get("text")

        if email:
            try:
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
            except Exception as e:
                results.append({
                    "Recruiter Email": email,
                    "Status": f"Failed: {str(e)}"
                })

    driver.quit()
    
    # Return both the results and the screenshots so the UI can still show them
    return results, screenshots
