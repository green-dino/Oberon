import os
import sqlite3
import streamlit as st
import graphviz as gv
import json
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd
from utilities.db_operations import get_db_connection, fetch_query_results, get_column_names, fetch_elements, fetch_suggestions, fetch_elements_by_type


class PlaybookUtils:
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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


class PlaybookGraphCreator:
    """
    Class to create a playbook graph using Graphviz.
    """
    def __init__(self, play_name, roles, blocks, tasks):
        self.dot = gv.Digraph()
        with self.dot.subgraph(name='cluster_playbook') as playbook:
            playbook.attr(label='Playbook')
            playbook.node('Play', play_name)
            self._add_nodes(playbook, roles, 'Role')
            self._add_nodes(playbook, blocks, 'Block')
            self._add_nodes(playbook, tasks, 'Task')

    def _add_nodes(self, playbook, items, prefix):
        for item in items:
            node_id = f'{prefix}_{item}'
            playbook.node(node_id, item)
            playbook.edge('Play', node_id)

    def get_dot(self):
        """
        Get the Graphviz dot representation of the playbook graph.

        Returns:
            dot (graphviz.Digraph): Graphviz dot object.
        """
        return self.dot


class InteractiveGraphCreator:
    @staticmethod
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
        InteractiveGraphCreator._add_nodes(net, roles, play_name, 'blue')
        InteractiveGraphCreator._add_nodes(net, blocks, play_name, 'green')
        InteractiveGraphCreator._add_nodes(net, tasks, play_name, 'orange')
        return net

    @staticmethod
    def _add_nodes(net, items, parent, color):
        for item in items:
            net.add_node(item, label=item, color=color)
            net.add_edge(parent, item)


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
    net = InteractiveGraphCreator.create_interactive_graph(play_name, roles, blocks, tasks)
    net.write_html("playbook_graph.html")

    with open("playbook_graph.html", "r", encoding="utf-8") as f:
        components.html(f.read(), height=600)


def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Playbook Builder")
    st.sidebar.header("Input Playbook Details")

    role_suggestions = fetch_suggestions('element_type')
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
        search_elements(search_column, search_term)

    element_type = st.sidebar.text_input("Element Type")
    if st.sidebar.button("Fetch Elements by Type"):
        fetch_and_display_elements_by_type(element_type)

    if st.sidebar.button("Generate Playbook"):
        roles = [role.strip() for role in roles if role.strip()]
        blocks = [block.strip() for block in blocks if block.strip()]
        tasks = [task.strip() for task in tasks if task.strip()]

        errors = PlaybookUtils.validate_input(play_name, roles, blocks, tasks)
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
            PlaybookUtils.save_playbook_to_file(playbook_data, version, author)
            st.sidebar.success("Playbook generated and saved successfully.")

    if st.sidebar.button("Load Playbook"):
        playbook_data = PlaybookUtils.load_playbook_from_file()
        if playbook_data:
            st.sidebar.success("Playbook loaded successfully.")
            st.write("Loaded Playbook Data:")
            st.write(playbook_data)
        else:
            st.sidebar.error("Failed to load playbook.")


def search_elements(search_column, search_term):
    try:
        elements = fetch_elements(search_column, search_term)
        if not elements.empty:
            st.write("Search Results:")
            for _, element in elements.iterrows():
                st.write({
                    "Element Identifier": element[0],
                    "Element Type": element[1],
                    "Title": element[2],
                    "Text": element[3]
                })
        else:
            st.write("No matching elements found.")
    except ValueError as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


def fetch_and_display_elements_by_type(element_type):
    elements_by_type = fetch_elements_by_type(element_type)
    if elements_by_type:
        st.write("Elements of the specified type:")
        for element in elements_by_type:
            st.write(element)
    else:
        st.write("No elements found for the specified type.")

if __name__ == "__main__":
    main()
