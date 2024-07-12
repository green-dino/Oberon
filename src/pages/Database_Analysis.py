import pygwalker as pyg
import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3
from utilities.db_operations import get_db_connection, fetch_query_results, get_column_names, fetch_elements, fetch_suggestions, fetch_elements_by_type

# Define constants
PROJECT_DIR = Path(__file__).parent
DB_PATH = PROJECT_DIR / '..' / 'database.db'

def get_database_connection():
    try:
        conn = sqlite3.connect(str(DB_PATH))
        return conn
    except sqlite3.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

def get_table_names(conn):
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(query, conn)
    return tables['name'].tolist()

def get_column_names(conn, table_name):
    query = f"PRAGMA table_info({table_name});"
    columns = pd.read_sql(query, conn)
    return columns['name'].tolist()

def fetch_data(conn, table_name, columns):
    query = f"SELECT {', '.join(columns)} FROM {table_name};"
    data = pd.read_sql(query, conn)
    return data

# Set up the Streamlit app
st.set_page_config(page_title="Database Exploration Tool", layout="wide")
st.title("Database Exploration Tool")

# Get database connection
conn = get_database_connection()

if conn:
    # Sidebar for user input
    st.sidebar.header("Build Your Custom DataFrame")
    table_name = st.sidebar.selectbox("Select a table", get_table_names(conn))

    if table_name:
        columns = st.sidebar.multiselect("Select columns", get_column_names(conn, table_name))
        
        # Generate DataFrame and Pygwalker HTML on button click
        if st.sidebar.button("Generate DataFrame") and columns:
            df = fetch_data(conn, table_name, columns)
            st.write("Your Custom DataFrame:")
            st.dataframe(df)

            pyg_html = pyg.walk(df, return_html=True, hideDataSourceConfig=False)
            st.components.v1.html(pyg_html, height=1000, scrolling=True)

    # Close the connection when done
    conn.close()
else:
    st.error("Could not connect to the database.")
