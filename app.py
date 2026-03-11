import streamlit as st
import os
import pandas as pd

# 1. Page config
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="✈️",
    layout="wide"
)

# 2. Custom CSS – elegant background, card style, black borders and labels
st.markdown("""
<style>
/* Make input labels solid black */
.stTextInput>div>label {
    color: black !important;
    font-weight: bold;
}

/* Remove white background for the "Enter your details:" card */
.card:first-of-type {
    background-color: transparent !important;
    box-shadow: none !important;
    padding: 0px !important;
    margin-bottom: 0px !important;
}

/* Remove white background for the button card */
.card:last-of-type {
    background-color: transparent !important;
    box-shadow: none !important;
    padding: 0px !important;
    margin-bottom: 0px !important;
}
</style>
""", unsafe_allow_html=True)

# 3. Main title and subtitle using HTML
st.markdown('<h1 style="text-align:left; font-size:40px; color:white; margin-bottom:10px;">✈️ CareerPilot AI</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:left; font-size:20px; color:white; margin-bottom:20px;">Your AI assistant that finds jobs and applies automatically</h3>', unsafe_allow_html=True)

# 4. Inputs on main page inside a card
st.markdown('<div class="card">', unsafe_allow_html=True)
st.write("### Enter your details:")
job_roles = st.text_input("Job Roles (use & to separate)")
user_email = st.text_input("Your Email")
linkedin_email = st.text_input("LinkedIn Email")
linkedin_password = st.text_input("LinkedIn Password", type="password")
cv = st.file_uploader("Upload CV", type=["pdf", "docx"])
st.markdown('</div>', unsafe_allow_html=True)

# 5. Import agents safely
try:
    from agents import run_agents
except Exception as e:
    st.error(f"Agents import failed: {e}")
    run_agents = None

# 6. Apply button inside card
st.markdown('<div class="card">', unsafe_allow_html=True)
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
st.markdown('</div>', unsafe_allow_html=True)
