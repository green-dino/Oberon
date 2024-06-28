import streamlit as st

# Import pages
from home import home_page
from analysis import analysis_page
from clouds import 

# Initialize pages
home = st.Page(home_page, "Home")
analysis = st.Page(analysis_page, "Analysis")
clouds = st.Page(clouds, "Data")

# Set up navigation
st.navigation(home, analysis)
