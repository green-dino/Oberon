import streamlit as st
from enum import Enum

from framework.frame_dictionary import (
    victim_country_dict,
    victim_industry_dict,
    victim_region_dict,
    victim_revenue_iso_currency_code_dict,
    actor_external_country_dict,
    actor_external_region_dict,
    actor_partner_country_dict,
    actor_partner_industry_dict,
    action_error_variety_dict,
    action_hacking_variety_dict,
    action_malware_variety_dict,
    attribute_availability_variety_dict,
    attribute_confidentiality_data_variety_dict,
    attribute_confidentiality_state_dict,
    attribute_integrity_variety_dict,
    discovery_method_external_variety_dict,
    discovery_method_internal_variety_dict,
    impact_iso_currency_code_dict,
    impact_loss_variety_dict,
    impact_overall_rating_dict,
    plus_analysis_status_dict,
    actor_partner_region_dict,
    value_chain_dict,
    action_error_vector_dict,
    action_hacking_vector_dict,
    actor_internal_job_change_dict,
    actor_internal_motive_dict,
    actor_internal_variety_dict,
    actor_external_variety_dict,
    action_malware_result_dict
)


class Unit(Enum):
    DAYS = "Days"
    HOURS = "Hours"
    MINUTES = "Minutes"
    SECONDS = "Seconds"

st.title("Cybersecurity Incident Reporting")

# Incident Information Section
with st.container():
    st.header("Incident Information")
    incident_id = st.text_input("Enter Incident ID:")
    source_id = st.text_input("Source ID:")
    reference = st.text_input("References:")
    confidence = st.selectbox("Confidence Level:", options=["Low", "Medium", "High"])
    summary = st.text_area("Incident Summary:")
    campaign_id = st.text_input("Campaign ID:")
    notes = st.text_area("Notes:")

# Timeline Section
with st.container():
    st.header("Timeline")

    # Helper function to create a selectbox with Enum options
    def select_enumbox(label, enum_class, key):
        return st.selectbox(label, options=[e.name for e in enum_class], key=key)
    
    # Helper function to create a number input with given parameters
    def number_input(label, min_value, max_value, key, step=1.0):
        return st.number_input(label, min_value=min_value, max_value=max_value, step=step, key=key)

    # Compromise
    with st.expander("Compromise"):
        timeline_compromise_unit = select_enumbox("Compromise Unit:", Unit, key="compromise_unit")

    # Containment
    with st.expander("Containment"):
        timeline_containment_unit = st.text_input("Containment Unit:", key="containment_unit")

    # Discovery
    with st.expander("Discovery"):
        timeline_discovery_unit = st.text_input("Discovery Unit:", key="discovery_unit")
        timeline_discovery_value = st.number_input("Discovery Value:", min_value=0.0, step=0.1, key="discovery_value")

    # Exfiltration
    with st.expander("Exfiltration"):
        timeline_exfiltration_unit = st.text_input("Exfiltration Unit:", key="exfiltration_unit")

    # Incident Date
    with st.expander("Incident Date"):
        col1, col2, col3 = st.columns(3)
        with col1:
            timeline_incident_day = st.number_input("Incident Day:", min_value=1, max_value=31, step=1, key="incident_day")
        with col2:
            timeline_incident_month = st.number_input("Incident Month:", min_value=1, max_value=12, step=1, key="incident_month")
        with col3:
            timeline_incident_year = st.number_input("Incident Year:", min_value=2000, max_value=2100, step=1, key="incident_year")

# Victim Information Section
with st.container():
    st.header("Victim Information")
    victim_country = st.selectbox("Victim Country:", options=list(victim_country_dict.keys()), key="victim_country")
    victim_employee_count = st.number_input("Employee Count:", min_value=0, key="victim_employee_count")
    victim_government = st.selectbox("Government Entity:", options=["Yes", "No"], key="victim_government")
    victim_industry = st.selectbox("Industry:", options=list(victim_industry_dict.keys()), key="victim_industry")
    victim_locations_affected = st.text_area("Locations Affected:", key="victim_locations_affected")
    victim_region = st.selectbox("Region:", options=list(victim_region_dict.keys()), key="victim_region")
    victim_revenue_amount = st.number_input("Revenue Amount:", min_value=0.0, step=0.1, key="victim_revenue_amount")
    victim_revenue_iso_currency_code = st.selectbox("Revenue ISO Currency Code:", options=list(victim_revenue_iso_currency_code_dict.keys()), key="victim_revenue_iso_currency_code")
    victim_secondary_amount = st.number_input("Secondary Amount:", min_value=0.0, step=0.1, key="victim_secondary_amount")
    victim_state = st.text_input("State:", key="victim_state")
    victim_victim_id = st.text_input("Victim ID:", key="victim_victim_id")

