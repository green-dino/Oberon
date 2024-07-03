import streamlit as st
import graphviz as gv
import json
import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = sqlite3.connect(db_path)

    return conn


# Fetch elements from the database for autocomplete suggestions

def fetch_elements(prefix, element_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM elements LIMIT 1 OFFSET 1"
    params = (prefix + '%', element_type)
    cursor.execute(query, params)
    suggestions = [row[0] for row in cursor.fetchall()]

    conn.close()
    return suggestions

task_suggestions = fetch_elements('sort')

version = st.sidebar.text_input("Version")
author = st.sidebar.text_input("Author")

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

def create_playbook_graph(play_name, roles, blocks, tasks):
    dot = gv.Digraph()
    with dot.subgraph(name='cluster_playbook') as playbook:
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
    return dot

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



# Inputs
play_name = st.sidebar.text_input("Play Name")
roles = st.sidebar.text_area("Roles (comma separated)").split(',')
blocks = st.sidebar.text_area("Blocks (comma separated)").split(',')
tasks = st.sidebar.text_area("Tasks (comma separated)").split(',')

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
        dot = create_playbook_graph(play_name, roles, blocks, tasks)
        st.graphviz_chart(dot)

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
