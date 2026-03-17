import streamlit as st
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.parse
import re
import time
import io
from PIL import Image

def linkedin_search(driver, email, password, roles):
    results = []
    screenshots = {}

    # 1. Login Page
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    # Capture Login Screen
    login_png = driver.get_screenshot_as_png()
    screenshots["Login Page"] = Image.open(io.BytesIO(login_png))

    # Login Action
    try:
        driver.find_element(By.ID, "username").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(5)
    except Exception as e:
        st.error(f"Login failed: {e}")
        return results, screenshots

    # 2. Search Query
    query = f'"Hiring" AND "email" AND "{roles}"'
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_query}"

    driver.get(url)
    time.sleep(5)
    
    # Capture Search Results Screen
    search_png = driver.get_screenshot_as_png()
    screenshots["Last Search Page"] = Image.open(io.BytesIO(search_png))

    # 3. Data Extraction
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Target post containers specifically to keep text context relevant
    posts = soup.find_all('div', {'class': 'update-components-text'})
    
    for post in posts:
        post_text = post.get_text(separator=" ").strip()
        # Improved Regex to catch common email patterns
        found_emails = re.findall(r"[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+\.[a-zA-Z]{2,5}", post_text)
        
        for e in found_emails:
            results.append({
                "email": e,
                "context": post_text[:300] + "..." # Snippet of the post
            })

    return results, screenshots

# --- Streamlit UI Display ---
# Assuming you have the driver, email, password, and roles defined:
# data, images = linkedin_search(driver, email, password, roles)

# st.subheader("📸 Browser Screenshots")
# cols = st.columns(len(images))
# for idx, (title, img) in enumerate(images.items()):
#     cols[idx].image(img, caption=title, use_container_width=True)

# st.subheader("📧 Identified Hiring Posts")
# if data:
#     st.table(data)
# else:
#     st.warning("No emails found in the current search results.")

