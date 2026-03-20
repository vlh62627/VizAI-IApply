import streamlit as st
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.parse
import re
import time
import io
from PIL import Image

def linkedin_login_stage(driver):
    """
    Opens LinkedIn and captures the login page for the user.
    """
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    png = driver.get_screenshot_as_png()
    return Image.open(io.BytesIO(png))

def linkedin_search_stage(driver, roles):
    """
    Performs search AFTER the user has logged in manually.
    """
    results = []
    
    # 1. Build Query
    query = f'"Hiring" AND "@" AND "{roles}"'
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_query}"

    driver.get(url)
    time.sleep(5)
    
    # Capture Results Screenshot
    search_png = driver.get_screenshot_as_png()
    search_img = Image.open(io.BytesIO(search_png))

    # 2. Extract Data
    soup = BeautifulSoup(driver.page_source, "html.parser")
    posts = soup.find_all('div', {'class': 'update-components-text'})
    
    seen_emails = set() 
    for post in posts:
        post_text = post.get_text(separator=" ").strip()
        found_emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}", post_text)
        
        for e in found_emails:
            e_lower = e.lower()
            if e_lower not in seen_emails:
                results.append({
                    "Email Address": e_lower,
                    "Post Snippet": post_text[:300] + "..." 
                })
                seen_emails.add(e_lower)

    return results, search_img

# --- STREAMLIT UI INTEGRATION ---

st.title("✈️ CareerPilot AI: Manual Login Mode")

# Sidebar - No password field
with st.sidebar:
    st.header("Search Settings")
    target_role = st.text_input("Job Keywords", placeholder="e.g. SDET")
    st.info("Note: Login is handled via the browser session for security.")

# Step 1: Initialize and show Login Screen
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    if st.button("Step 1: Open LinkedIn Login"):
        with st.spinner("Opening LinkedIn..."):
            login_snapshot = linkedin_login_stage(driver)
            st.image(login_snapshot, caption="Current Browser View")
            st.warning("⚠️ Please log in to LinkedIn in the browser window that opened. Once you see your feed, click the button below.")
            
    if st.button("Step 2: I have logged in ✅"):
        st.session_state.logged_in = True
        st.rerun()

# Step 2: Run Search
if st.session_state.logged_in:
    if st.button("🚀 Start Search Agent"):
        if not target_role:
            st.error("Please enter Job Keywords in the sidebar.")
        else:
            with st.spinner("Searching hiring posts..."):
                try:
                    data, search_img = linkedin_search_stage(driver, target_role)
                    
                    st.subheader("📸 Search Result View")
                    st.image(search_img)

                    st.subheader("📧 Found Contacts")
                    if data:
                        st.dataframe(data, use_container_width=True)
                    else:
                        st.info("No emails found. Try adjusting your keywords.")
                        
                    # Reset button
                    if st.button("Reset Session"):
                        st.session_state.logged_in = False
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Search failed: {e}")
