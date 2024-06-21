import os
import sqlite3
import streamlit as st
import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename='titania.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

# Function to get data from the selected database
def get_data(query, db_path):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        st.error(f"SQLite error: {e}")
        logging.error(f"SQLite error in query '{query}': {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        logging.error(f"Error in query '{query}': {e}")
        return pd.DataFrame()

# Function to fetch table names from the database
def fetch_table_names(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        return [table[0] for table in tables]
    except sqlite3.Error as e:
        st.error(f"SQLite error: {e}")
        logging.error(f"SQLite error fetching table names: {e}")
        return []
    except Exception as e:
        st.error(f"Error: {e}")
        logging.error(f"Error fetching table names: {e}")
        return []

# Function to display the database content
def display_data(db_path, table_name, page_size=10):
    st.title("Database Viewer")
    query = f"SELECT * FROM {table_name}"
    
    df = get_data(query, db_path)
    if df.empty:
        st.warning("No data available in the selected table.")
    else:
        st.write("Data from the database:")
        
        if 'start_index' not in st.session_state:
            st.session_state.start_index = 0
        if 'page_size' not in st.session_state:
            st.session_state.page_size = page_size
        
        start_index = st.session_state.start_index
        end_index = start_index + st.session_state.page_size
        paged_df = df.iloc[start_index:end_index]
        st.dataframe(paged_df)
        
        # Pagination controls
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("Previous Page"):
                st.session_state.start_index = max(0, start_index - st.session_state.page_size)
        with col2:
            if st.button("Next Page"):
                st.session_state.start_index = start_index + st.session_state.page_size
        with col3:
            st.write(f"Showing rows {start_index + 1} to {min(end_index, len(df))} of {len(df)}")

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

    databases = find_databases('.')
    
    if not databases:
        st.sidebar.warning("No database files found.")
        return

    db_choice = st.sidebar.selectbox("Select Database", databases)
    db_path = os.path.join('.', db_choice)
    
    # Fetching table names for the selected database
    table_names = fetch_table_names(db_path)
    if not table_names:
        st.sidebar.warning("No tables found in the selected database.")
        return

    table_name = st.sidebar.selectbox("Select Table", table_names)
    
    options = ["View Data", "Run Custom Query"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "View Data":
        display_data(db_path, table_name)
    elif choice == "Run Custom Query":
        st.title("Run Custom Query")
        query = st.text_area("Enter SQL query", height=100)
        if st.button("Execute"):
            if query.strip().startswith("select"):
                df = get_data(query, db_path)
                if not df.empty:
                    st.write("Query result:")
                    st.dataframe(df)
                else:
                    st.warning("No data returned from the query.")
            else:
                st.error("Invalid query syntax. Please enter a valid SELECT statement.")

if __name__ == "__main__":
    main()
