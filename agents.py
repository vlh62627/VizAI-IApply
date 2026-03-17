import time
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
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    return driver

def run_agents(job_roles, li_email, li_pass, user_email, cv, status_placeholder):
    driver = create_driver()
    
    # 1. Fetch posts and screenshots from LinkedIn
    posts, screenshots = linkedin_search(driver, li_email, li_pass, job_roles)

    final_results = []

    # 2. Process each identified post
    total_posts = len(posts)
    for i, post in enumerate(posts):
        email_to = post.get("Email Address") or post.get("email")
        context_text = post.get("Post Snippet") or post.get("context") or post.get("text")

        if email_to:
            try:
                # Update UI for current progress
                status_placeholder.info(f"Processing {i+1}/{total_posts}: {email_to}")
                
                # Generate cover letter
                cover = generate_cover(context_text)

                # Send application with BCC to user
                send_application(
                    to_email=email_to,
                    user_email=user_email,
                    cover=cover,
                    cv=cv
                )

                final_results.append({
                    "Identified Email": email_to,
                    "Status": "✅ Sent & BCC'd",
                    "Snippet": context_text[:100] + "..."
                })

                # Safety Delay: 10s Countdown between applications
                if i < total_posts - 1:
                    for seconds in range(10, 0, -1):
                        status_placeholder.warning(f"⏳ Cooling down... Next email in {seconds}s")
                        time.sleep(1)

            except Exception as e:
                final_results.append({
                    "Identified Email": email_to,
                    "Status": f"❌ Failed: {str(e)}",
                    "Snippet": context_text[:100] + "..."
                })
        else:
            final_results.append({
                "Identified Email": "N/A",
                "Status": "⚠️ No Email Found",
                "Snippet": context_text[:100] + "..."
            })

    driver.quit()
    return final_results, screenshots
