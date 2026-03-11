import streamlit as st
import os
import pandas as pd

# 1. Page config must be first
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

# 2. Load CSS safely
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("style.css not found")

st.markdown('<div class="math-header">✈️CareerPilot AI</p>', unsafe_allow_html=True)

# 3. Test API key safely
gemini_key = os.environ.get("GEMINI_API_KEY")

st.write("Your AI assistant that finds jobs and applies automatically.")

# 4. Sidebar inputs
st.sidebar.header("User Settings")

job_roles = st.text_input("Job Roles (use & to separate)")
user_email = st.text_input("Your Email")
linkedin_email = st.text_input("LinkedIn Email")
linkedin_password = st.text_input("LinkedIn Password", type="password")
cv = st.file_uploader("Upload CV", type=["pdf","docx"])

# 5. Import agents safely
try:
    from agents import run_agents
except Exception as e:
    st.error(f"Agents import failed: {e}")
    run_agents = None

# 6. Button click
if st.button("Start AI Job Agent"):
    if run_agents:
        try:
            results = run_agents(job_roles, linkedin_email, linkedin_password, user_email, cv)
            df = pd.DataFrame(results)
            st.success(f"{len(df)} applications sent!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error during job agent run: {e}")
    else:
        st.error("Cannot run agents due to import error")
