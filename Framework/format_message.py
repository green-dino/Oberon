KEYNAMES = [
    'incident_id', 'source_id', 'reference', 'confidence', 'summary', 'campaign_id', 
    'notes', 'timeline.compromise.unit', 'timeline.containment.unit', 'timeline.discovery.unit', 
    'timeline.discovery.value', 'timeline.exfiltration.unit', 'timeline.incident.day', 
    'timeline.incident.month', 'timeline.incident.year', 'victim.country', 'victim.employee_count', 
    'victim.government', 'victim.industry', 'victim.locations_affected', 'victim.region', 
    'victim.revenue.amount', 'victim.revenue.iso_currency_code', 'victim.secondary.amount', 
    'victim.state', 'victim.victim_id', 'actor.external.country', 'actor.external.motive', 
    'actor.external.notes', 'actor.external.region', 'actor.external.variety', 'actor.internal.job_change', 
    'actor.internal.motive', 'actor.internal.notes', 'actor.internal.variety', 'actor.partner.country', 
    'actor.partner.industry', 'actor.partner.motive', 'actor.partner.region', 'action.error.notes', 
    'action.error.variety', 'action.error.vector', 'action.hacking.notes', 'action.hacking.variety', 
    'action.hacking.vector', 'action.malware.cve', 'action.malware.name', 'action.malware.notes', 
    'action.malware.result', 'action.malware.variety', 'action.malware.vector', 'action.misuse.variety', 
    'action.misuse.vector', 'action.physical.variety', 'action.physical.vector', 'action.social.target', 
    'action.social.variety', 'action.social.vector', 'attribute.availability.duration.unit', 
    'attribute.availability.duration.value', 'attribute.availability.notes', 'attribute.availability.variety', 
    'attribute.confidentiality.data.variety', 'attribute.confidentiality.data_disclosure', 
    'attribute.confidentiality.data_total', 'attribute.confidentiality.data_victim', 
    'attribute.confidentiality.notes', 'attribute.confidentiality.state', 'attribute.integrity.variety', 
    'discovery_method.external.variety', 'discovery_method.internal.variety', 'discovery_method.unknown', 
    'discovery_notes', 'targeted', 'asset.assets.variety', 'asset.cloud', 'asset.country', 'asset.management', 
    'asset.notes', 'asset.total_amount', 'impact.iso_currency_code', 'impact.loss.variety', 
    'impact.overall_amount', 'impact.overall_rating', 'plus.analysis_status', 'plus.analyst', 'plus.analyst_notes', 
    'plus.asset.total', 'plus.asset_os', 'plus.attribute.confidentiality.credit_monitoring', 
    'plus.attribute.confidentiality.credit_monitoring_years', 'plus.attribute.confidentiality.data_abuse', 
    'plus.created', 'plus.dbir_year', 'plus.event_chain', 'plus.github', 'plus.master_id', 'plus.modified', 
    'plus.sub_source', 'plus.timeline.notification.day', 'plus.timeline.notification.month', 
    'plus.timeline.notification.year', 'schema_version', 'security_incident', 'value_chain.cash-out.variety', 
    'value_chain.development.variety', 'value_chain.distribution.variety', 'value_chain.targeting.variety'
]

def format_incident_message(incident_data):
    message_lines = []
    
    for key in KEYNAMES:
        if key in incident_data:
            message_lines.append(f"{key.replace('.', ' ').capitalize()}: {incident_data[key]}")
        else:
            message_lines.append(f"{key.replace('.', ' ').capitalize()}: N/A")
    
    return "\n".join(message_lines)

# Example incident data dictionary
incident_data = {
    'incident_id': 'INC123456',
    'source_id': 'SRC7890',
    'confidence': 'High',
    'summary': 'Data breach involving unauthorized access.',
    'timeline.incident.day': 12,
    'timeline.incident.month': 6,
    'timeline.incident.year': 2024,
    'victim.country': 'US',
    'victim.industry': 'Healthcare',
    'actor.external.country': 'CN',
    'action.hacking.variety': 'SQL injection',
    'impact.overall_amount': '1000000',
    'impact.iso_currency_code': 'USD',
}

formatted_message = format_incident_message(incident_data)
print(formatted_message)