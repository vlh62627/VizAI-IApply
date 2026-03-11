import streamlit as st
import os
import pandas as pd

# 1. Page config
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="✈️",
    layout="wide"
)

# 2. Custom CSS – remove spacing, increase label font size, bold
st.markdown("""
<style>
/* Input labels - match "Enter your details" color (white), bold, bigger font */
.stTextInput>div>label {
    color: white !important;  /* Match heading color */
    font-weight: bold !important;
    font-size: 20px !important;  /* +2 font size */
}

/* Remove white background for cards */
.card {
    background-color: transparent !important;
    box-shadow: none !important;
    padding: 0px !important;
    margin-bottom: 0px !important;
}

/* Subtle gold divider */
.divider {
    border-bottom: 2px solid #FFD700; /* Gold divider */
    margin: 0px 0px 5px 0px; /* minimal space below line */
}

/* Section spacing tightened */
.section {
    margin-top: 10px;
    margin-bottom: 10px;
}

/* Button */
.stButton>button {
    background-color: #FFA500;
    color: black;
    font-size: 22px;
    padding: 14px 40px;
    border-radius: 12px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #FFD700; /* Gold hover */
    color: #1E40AF;
}

/* Center all inputs */
.css-1aumxhk {
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# 3. Main title and subtitle
st.markdown('<h1 style="text-align:left; font-size:50px; color:white; margin-bottom:10px;">✈️ CareerPilot AI</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:left; font-size:22px; color:white; margin-bottom:20px;">Your AI assistant that finds jobs and applies automatically</h3>', unsafe_allow_html=True)

# 4. Inputs section with tight divider
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
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

# 6. Apply button section with tight divider
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
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
