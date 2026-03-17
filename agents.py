import streamlit as st
import os
import pandas as pd
import time

# 1. Page config
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="✈️",
    layout="wide"
)

# 2. Custom CSS
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #1E40AF; color: white; }
.stTextInput>div>label { color: white !important; font-weight: bold !important; font-size: 20px !important; }
.divider { border-bottom: 2px solid #FFD700; margin: 0px 0px 5px 0px; }
.section { margin-top: 10px; margin-bottom: 10px; }
.stButton>button { 
    background-color: #FFA500; color: black; font-size: 22px; 
    padding: 14px 40px; border-radius: 12px; font-weight: bold; width: 100%;
}
.stButton>button:hover { background-color: #FFD700; color: #1E40AF; }
</style>
""", unsafe_allow_html=True)

# 3. Titles
st.markdown('<h1 style="color:white; margin-bottom:0px;">✈️ CareerPilot AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:white; font-size:20px;">AI Job Agent: Search, Personalize, Apply</p>', unsafe_allow_html=True)

# 4. Inputs
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.write("### Enter your details:")
job_roles = st.text_input("Job Roles (e.g. QA Engineer & SDET)")
user_email = st.text_input("Your Email (For BCC and Sending)")
linkedin_email = st.text_input("LinkedIn Login Email")
linkedin_password = st.text_input("LinkedIn Password", type="password")
cv = st.file_uploader("Upload CV", type=["pdf", "docx"])

# 5. Import and Run
try:
    from agents import run_agents
except Exception as e:
    st.error(f"Agents import failed: {e}")
    run_agents = None

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if st.button("Start AI Job Agent"):
    if not (job_roles and user_email and linkedin_email and linkedin_password and cv):
        st.warning("All fields and CV are required.")
    elif run_agents:
        try:
            # Create a placeholder for the live countdown
            status_container = st.empty()
            
            # Start Agent
            with st.spinner("Agent Initializing..."):
                results, screenshots = run_agents(
                    job_roles, linkedin_email, linkedin_password, user_email, cv, status_container
                )
            
            status_container.success("🎯 Job Agent Run Complete!")

            # Display Screenshots
            st.subheader("📸 Activity Log")
            cols = st.columns(len(screenshots))
            for idx, (title, img) in enumerate(screenshots.items()):
                cols[idx].image(img, caption=title)

            # Display Results Table
            st.subheader("📊 Identification & Transmission Report")
            df = pd.DataFrame(results)
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No relevant posts found in this search.")

        except Exception as e:
            st.error(f"Agent Execution Error: {e}")
