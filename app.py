import streamlit as st
import pandas as pd
from agents import run_agents

try:
    st.title("CareerPilot AI")
    st.write("Loading…")

    # Example: check if Gemini key exists
    import os
    st.write(os.environ["GEMINI_API_KEY"])


st.set_page_config(
page_title="CareerPilot AI",
page_icon="🚀",
layout="wide"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<p class="main-title">CareerPilot AI</p>', unsafe_allow_html=True)

st.write("Your AI assistant that finds jobs and applies automatically.")

st.sidebar.header("User Settings")


job_roles = st.text_input(
"Job Roles (use & to separate)",
"QA Analyst & Automation Tester"
)

user_email = st.text_input("Your Email")

linkedin_email = st.text_input("LinkedIn Email")

linkedin_password = st.text_input(
"LinkedIn Password",
type="password"
)

cv = st.file_uploader(
"Upload CV",
type=["pdf","docx"]
)

if st.button("Start AI Job Agent"):

    results = run_agents(
        job_roles,
        linkedin_email,
        linkedin_password,
        user_email,
        cv
    )

    df = pd.DataFrame(results)

    st.success(f"{len(df)} applications sent!")

    st.dataframe(df)
