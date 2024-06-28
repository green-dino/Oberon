import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3
import os

PROJECT_DIR = Path(__file__).parent
DB_PATH = Path(__file__).resolve().parent / '..' / 'database.db'
conn = sqlite3.connect(DB_PATH)


def get_documents():
    documents_df = pd.read_sql("SELECT * FROM documents", conn)
    return documents_df

def get_relationship_types():
    relationship_types_df = pd.read_sql("SELECT * FROM relationship_types", conn)
    return relationship_types_df

def get_elements():
    elements_df = pd.read_sql("SELECT * FROM elements", conn)
    return elements_df

if __name__ == '__main__':
   st.set_page_config(layout='wide')

   documents_df = get_documents()
   relationship_types_df = get_relationship_types()
   elements_df = get_elements()

   st.header("My Database App")

   st.subheader("Documents")
   st.write(documents_df)

   st.subheader("Relationship Types")
   st.write(relationship_types_df)

   st.subheader("Elements")
   st.write(elements_df)