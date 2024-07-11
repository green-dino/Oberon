import streamlit as st
import pandas as pd


# Connect to the database
conn = st.connection('my_database')


# Execute a query
results = conn.query('SELECT * FROM elements')
roles = conn.query('SELECT DISTINCT element_type FROM elements')
titles = conn.query('SELECT DISTINCT title FROM elements')
#breakpoint()
element_identity = conn.query('SELECT DISTINCT element_identifier from ELEMENTS')




# Display the results
st.dataframe(results)
st.dataframe(roles)
st.dataframe(titles)
st.dataframe(element_identity)
st.dataframe()