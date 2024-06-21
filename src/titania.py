import os
import sqlite3
import streamlit as st
import pandas as pd

# Function to get data from the selected database
def get_data(query, db_path):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        st.error(f"SQLite error: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# Function to display the database content
def display_data(db_path, table_name):
    st.title("Database Viewer")
    
    query = f"SELECT * FROM {table_name}"
    
    df = get_data(query, db_path)
    if df.empty:
        st.warning("No data available in the database.")
    else:
        st.write("Data from the database:")
        st.dataframe(df)

# Function to search for available .db files
def find_databases(directory):
    try:
        return [f for f in os.listdir(directory) if f.endswith('.db')]
    except FileNotFoundError:
        st.error(f"Directory '{directory}' not found.")
        return []
    except PermissionError:
        st.error(f"Permission denied to access directory '{directory}'.")
        return []
    except Exception as e:
        st.error(f"Error accessing directory '{directory}': {e}")
        return []

def main():
    st.sidebar.title("Navigation")

    # Search for .db files in the current directory (where app.py is located)
    databases = find_databases('.')
    
    if not databases:
        st.sidebar.warning("No database files found.")
        return

    # Present available databases to the user
    db_choice = st.sidebar.selectbox("Select Database", databases)

    # Full path to the selected database
    db_path = os.path.join('.', db_choice)

    # Provide a text input for the table name
    table_name = st.sidebar.text_input("Table Name", "users")

    options = ["View Data", "Run Custom Query"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "View Data":
        display_data(db_path, table_name)
    elif choice == "Run Custom Query":
        st.title("Run Custom Query")
        query = st.text_area("Enter SQL query", height=100)
        if st.button("Execute"):
            df = get_data(query, db_path)
            if df.empty:
                st.warning("No data returned from the query.")
            else:
                st.write("Query result:")
                st.dataframe(df)

if __name__ == "__main__":
    main()
