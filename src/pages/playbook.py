import os
import sqlite3
import streamlit as st
import graphviz as gv
import json


def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = sqlite3.connect(db_path)
    return conn

# Function to fetch and display column names from the 'elements' table
def get_column_names():
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(elements)")
                columns = [row[1] for row in cursor.fetchall()]
            return columns
        except sqlite3.Error as e:
            st.error(f"Error fetching column names: {e}")
            return []
        finally:
            conn.close()
    return []

# Function to fetch rows from the database based on search term in a specific column
def fetch_elements(search_column, search_term):
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                query = f"""
                    SELECT element_identifier, element_type, title, text 
                    FROM elements 
                    WHERE {search_column} LIKE ?
                """
                cursor.execute(query, ('%' + search_term + '%',))
                elements = cursor.fetchall()
            return elements
        except sqlite3.Error as e:
            st.error(f"Error fetching elements: {e}")
            return []
        finally:
            conn.close()
    return []

# Function to fetch unique suggestions for specific columns
def fetch_suggestions(column_name):
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                query = f"SELECT DISTINCT {column_name} FROM elements"
                cursor.execute(query)
                suggestions = [row[0] for row in cursor.fetchall()]
            return suggestions
        except sqlite3.Error as e:
            st.error(f"Error fetching suggestions from column '{column_name}': {e}")
            return []
        finally:
            conn.close()
    return []

# Utility functions
def validate_input(play_name, roles, blocks, tasks):
    errors = []
    if not play_name:
        errors.append("Play name is required.")
    if not roles:
        errors.append("At least one role is required.")
    if not blocks:
        errors.append("At least one block is required.")
    if not tasks:
        errors.append("At least one task is required.")
    if any(not item for item in roles + blocks + tasks):
        errors.append("All entries must contain at least one item.")
    return errors

class PlaybookGraphCreator:
    def __init__(self, play_name, roles, blocks, tasks):
        self.dot = gv.Digraph()
        with self.dot.subgraph(name='cluster_playbook') as playbook:
            playbook.attr(label='Playbook')
            playbook.node('Play', play_name)
            for role in roles:
                playbook.node(f'Role_{role}', role)
                playbook.edge('Play', f'Role_{role}')
            for block in blocks:
                playbook.node(f'Block_{block}', block)
                playbook.edge('Play', f'Block_{block}')
            for task in tasks:
                playbook.node(f'Task_{task}', task)
                playbook.edge('Play', f'Task_{task}')

    def get_dot(self):
        return self.dot

def save_playbook_to_file(playbook_data, version, author, filename="playbook.json"):
    playbook_data.update({"version": version, "author": author})
    try:
        with open(filename, "w") as file:
            json.dump(playbook_data, file)
        st.success("Current playbook saved successfully.")
    except TypeError as e:
        st.error(f"Error saving playbook: {e}")

def load_playbook_from_file(filename="playbook.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        st.error(f"Error loading playbook: {e}")
        return {}

# Streamlit app layout
st.title("Playbook Builder")

st.sidebar.header("Input Playbook Details")

# Fetch suggestions for autocomplete
role_suggestions = fetch_suggestions('element_identifier')
block_suggestions = fetch_suggestions('title')
task_suggestions = fetch_suggestions('text')

version = st.sidebar.text_input("Version")
author = st.sidebar.text_input("Author")

# Inputs
play_name = st.sidebar.text_input("Play Name")
roles = st.sidebar.multiselect("Roles", options=role_suggestions)
blocks = st.sidebar.multiselect("Blocks", options=block_suggestions)
tasks = st.sidebar.multiselect("Tasks", options=task_suggestions)

# Search functionality
search_column = st.sidebar.selectbox("Search Column", options=['element_type'])
search_term = st.sidebar.text_input("Search Term (e.g., 'task')")

if st.sidebar.button("Search"):
    elements = fetch_elements(search_column, search_term)
    if elements:
        st.write("Search Results:")
        for element in elements:
            st.write({
                "Element Identifier": element[0],
                "Element Type": element[1],
                "Title": element[2],
                "Text": element[3]
            })
    else:
        st.write("No matching elements found.")

if st.sidebar.button("Generate Playbook"):
    roles = [role.strip() for role in roles if role.strip()]
    blocks = [block.strip() for block in blocks if block.strip()]
    tasks = [task.strip() for task in tasks if task.strip()]

    errors = validate_input(play_name, roles, blocks, tasks)

    if errors:
        for error in errors:
            st.sidebar.error(error)
    else:
        st.header("Playbook Graph")
        creator = PlaybookGraphCreator(play_name, roles, blocks, tasks)
        st.graphviz_chart(creator.get_dot())

# Save playbook
if st.sidebar.button("Save Current Playbook"):
    if 'playbook_data' not in st.session_state:
        st.session_state.playbook_data = {
            'play_name': play_name,
            'roles': roles,
            'blocks': blocks,
            'tasks': tasks
        }

    save_playbook_to_file(st.session_state.playbook_data, version, author)

# Additional options
st.sidebar.subheader("Other Options")
if st.sidebar.checkbox("Show Raw Inputs"):
    st.subheader("Raw Inputs")
    st.write(f"Play Name: {play_name}")
    st.write(f"Roles: {roles}")
    st.write(f"Blocks: {blocks}")
    st.write(f"Tasks: {tasks}")

st.write("Column Names in 'elements' table:", get_column_names())
