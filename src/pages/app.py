import streamlit as st


import pages.clouds as clouds


# Initialize pages
#home = st.Page(home, "Home")

clouds = st.Page(clouds, "Data")

# Set up navigation
st.navigation(home, analysis)
