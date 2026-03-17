import streamlit as st
import os
import pandas as pd
import time  # 1. Import time for the delay

# 1. Page config
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="✈️",
    layout="wide"
)

# 2. Custom CSS (Kept exactly as provided)
st.markdown("""
<style>
/* Full page background elegant blue */
[data-testid="stAppViewContainer"] {
    background-color: #1E40AF;  /* Elegant deep blue */
    color: black;
}
.stTextInput>div>label {
    color: white !important;  
    font-weight: bold !important;
    font-size: 20px !important;  
}
.card {
    background-color: transparent !important;
    box-shadow: none !important;
    padding: 0px !important;
    margin-bottom: 0px !important;
}
.divider {
    border-bottom: 2px solid #FFD700; 
    margin: 0px 0px 5px 0px; 
}
.section {
    margin-top: 10px;
    margin-bottom: 10px;
}
.stButton>button {
    background-color: #FFA500;
    color: black;
    font-size: 22px;
    padding: 14px 40px;
    border-radius: 12px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #FFD700; 
    color: #1E40AF;
}
</style>
""", unsafe_allow_html=True)

# 3. Main title and subtitle
st.markdown('<h1 style="text-align:left; font-size:50px; color:white; margin-bottom:10px;">✈️ CareerPilot AI</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:left; font-size:22px; color:white; margin-bottom:20px;">Your AI assistant that finds jobs and applies automatically</h3>', unsafe_allow_html=True)

# 4. Inputs section
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

# 6. Apply button section
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if st.button("Start AI Job Agent"):
    if not (job_roles and user_email and linkedin_email and linkedin_password and cv):
        st.warning("Please fill in all details and upload your CV.")
    elif run_agents:
        try:
            with st.spinner("Agent is working... This includes a 10s safety delay between steps."):
                # 2. Executing run_agents
                # Note: run_agents returns (results, screenshots)
                results, screenshots = run_agents(job_roles, linkedin_email, linkedin_password, user_email, cv)
                
                # 3. Adding the requested 10-second wait after the agent run
                time.sleep(10)
                
                # 4. Display Screenshots/Execution History
                st.subheader("📸 Execution Screenshots")
                cols = st.columns(len(screenshots))
                for idx, (title, img) in enumerate(screenshots.items()):
                    cols[idx].image(img, caption=title)

                # 5. Display Final Table
                df = pd.DataFrame(results)
                if not df.empty:
                    st.success(f"Processing complete! {len(df)} posts identified/processed.")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No relevant posts were found during this run.")
                    
        except Exception as e:
            st.error(f"Error during job agent run: {e}")
    else:
        st.error("Cannot run agents due to import error")
st.markdown('</div>', unsafe_allow_html=True)
