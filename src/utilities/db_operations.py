import os
import sqlite3
from functools import lru_cache
import asyncio
import streamlit as st
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """
    Establish a connection to the SQLite database.

    Returns:
        conn (sqlite3.Connection): Database connection object.
    """
    conn = st.connection('my_database')
    return conn


def fetch_query_results(query, params=(), db_name='my_database.db'):
    """
    Execute a SQL query and fetch the results.

    Args:
        query (str): SQL query to execute.
        params (tuple): Parameters to pass to the query.
        db_name (str): Name of the SQLite database file.

    Returns:
        results (pd.DataFrame): DataFrame of fetched rows.
    """
    conn = get_db_connection()
    try:
        df = conn.query(query)
        return df
    except Exception as e:
        logging.error(f"Database error: {e}")  # Logging the error
        return pd.DataFrame()

def get_column_names():
    """
    Fetch and display column names from the 'elements' table.

    Returns:
        columns (list): List of column names.
    """
    query = "PRAGMA table_info(elements)"
    columns = [row[0] for row in fetch_query_results(query).itertuples(index=False)]
    return columns

def fetch_elements(search_column, search_term):
    """
    Fetch rows from the database based on search term in a specific column.

    Args:
        search_column (str): Column to search in.
        search_term (str): Term to search for.

    Returns:
        elements (pd.DataFrame): DataFrame of matching elements.
    """
    query = f"""
        SELECT element_identifier, element_type, title, text 
        FROM elements 
        WHERE {search_column} LIKE ?
    """
    elements = fetch_query_results(query, ('%' + search_term + '%',))
    return elements

def fetch_suggestions(column_name):
    """
    Fetch unique suggestions for specific columns.

    Args:
        column_name (str): Column to fetch suggestions from.

    Returns:
        suggestions (list): List of unique suggestions.
    """
    query = f"SELECT DISTINCT {column_name} FROM elements"
    suggestions_df = fetch_query_results(query)
    if not suggestions_df.empty:
        suggestions = suggestions_df[column_name].tolist()
    else:
        suggestions = []
    return suggestions

def fetch_elements_by_type(element_type):
    """
    Fetch elements by type.

    Args:
        element_type (str): Type of elements to fetch.

    Returns:
        elements (pd.DataFrame): DataFrame of elements of the specified type.
    """
    query = "SELECT * FROM elements WHERE element_type = ?"
    elements = fetch_query_results(query, (element_type,))
    return elements
