import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt



# Define the mock method
def mock_method(name):
    st.write(f"Mock method {name} executed.")

# Group methods into categories
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

# Create a single method map
method_map = {method: mock_method for category in categories.values() for method in category}

class ChangeControlProcess:
    def __init__(self):
        self.method_map = method_map

    def execute_mock_method(self, method_name):
        """Executes the mock method associated with the given name."""
        if method_name in self.method_map:
            self.method_map[method_name](method_name)
        else:
            st.error(f"No mock method found for '{method_name}'.")

    # Generate method dynamically
    def __getattr__(self, name):
        if name in self.method_map:
            return lambda: self.execute_mock_method(name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

# Initialize the ChangeControlProcess object
process = ChangeControlProcess()

st.title("Change Control Process Demo")

# Example usage
process.identify_and_document_problem()

# Create columns for categories and buttons
num_columns = min(len(categories), 4)
cols = st.columns(num_columns)

for col, (category, methods) in zip(cols, categories.items()):
    with col:
        st.header(category)
        for method_name in methods:
            button_label = method_name.replace("_", " ").title()  # Improve button label readability
            button_key = f"{method_name}_button"
            st.button(button_label, key=button_key, on_click=lambda method=method_name: process.execute_mock_method(method))
            st.text("")

