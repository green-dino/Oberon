import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Organizational Improvement Dashboard", layout="wide")
st.title("Organizational Improvement Dashboard")

# Mock data for visualization
data = {
    "System": ["RootCause", "Trigger", "Event", "Incident", "AvoidAntipatterns", "SpreadRisks", "AdoptDevPractices",
               "Problem", "Change", "Request", "Loops", "Functions", "Mappings", "Playbooks", "Roles", "Align",
               "FreshData", "EffectiveAlerts"],
    "Category": ["Systems Analysis", "Systems Analysis", "Systems Analysis", "Systems Analysis", "Increasing Resilience", 
                 "Increasing Resilience", "Increasing Resilience", "Trouble Tickets", "Trouble Tickets", "Trouble Tickets", 
                 "Framework", "Framework", "Framework", "Framework", "Framework", "Reducing Detection Time", 
                 "Reducing Detection Time", "Reducing Detection Time"],
    "Metric": [20, 15, 30, 10, 25, 30, 35, 40, 50, 45, 15, 20, 10, 25, 30, 50, 45, 40]
}

df = pd.DataFrame(data)

# Plot the data
fig = px.bar(df, x="System", y="Metric", color="Category", title="Organizational Improvement Metrics",
             labels={"Metric": "Metric Value", "System": "Systems"})

st.plotly_chart(fig)

# Mock relationships graph
st.subheader("System Relationships")
st.graphviz_chart("""
    digraph {
        subgraph "cluster_0" {
            label = "Systems Analysis for Organizational Improvement";
            RootCause -> Event [label="Causes"];
            Trigger -> Event [label="Triggers"];
            Event -> Incident [label="Leads to"];
        }
        subgraph "cluster_1" {
            label = "Increasing the Time Between Failures";
            AvoidAntipatterns -> Resilience [label="Improves"];
            SpreadRisks -> Resilience [label="Improves"];
            AdoptDevPractices -> Resilience [label="Improves"];
        }
        subgraph "cluster_2" {
            label = "Trouble Tickets";
            Problem -> Change [label="Initiates"];
            Problem -> Incident [label="Initiates"];
            Problem -> Request [label="Initiates"];
            Change -> Implementation [label="Requires"];
            Change -> Validation [label="Requires"];
            Incident -> Investigation [label="Requires"];
            Incident -> Resolution [label="Requires"];
            Request -> Evaluation [label="Requires"];
            Request -> Fulfillment [label="Requires"];
        }
        subgraph "cluster_3" {
            label = "Framework";
            Loops -> Functions [label="Utilizes"];
            Loops -> Playbooks [label="Utilizes"];
            Functions -> Mappings [label="Defines"];
            Mappings -> Playbooks [label="Defines"];
            Playbooks -> Roles [label="Defines"];
            Roles -> Playbooks [label="Defines"];
        }
        subgraph "cluster_4" {
            label = "Reducing Time to Detect";
            Align -> SLIs [label="Improves"];
            FreshData -> SLIs [label="Improves"];
            EffectiveAlerts -> SLIs [label="Improves"];
        }
        Problem -> Align [label="Relates to"];
        Problem -> FreshData [label="Relates to"];
        Problem -> EffectiveAlerts [label="Relates to"];
        Resilience -> Change [label="Affects"];
        Resilience -> Incident [label="Affects"];
        Resilience -> Request [label="Affects"];
        Resilience -> Problem [label="Affects"];
        Resilience -> Align [label="Affects"];
        Resilience -> FreshData [label="Affects"];
        Resilience -> EffectiveAlerts [label="Affects"];
        Event -> Resilience [label="Affected by"];
        Incident -> Resilience [label="Affected by"];
    }
""")

# Adding interactive elements for user experience
st.sidebar.header("Filter Metrics")
categories = st.sidebar.multiselect("Select Categories", options=df["Category"].unique(), default=df["Category"].unique())

filtered_df = df[df["Category"].isin(categories)]
fig_filtered = px.bar(filtered_df, x="System", y="Metric", color="Category", title="Filtered Organizational Improvement Metrics",
                      labels={"Metric": "Metric Value", "System": "Systems"})

st.plotly_chart(fig_filtered)

st.sidebar.header("About")
st.sidebar.info("""
    This dashboard helps teams visualize and analyze various organizational processes, 
    including systems analysis, resilience improvement, trouble ticket management, 
    framework utilization, and detection time reduction.
""")
