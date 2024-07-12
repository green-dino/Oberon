import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network

class DataCommunitiesVisualizer:
    def __init__(self):
        st.set_page_config(page_title="Data Communities", layout="wide")
        st.title("Data Communities Visualization")
        
    @staticmethod
    def read_csv(file):
        try:
            return pd.read_csv(file)
        except Exception as e:
            raise FileUploadException(f"Failed to read CSV file: {e}")
    
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
    
    def render_visualization(self, net):
        net.show_buttons(filter_=['physics'])
        net_html = net.generate_html()
        st.components.v1.html(net_html, height=750, scrolling=True)
    
    def main(self):
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        if uploaded_file is not None:
            df = self.read_csv(uploaded_file)
            st.write("Data Preview:")
            st.dataframe(df.head())
            
            source_col = st.selectbox("Select Source Column", df.columns)
            target_col = st.selectbox("Select Target Column", df.columns)
            
            if st.button("Create Visualization"):
                G = self.create_graph_from_df(df, source_col, target_col)
                self.validate_nodes(G)  # Validate nodes before setting up the network
                net = self.setup_pyvis_network(G)
                self.render_visualization(net)
        else:
            st.write("Please upload a CSV file to visualize the data communities.")

if __name__ == "__main__":
    visualizer = DataCommunitiesVisualizer()
    visualizer.main()
