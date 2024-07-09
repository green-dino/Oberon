import os
import sqlite3
import streamlit as st
import graphviz as gv
import json
from pyvis.network import Network
import streamlit.components.v1 as components

def get_db_connection():
    """
    Establish a connection to the SQLite database.

    Returns:
        conn (sqlite3.Connection): Database connection object.
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = st.connection('my_database')
    return conn

def fetch_query_results(query, params=()):
    """
    Execute a SQL query and fetch the results.

    Args:
        query (str): SQL query to execute.
        params (tuple): Parameters to pass to the query.

    Returns:
        results (list): List of fetched rows.
    """
    conn = get_db_connection()
    try:
        results = conn.query(query)
        return results
    except Exception as e:
        st.error(f"Database error: {e}")
        return []


def get_column_names():
    """
    Fetch and display column names from the 'elements' table.

    Returns:
        columns (list): List of column names.
    """
    query = "PRAGMA table_info(elements)"
    columns = [row[1] for row in fetch_query_results(query)]
    breakpoint()
    return columns

def fetch_elements(search_column, search_term):
    """
    Fetch rows from the database based on search term in a specific column.

    Args:
        search_column (str): Column to search in.
        search_term (str): Term to search for.

    Returns:
        elements (list): List of matching elements.
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
    suggestions = [row[0] for row in fetch_query_results(query)]
    return suggestions

def fetch_elements_by_type(element_type):
    """
    Fetch elements by type.

    Args:
        element_type (str): Type of elements to fetch.

    Returns:
        elements (list): List of elements of the specified type.
    """
    query = "SELECT * FROM elements WHERE element_type = ?"
    elements = fetch_query_results(query, (element_type,))
    return elements

def validate_input(play_name, roles, blocks, tasks):
    """
    Validate playbook input data.

    Args:
        play_name (str): Name of the play.
        roles (list): List of roles.
        blocks (list): List of blocks.
        tasks (list): List of tasks.

    Returns:
        errors (list): List of validation errors.
    """
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
    """
    Class to create a playbook graph using Graphviz.
    """
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
        """
        Get the Graphviz dot representation of the playbook graph.

        Returns:
            dot (graphviz.Digraph): Graphviz dot object.
        """
        return self.dot

def create_interactive_graph(play_name, roles, blocks, tasks):
    """
    Create an interactive graph using Pyvis.

    Args:
        play_name (str): Name of the play.
        roles (list): List of roles.
        blocks (list): List of blocks.
        tasks (list): List of tasks.

    Returns:
        net (pyvis.network.Network): Pyvis network object.
    """
    net = Network(directed=True)
    net.add_node(play_name, label=play_name, color='red', size=25)
    
    for role in roles:
        net.add_node(role, label=role, color='blue')
        net.add_edge(play_name, role)
    
    for block in blocks:
        net.add_node(block, label=block, color='green')
        net.add_edge(play_name, block)
    
    for task in tasks:
        net.add_node(task, label=task, color='orange')
        net.add_edge(play_name, task)

    return net

def save_playbook_to_file(playbook_data, version, author, filename="playbook.json"):
    """
    Save playbook data to a JSON file.

    Args:
        playbook_data (dict): Playbook data to save.
        version (str): Version of the playbook.
        author (str): Author of the playbook.
        filename (str): Name of the file to save the playbook in.
    """
    playbook_data.update({"version": version, "author": author})
    try:
        with open(filename, "w") as file:
            json.dump(playbook_data, file)
        st.success("Current playbook saved successfully.")
    except TypeError as e:
        st.error(f"Error saving playbook: {e}")

def load_playbook_from_file(filename="playbook.json"):
    """
    Load playbook data from a JSON file.

    Args:
        filename (str): Name of the file to load the playbook from.

    Returns:
        playbook_data (dict): Loaded playbook data.
    """
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        st.error(f"Error loading playbook: {e}")
        return {}

def display_playbook_graph(play_name, roles, blocks, tasks):
    """
    Display the playbook graph using Graphviz and Pyvis.

    Args:
        play_name (str): Name of the play.
        roles (list): List of roles.
        blocks (list): List of blocks.
        tasks (list): List of tasks.
    """
    st.header("Playbook Graph")
    creator = PlaybookGraphCreator(play_name, roles, blocks, tasks)
    st.graphviz_chart(creator.get_dot())

    st.header("Interactive Playbook Graph")
    net = create_interactive_graph(play_name, roles, blocks, tasks)
    net.write_html("playbook_graph.html")

    with open("playbook_graph.html", "r", encoding="utf-8") as f:
        components.html(f.read(), height=600)

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Playbook Builder")
    st.sidebar.header("Input Playbook Details")

    role_suggestions = fetch_suggestions('element_identifier')
    block_suggestions = fetch_suggestions('title')
    task_suggestions = fetch_suggestions('text')

    version = st.sidebar.text_input("Version")
    author = st.sidebar.text_input("Author")

    play_name = st.sidebar.text_input("Play Name")
    roles = st.sidebar.multiselect("Roles", options=role_suggestions)
    blocks = st.sidebar.multiselect("Blocks", options=block_suggestions)
    tasks = st.sidebar.multiselect("Tasks", options=task_suggestions)

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

    element_type = st.sidebar.text_input("Element Type")
    if st.sidebar.button("Fetch Elements by Type"):
        elements_by_type = fetch_elements_by_type(element_type)
        if elements_by_type:
            st.write("Elements of the specified type:")
            for element in elements_by_type:
                st.write(element)
        else:
            st.write("No elements found for the specified type.")

    if st.sidebar.button("Generate Playbook"):
        roles = [role.strip() for role in roles if role.strip()]
        blocks = [block.strip() for block in blocks if block.strip()]
        tasks = [task.strip() for task in tasks if task.strip()]

        errors = validate_input(play_name, roles, blocks, tasks)
        if errors:
            st.sidebar.error("\n".join(errors))
        else:
            display_playbook_graph(play_name, roles, blocks, tasks)
            
            playbook_data = {
                "play_name": play_name,
                "roles": roles,
                "blocks": blocks,
                "tasks": tasks
            }
            save_playbook_to_file(playbook_data, version, author)
            st.sidebar.success("Playbook generated and saved successfully.")
    
    if st.sidebar.button("Load Playbook"):
        playbook_data = load_playbook_from_file()
        if playbook_data:
            st.sidebar.success("Playbook loaded successfully.")
            st.write("Loaded Playbook Data:")
            st.write(playbook_data)
        else:
            st.sidebar.error("Failed to load playbook.")

if __name__ == "__main__":
    main()
