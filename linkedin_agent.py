import streamlit as st
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.parse
import re
import time
import io
from PIL import Image

def linkedin_search(driver, email, password, roles):
    """
    Performs LinkedIn content search for hiring posts containing any email address.
    """
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
        user_field = driver.find_element(By.ID, "username")
        user_field.clear()
        user_field.send_keys(email)
        
        pass_field = driver.find_element(By.ID, "password")
        pass_field.clear()
        pass_field.send_keys(password)
        
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(5)
    except Exception as e:
        st.error(f"Login process failed: {e}")
        return results, screenshots

    # 2. Universal Search Query
    # Requirement: "Hiring", a generic "@" to trigger email posts, and the Role
    # Using "@" in quotes forces LinkedIn to prioritize posts with email formatting
    query = f'"Hiring" AND "@" AND "{roles}"'
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_query}"

    driver.get(url)
    time.sleep(5)
    
    # Capture Results Screen
    search_png = driver.get_screenshot_as_png()
    screenshots["Last Search Page"] = Image.open(io.BytesIO(search_png))

    # 3. Data Extraction
    soup = BeautifulSoup(driver.page_source, "html.parser")
    posts = soup.find_all('div', {'class': 'update-components-text'})
    
    seen_emails = set() 

    for post in posts:
        post_text = post.get_text(separator=" ").strip()
        
        # --- UPDATED REGEX: Captures ANY standard email format ---
        # Look for alphanumeric chars, @, domain name, and a 2-6 char TLD
        found_emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}", post_text)
        
        for e in found_emails:
            e_lower = e.lower()
            if e_lower not in seen_emails:
                results.append({
                    "Email Address": e_lower,
                    "Post Snippet": post_text[:300] + "..." 
                })
                seen_emails.add(e_lower)

    return results, screenshots

# --- STREAMLIT UI INTEGRATION ---

st.title("VizAI-IApply Universal Agent")

with st.sidebar:
    st.header("Settings")
    u_email = st.text_input("LinkedIn Email")
    u_pass = st.text_input("LinkedIn Password", type="password")
    target_role = st.text_input("Job Keywords", placeholder="e.g. Principal QA")

if st.button("🚀 Run Universal Email Agent"):
    if not u_email or not u_pass or not target_role:
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Searching for hiring posts..."):
            try:
                # Execution (Assumes 'driver' is initialized in your main logic)
                data, images = linkedin_search(driver, u_email, u_pass, target_role)
                
                # Show Browser Progress
                st.subheader("📸 Execution History")
                cols = st.columns(len(images))
                for idx, (title, img) in enumerate(images.items()):
                    cols[idx].image(img, caption=title)

                # Show Results
                st.subheader("📧 Found Contacts")
                if data:
                    st.dataframe(data, use_container_width=True)
                else:
                    st.info("No email addresses detected. Try broader keywords.")
            
            except Exception as main_e:
                st.error(f"Fatal Error: {main_e}")
