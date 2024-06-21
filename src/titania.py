import sqlite3
import streamlit as st
import pandas as pd

def get_data(query):
    conn = sqlite3.connect('src/nice.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def display_data():
    st.title("Database Viewer")
    
    query = "SELECT * FROM users"
    
    try:
        df = get_data(query)
        if df.empty:
            st.warning("No data available in the database.")
        else:
            st.write("Data from the database:")
            st.dataframe(df)
    except sqlite3.Error as e:
        st.error(f"SQLite error: {e}")
    except Exception as e:
        st.error(f"Error: {e}")

def main():
    st.sidebar.title("Navigation")
    options = ["View Data", "Run Custom Query"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "View Data":
        display_data()
    elif choice == "Run Custom Query":
        st.title("Run Custom Query")
        query = st.text_area("Enter SQL query", height=100)
        if st.button("Execute"):
            try:
                df = get_data(query)
                if df.empty:
                    st.warning("No data returned from the query.")
                else:
                    st.write("Query result:")
                    st.dataframe(df)
            except sqlite3.Error as e:
                st.error(f"SQLite error: {e}")
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
