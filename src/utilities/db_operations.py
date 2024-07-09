import os
import sqlite3
from functools import lru_cache
import asyncio
import streamlit as st


# Constants
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')

def get_db_connection():
    """
    Establish and return a database connection.
    
    Returns:
        sqlite3.Connection: The database connection object.
    """
    return st.connection('my_database')
    #return sqlite3.connect(DB_PATH)

@lru_cache(maxsize=32)
def fetch_query_results(query, params=()):
    """
    Fetch the results of a database query.
    
    Args:
        query (str): The SQL query to execute.
        params (tuple): The parameters to use with the SQL query.
        
    Returns:
        list: The results of the query.
        
    Raises:
        Exception: If a database error occurs.
    """
    conn = get_db_connection()
    try:
        with conn:
            breakpoint()
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        raise Exception(f"Database error: {e}")
    finally:
        conn.close()


