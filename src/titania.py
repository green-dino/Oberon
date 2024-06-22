import os
import sqlite3
import streamlit as st
import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename='titania.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

# Function to get data from SQLite database or JSON file
def fetch_data_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.db':
        # It's an SQLite database
        try:
            conn = sqlite3.connect(file_path)
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
    elif file_extension == '.json':
        # It's a JSON file
        try:
            df = pd.read_json(file_path)
            return df.columns.tolist()  # Assuming each JSON file represents a single table-like structure
        except Exception as e:
            st.error(f"Error reading JSON file: {e}")
            logging.error(f"Error reading JSON file: {e}")
            return []
    else:
        st.error("Unsupported file format. Only .db (SQLite) and .json files are supported.")
        return []

# Function to search for available .db and .json files
def find_data_files(directory):
    try:
        return [f for f in os.listdir(directory) if f.endswith(('.db', '.json'))]
    except FileNotFoundError:
        st.error(f"Directory '{directory}' not found.")
        return []
    except PermissionError:
        st.error(f"Permission denied to access directory '{directory}'.")
        return []
    except Exception as e:
        st.error(f"Error accessing directory '{directory}': {e}")
        return []

# Function to display data from SQLite database or JSON file
def display_data(file_path, table_name, page_size=10):
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension == '.db':
        # It's an SQLite database
        query = f"SELECT * FROM {table_name}"
        df = get_data(query, file_path)
    elif file_extension == '.json':
        # It's a JSON file
        try:
            df = pd.read_json(file_path)
        except Exception as e:
            st.error(f"Error reading JSON file: {e}")
            logging.error(f"Error reading JSON file: {e}")
            df = pd.DataFrame()
    else:
        st.error("Unsupported file format. Only .db (SQLite) and .json files are supported.")
        df = pd.DataFrame()

    if df.empty:
        st.warning("No data available in the selected table or file.")
    else:
        st.write("Data:")
        
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

# Function to get data from SQLite database
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

def main():
    st.sidebar.title("Navigation")

    data_files = find_data_files('.')
    
    if not data_files:
        st.sidebar.warning("No database or JSON files found.")
        return

    data_choice = st.sidebar.selectbox("Select Data File", data_files)
    data_path = os.path.join('.', data_choice)
    
    # Fetching table or structure names from the selected file
    data_names = fetch_data_from_file(data_path)
    if not data_names:
        st.sidebar.warning("No tables or data structures found in the selected file.")
        return

    data_name = st.sidebar.selectbox("Select Table or Structure", data_names)
    
    options = ["View Data", "Run Custom Query"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "View Data":
        display_data(data_path, data_name)
    elif choice == "Run Custom Query":
        st.title("Run Custom Query")
        query = st.text_area("Enter SQL query", height=100)
        if st.button("Execute"):
            if query.strip().startswith("select"):
                df = get_data(query, data_path)
                if not df.empty:
                    st.write("Query result:")
                    st.dataframe(df)
                else:
                    st.warning("No data returned from the query.")
            else:
                st.error("Invalid query syntax. Please enter a valid SELECT statement.")

if __name__ == "__main__":
    main()