# Actor Information Section
with st.container():
    st.header("Actor Information")
    
    with st.expander("External Actor"):
        actor_external_country = st.selectbox("Country:", options=list(actor_external_country_dict.keys()), key="actor_external_country")
        actor_external_motive = st.text_input("Motive:", key="actor_external_motive")
        actor_external_notes = st.text_area("Notes:", key="actor_external_notes")
        actor_external_region = st.selectbox("Region:", options=list(actor_external_region_dict.keys()), key="actor_external_region")
        actor_external_variety = st.multiselect("Variety:", options=list(actor_external_variety_dict.keys()))

    with st.expander("Internal Actor"):
        actor_internal_job_change = st.multiselect("Job Change:", options=list(actor_internal_job_change_dict.keys()))
        actor_internal_motive = st.multiselect("Motive:", options=list(actor_internal_motive_dict.keys()))
        actor_internal_notes = st.text_area("Notes:", key="actor_internal_notes")
        actor_internal_variety = st.multiselect("Variety:", options=list(actor_internal_variety_dict.keys()))

    with st.expander("Partner Actor"):
        actor_partner_country = st.selectbox("Country:", options=list(actor_partner_country_dict.keys()), key="actor_partner_country")
        actor_partner_industry = st.selectbox("Industry:", options=list(actor_partner_industry_dict.keys()), key="actor_partner_industry")
        actor_partner_motive = st.text_input("Motive:", key="actor_partner_motive")
        actor_partner_region = st.selectbox("Region:", options=list(actor_partner_region_dict.keys()), key="actor_partner_region")

# Actions Section
with st.container():
    st.header("Actions Taken")
    
    with st.expander("Error"):
        action_error_notes = st.text_area("Notes:", key="action_error_notes")
        action_error_variety = st.selectbox("Variety:", options=list(action_error_variety_dict.keys()), key="action_error_variety")
        action_error_vector = st.multiselect("Vector:", options=list(action_error_vector_dict.keys()))

    with st.expander("Hacking"):
        action_hacking_notes = st.text_area("Notes:", key="action_hacking_notes")
        action_hacking_variety = st.selectbox("Variety:", options=list(action_hacking_variety_dict.keys()), key="action_hacking_variety")
        action_hacking_vector = st.multiselect("Vector:", options=list(action_hacking_vector_dict.keys()))

    with st.expander("Malware"):
        action_malware_cve = st.text_input("CVE:", key="action_malware_cve")
        action_malware_name = st.text_input("Name:", key="action_malware_name")
        action_malware_notes = st.text_area("Notes:", key="action_malware_notes")
        action_malware_result = st.multiselect("Result:", options=list(action_malware_result_dict.keys()), key="action_malware_result")
        action_malware_variety = st.selectbox("Variety:", options=list(action_malware_variety_dict.keys()), key="action_malware_variety")
        action_malware_vector = st.text_input("Vector:", key="action_malware_vector")

# Add other action types similarly...

# Attributes Section
with st.container():
    st.header("Attributes")
    with st.expander("Of Event"):
        attribute_availability_duration_unit = st.text_input("Availability Duration Unit:", key="availability_duration_unit")
        attribute_availability_duration_value = st.number_input("Availability Duration Value:", min_value=0.0, step=0.1, key="availability_duration_value")
        attribute_availability_notes = st.text_area("Availability Notes:", key="availability_notes")
        attribute_availability_variety = st.selectbox("Availability Variety:", options=list(attribute_availability_variety_dict.keys()), key="availability_variety")
        attribute_confidentiality_data_variety = st.selectbox("Confidentiality Data Variety:", options=list(attribute_confidentiality_data_variety_dict.keys()), key="confidentiality_data_variety")
        attribute_confidentiality_data_disclosure = st.text_input("Data Disclosure:", key="confidentiality_data_disclosure")
        attribute_confidentiality_data_total = st.number_input("Data Total:", min_value=0.0, step=0.1, key="confidentiality_data_total")
        attribute_confidentiality_data_victim = st.text_input("Data Victim:", key="confidentiality_data_victim")
        attribute_confidentiality_notes = st.text_area("Confidentiality Notes:", key="confidentiality_notes")
        attribute_confidentiality_state = st.selectbox("Confidentiality State:", options=list(attribute_confidentiality_state_dict.keys()), key="confidentiality_state")
        attribute_integrity_variety = st.selectbox("Integrity Variety:", options=list(attribute_integrity_variety_dict.keys()), key="integrity_variety")
        value_chain_dict = st.multiselect("Value Chain:", options=list(value_chain_dict.keys()))
# Discovery and Impact Section
with st.container():
    st.header("Discovery and Impact")
    discovery_method_external_variety = st.multiselect("External Discovery Method:", options=list(discovery_method_external_variety_dict.keys()), key="discovery_method_external_variety")
    discovery_method_internal_variety = st.multiselect("Internal Discovery Method:", options=list(discovery_method_internal_variety_dict.keys()), key="discovery_method_internal_variety")
    discovery_method_unknown = st.text_input("Unknown Discovery Method:", key="discovery_method_unknown")
    discovery_notes = st.text_area("Discovery Notes:", key="discovery_notes")
