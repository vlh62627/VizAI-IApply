import streamlit as st
import os
import pandas as pd

# 1. Page config
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="✈️",
    layout="wide"
)

# 2. Custom CSS for background, title, inputs, button
st.markdown(
    """
    <style>
    /* Full page background gradient */
    body {
        background: linear-gradient(135deg, #2563EB, #FFA500, #FFD700);
        background-attachment: fixed;
    }

    /* Title */
    .title {
        font-size: 80px;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 0px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 26px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
    }

    /* Input fields */
    .stTextInput>div>div>input {
        height: 50px;
        font-size: 18px;
        border-radius: 8px;
        border: 2px solid black; /* Black border */
    }

    /* File uploader */
    .stFileUploader>div>div>div {
        border: 2px solid black;
        border-radius: 8px;
    }

    /* Button */
    .stButton>button {
        background-color: #FFA500;
        color: white;
        font-size: 22px;
        padding: 14px 40px;
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FFD700; /* Gold hover */
        color: #2563EB;
    }

    /* Center all inputs and button */
    .css-1aumxhk {
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Main Title
st.markdown('<p class="title">✈️ CareerPilot AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI assistant that finds jobs and applies automatically.</p>', unsafe_allow_html=True)

# 4. Inputs on main page (no sidebar)
st.write("### Enter your details:")

job_roles = st.text_input("Job Roles (use & to separate)")
user_email = st.text_input("Your Email")
linkedin_email = st.text_input("LinkedIn Email")
linkedin_password = st.text_input("LinkedIn Password", type="password")
cv = st.file_uploader("Upload CV", type=["pdf", "docx"])

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
