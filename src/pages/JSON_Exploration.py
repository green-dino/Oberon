import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import json
import matplotlib.pyplot as plt

class GraphVisualization:
    @staticmethod
    def create_graph_from_df(df, source_col, target_col):
        df[source_col] = df[source_col].fillna('')
        df[target_col] = df[target_col].fillna('')
        
        G = nx.Graph()
        for _, row in df.iterrows():
            G.add_edge(row[source_col], row[target_col])
        return G
    
    @staticmethod
    def validate_nodes(G):
        for node in G.nodes:
            if not isinstance(node, (str, int)):
                raise InvalidNodeTypeException(f"Node {node} has an invalid identifier type.")
    
    @staticmethod
    def setup_pyvis_network(G):
        net = Network(height="750px", width="100%", directed=False, notebook=False)
        pos = nx.spring_layout(G, seed=42)
        for node, (x, y) in pos.items():
            net.add_node(node, x=x, y=y)
        for edge in G.edges():
            net.add_edge(*edge)
        return net
    
    @staticmethod
    def render_pyvis_network(net):
        net.show_buttons(filter_=['physics'])
        net_html = net.generate_html()
        st.components.v1.html(net_html, height=750, scrolling=True)

def filter_json_data(json_data, filter_key='', filter_value=''):
    filtered_data = []
    if isinstance(json_data, dict):
        filtered_data.extend([{'key': key, 'value': value} for key, value in json_data.items()
                              if filter_key.lower() in str(key).lower() or filter_value.lower() in str(value).lower()])
        for value in json_data.values():
            if isinstance(value, (dict, list)):
                filtered_data.extend(filter_json_data(value, filter_key, filter_value))
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, (dict, list)):
                filtered_data.extend(filter_json_data(item, filter_key, filter_value))
    return filtered_data

def visualize_data(json_data):
    if isinstance(json_data, dict):
        keys = list(json_data.keys())
        values = list(json_data.values())
        if all(isinstance(v, (int, float)) for v in values):
            plt.bar(keys, values)
            plt.xlabel('Keys')
            plt.ylabel('Values')
            st.pyplot()
        elif all(isinstance(v, str) for v in values):
            plt.pie(values, labels=keys, autopct='%1.1f%%')
            st.pyplot()
        else:
            st.write("Visualization not supported for this data type.")
    elif isinstance(json_data, list):
        st.write("Visualization not supported for list type data.")

def display_json_structure(json_content):
    st.json(json_content)

def main():
    st.title("JSON File Explorer")
    
    file_option = st.sidebar.selectbox(
        "Select how to load your JSON file:",
        ("Upload", "Local File")
    )

    if file_option == "Upload":
        uploaded_file = st.file_uploader("Upload a JSON file", type="json")
        if uploaded_file is not None:
            try:
                json_content = json.load(uploaded_file)
                search_term = st.sidebar.text_input("Search term:", "")
                filter_key = st.sidebar.text_input("Filter by key:", "")
                filter_value = st.sidebar.text_input("Filter by value:", "")

                if search_term or filter_key or filter_value:
                    st.subheader("Filtered Contents of the JSON file:")
                    filtered_data = filter_json_data(json_content, filter_key, filter_value)
                    if filtered_data:
                        for item in filtered_data:
                            display_json_structure(item['value'])
                            st.subheader("Data Visualization:")
                            visualize_data(item['value'])
                    else:
                        st.write("No matching data found.")
                else:
                    st.subheader("Contents of the JSON file:")
                    display_json_structure(json_content)
                    st.subheader("Data Visualization:")
                    visualize_data(json_content)
            except json.JSONDecodeError:
                st.error("The uploaded file is not a valid JSON file.")
    elif file_option == "Local File":
        local_file_path = st.sidebar.text_input("Enter path to your local JSON file:", "")
        if st.sidebar.button("Load"):
            try:
                with open(local_file_path, 'r') as file:
                    json_content = json.load(file)
                    st.subheader("Contents of the JSON file:")
                    display_json_structure(json_content)
                    st.subheader("Data Visualization:")
                    visualize_data(json_content)
            except FileNotFoundError:
                st.error(f"File not found at path: {local_file_path}")
            except json.JSONDecodeError:
                st.error("The file at the specified path is not a valid JSON file.")

if __name__ == "__main__":
    main()
