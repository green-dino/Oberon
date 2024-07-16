import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Define mock method
def mock_method(name):
    st.write(f"Mock method {name} executed.")

# Define categories and their associated methods
categories = {
    "Problem Identification": [
        "identify_and_document_problem",
        "review_and_validate_problem",
    ],
    "Change Control": [
        "create_change_control_record",
        "capture_document_control_info",
        "develop_implementation_plan",
    ],
    "Stakeholder Management": [
        "identify_stakeholders_and_communication",
    ],
    "Risk and Impact Assessment": [
        "conduct_risk_assessment",
        "conduct_impact_evaluation",
    ],
    "Document References": [
        "reference_documents_and_resources",
    ],
    "Fulfillment and Roles": [
        "initiate_fulfillment_process",
        "select_role_for_tasks",
    ],
    "Trouble Tickets": [
        "manage_trouble_tickets",
    ],
    "Status View": [
        "view_change_status",
    ],
}

# Generate some mock metrics data
data = {
    "Category": [],
    "Task": [],
    "Count": [],
}

for category, tasks in categories.items():
    for task in tasks:
        data["Category"].append(category)
        data["Task"].append(task)
        data["Count"].append(int(np.random.randint(1, 100)))  # Random count for demonstration

df = pd.DataFrame(data)

class ChangeControlProcess:
    def __init__(self):
        self.method_map = {method: mock_method for category in categories.values() for method in category}

    def execute_mock_method(self, method_name):
        """Executes the mock method associated with the given name."""
        if method_name in self.method_map:
            self.method_map[method_name](method_name)
        else:
            st.error(f"No mock method found for '{method_name}'.")

    def __getattr__(self, name):
        if name in self.method_map:
            return lambda: self.execute_mock_method(name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

# Initialize the ChangeControlProcess object
process = ChangeControlProcess()

st.title("Change Control Process Dashboard")

# Organize UI into columns
num_columns = min(len(categories), 4)
cols = st.columns(num_columns)

# Display buttons for each category and method
for col, (category, methods) in zip(cols, categories.items()):
    with col:
        st.header(category)
        for method_name in methods:
            button_label = method_name.replace("_", " ").title()
            button_key = f"{method_name}_button"
            if st.button(button_label, key=button_key, on_click=lambda method=method_name: process.execute_mock_method(method)):
                st.write(f"Executing {method_name}...")

# New container for metrics visualization
with st.container():
    st.header("Metrics")
    
    # Mock data for visualization
    metrics_data = {
        "Category": list(categories.keys()),
        "Methods": [len(methods) for methods in categories.values()],
        "Last Executed": ["None"] * len(categories),
    }
    
    metrics_df = pd.DataFrame(metrics_data)
    st.table(metrics_df)

# Bar chart for task counts per category
st.write("### Task Counts per Category")
bar_chart = alt.Chart(df).mark_bar().encode(
    x='Category:N',
    y='sum(Count):Q',
    color='Category:N',
    tooltip=['Category', 'sum(Count)']
).properties(
    width=600,
    height=400
).interactive()

st.altair_chart(bar_chart)

# Pie chart for task distribution
st.write("### Task Distribution")
pie_chart = alt.Chart(df).mark_arc().encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Category", type="nominal"),
    tooltip=['Category', 'Count']
).properties(
    width=600,
    height=400
).interactive()

st.altair_chart(pie_chart)

# Line chart for task counts over time (mock time series data)
st.write("### Task Counts Over Time")
df_time_series = df.copy()
df_time_series["Date"] = pd.date_range(start='1/1/2022', periods=len(df_time_series), freq='M')

line_chart = alt.Chart(df_time_series).mark_line().encode(
    x='Date:T',
    y='Count:Q',
    color='Category:N',
    tooltip=['Date', 'Count', 'Category']
).properties(
    width=600,
    height=400
).interactive()

st.altair_chart(line_chart)
