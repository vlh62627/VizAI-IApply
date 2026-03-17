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
    
    # 1. Scraping identified posts
    posts, screenshots = linkedin_search(driver, li_email, li_pass, job_roles)
    
    final_results = []

    # 2. Iterating through identified posts
    for post in posts:
        email_to = post.get("Email Address") or post.get("email")
        context = post.get("Post Snippet") or post.get("text")

        if email_to:
            # Generate cover letter
            cover_letter = generate_cover(context)
            
            # Send Email
            success = send_application(email_to, user_email, cover_letter, cv)
            
            status = "✅ Sent & BCC'd" if success else "❌ Failed to Send"
            
            final_results.append({
                "Identified Contact": email_to,
                "Action Status": status,
                "Source Post": context[:100] + "..."
            })
        else:
            final_results.append({
                "Identified Contact": "None Found",
                "Action Status": "⚠️ Skipped",
                "Source Post": context[:100] + "..."
            })

    driver.quit()
    return final_results, screenshots
