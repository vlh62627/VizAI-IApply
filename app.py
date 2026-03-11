import streamlit as st
import os
import pandas as pd

# 1. Page config
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="✈️",
    layout="wide"
)

# 2. Custom CSS – animated gradient, cards, inputs
st.markdown("""
<style>
/* Animated gradient background */
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

body {
    background: linear-gradient(135deg, #2563EB, #FFA500, #FFD700);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}

/* Title */
.title {
    font-size: 90px;
    font-weight: bold;
    color: white;
    text-align: center;
    margin-bottom: 0px;
}

/* Subtitle */
.subtitle {
    font-size: 28px;
    color: white;
    text-align: center;
    margin-bottom: 40px;
}

/* Card container */
.card {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
}

/* Inputs inside card */
.stTextInput>div>div>input, .stFileUploader>div>div>div {
    height: 50px;
    font-size: 18px;
    border-radius: 8px;
    border: 2px solid black; /* Black border */
}

/* Button */
.stButton>button {
    background-color: #FFA500;
    color: white;
    font-size: 22px;
    padding: 14px 40px;
    border-radius: 12px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #FFD700;
    color: #2563EB;
}

/* Center everything */
.css-1aumxhk {
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# 3. Main title
st.markdown('<p class="title">✈️ CareerPilot AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI assistant that finds jobs and applies automatically.</p>', unsafe_allow_html=True)

# 4. Input cards
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

# 6. Apply button in card
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
