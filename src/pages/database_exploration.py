import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3
import os
import plotly.express as px
import plotly.graph_objs as go
import networkx as nx


PROJECT_DIR = Path(__file__).parent
DB_PATH = Path(__file__).resolve().parent / '..' / 'database.db'
conn = sqlite3.connect(DB_PATH)

def get_data(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def create_networkx_graph(relationships_df):
    G = nx.from_pandas_edgelist(relationships_df, 'source_id', 'target_id')
    return G

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

   col1, col2, col3 = st.columns(3)
   with col1:
        st.subheader("Documents")
        if not documents_df.empty:
            doc_search = st.text_input("Search Documents")
            if doc_search:
                documents_df = documents_df[documents_df.apply(lambda row: doc_search.lower() in row.astype(str).str.lower().to_string(), axis=1)]
            st.write(documents_df)
            st.download_button("Download Documents as CSV", documents_df.to_csv(index=False), "documents.csv")

            st.subheader("Documents Visualization")
            doc_plot_type = st.selectbox("Select Plot Type", ["Bar Chart", "Line Chart"])
            if doc_plot_type == "Bar Chart":
                doc_fig = px.bar(documents_df, x=documents_df.columns[0], y=documents_df.columns[1])
            elif doc_plot_type == "Line Chart":
                doc_fig = px.line(documents_df, x=documents_df.columns[0], y=documents_df.columns[1])
            st.plotly_chart(doc_fig)

        with col2:
            st.subheader("Relationship Types")
            if not relationship_types_df.empty:
                rel_search = st.text_input("Search Relationship Types")
                if rel_search:
                    relationship_types_df = relationship_types_df[relationship_types_df.apply(lambda row: rel_search.lower() in row.astype(str).str.lower().to_string(), axis=1)]
                st.write(relationship_types_df)
                st.download_button("Download Relationship Types as CSV", relationship_types_df.to_csv(index=False), "relationship_types.csv")

                st.subheader("Relationship Types Visualization")
                rel_plot_type = st.selectbox("Select Plot Type", ["Bar Chart", "Line Chart"], key='rel')
                if rel_plot_type == "Bar Chart":
                    rel_fig = px.bar(relationship_types_df, x=relationship_types_df.columns[0], y=relationship_types_df.columns[1])
                elif rel_plot_type == "Line Chart":
                    rel_fig = px.line(relationship_types_df, x=relationship_types_df.columns[0], y=relationship_types_df.columns[1])
                st.plotly_chart(rel_fig)
        with col3:
            st.subheader("Elements")
            if not elements_df.empty:
                elem_search = st.text_input("Search Elements")
                if elem_search:
                    elements_df = elements_df[elements_df.apply(lambda row: elem_search.lower() in row.astype(str).str.lower().to_string(), axis=1)]
                st.write(elements_df)
                st.download_button("Download Elements as CSV", elements_df.to_csv(index=False), "elements.csv")

                st.subheader("Elements Visualization")
                elem_plot_type = st.selectbox("Select Plot Type", ["Bar Chart", "Line Chart", "Scatter Chart"], key='elem')
                if elem_plot_type == "Bar Chart":
                    elem_fig = px.bar(elements_df, x=elements_df.columns[0], y=elements_df.columns[1])
                elif elem_plot_type == "Line Chart":
                    elem_fig = px.line(elements_df, x=elements_df.columns[0], y=elements_df.columns[1])
                st.plotly_chart(elem_fig)
    
   st.subheader("Visualization:")
   if not relationship_types_df.empty:
       G = create_networkx_graph(relationship_types_df)
       fig = visualize_graph(G)
       st.plotly_chart(fig)

   st.subheader("Documents")
   st.write(documents_df)

   st.subheader("Relationship Types")
   st.write(relationship_types_df)

   st.subheader("Elements")
   st.write(elements_df)