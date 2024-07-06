import streamlit as st

# Define categories and their associated methods
CATEGORIES = {
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

class DataCollector:
    def __init__(self, categories):
        self.data_store = {}
        self.categories = categories

    def collect_data(self, method_name):
        """Collects data for a specific method."""
        if method_name not in self.categories:
            st.warning(f"Method {method_name} not found in categories.")
            return
        
        collected_data = st.text_input(f"Enter data for {method_name.replace('_', ' ').title()}:")
        
        if st.button(f"Submit {method_name.replace('_', ' ').title()}", key=f"{method_name}_submit"):
            self.data_store[method_name] = collected_data
            st.success(f"Data for {method_name.replace('_', ' ').title()} stored successfully!")

def main():
    # Initialize the data collector
    collector = DataCollector(CATEGORIES)

    # Ensure session state is initialized
    if 'data_store' not in st.session_state:
        st.session_state.data_store = {}

    # Dynamically display buttons and collect data based on categories
    for method_name, _ in CATEGORIES.items():
        collector.collect_data(method_name)

    # Update the session state with the latest data store
    st.session_state.data_store = collector.data_store

    # Display collected data
    st.write("### Collected Data")
    st.write(st.session_state.data_store)

if __name__ == "__main__":
    main()
