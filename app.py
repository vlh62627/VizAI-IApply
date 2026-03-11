import streamlit as st
import os
import pandas as pd

# 1. Page config
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="✈️",
    layout="wide"
)

# 2. Custom CSS – solid blue background, card style, black borders
st.markdown("""
<style>
/* Full page background solid blue */
[data-testid="stAppViewContainer"] {
    background-color: #2563EB;  /* Primary Blue */
    color: white;
}

/* Card container for inputs */
.card {
    background-color: #FFFFFF;  /* White card for inputs */
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
    color: black;
}

/* Text input inside card */
.stTextInput>div>div>input, .stFileUploader>div>div>div {
    height: 50px;
    font-size: 18px;
    border-radius: 8px;
    # border: 2px solid black; /* Black border */
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
    background-color: #FFD700; /* Gold hover */
    color: #2563EB;
}

/* Center all inputs */
.css-1aumxhk {
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# 3. Main title and subtitle using HTML for proper size
st.markdown('<h1 style="text-align:center; font-size:50px; color:white; margin-bottom:10px;">✈️ CareerPilot AI</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:center; font-size:28px; color:white; margin-bottom:40px;">Your AI assistant that finds jobs and applies automatically</h3>', unsafe_allow_html=True)

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
