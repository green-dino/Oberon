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


# Function to filter JSON data
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

# Function to visualize data using matplotlib
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

# Main function
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
                    st.json(json_content)
                    st.subheader("Structure of the JSON file:")
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
                    st.json(json_content)
                    st.subheader("Structure of the JSON file:")
                    display_json_structure(json_content)
                    st.subheader("Data Visualization:")
                    visualize_data(json_content)
            except FileNotFoundError:
                st.error(f"File not found at path: {local_file_path}")
            except json.JSONDecodeError:
                st.error("The file at the specified path is not a valid JSON file.")

if __name__ == "__main__":
    main()
