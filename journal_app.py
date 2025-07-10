import streamlit as st
import pandas as pd

# Title of the app
st.title("Journal App")

# Initialize session state for data storage (in-memory, persists during session)
if 'entries' not in st.session_state:
    st.session_state.entries = pd.DataFrame(columns=['Domain', 'Date', 'Field1', 'Field2', 'Notes'])

# Function to add an entry
def add_entry(domain, date, field1, field2, notes):
    new_entry = pd.DataFrame({
        'Domain': [domain],
        'Date': [date],
        'Field1': [field1],
        'Field2': [field2],
        'Notes': [notes]
    })
    st.session_state.entries = pd.concat([st.session_state.entries, new_entry], ignore_index=True)

# Sidebar for domain selection
domain = st.sidebar.selectbox("Select Domain", ["Fire Station", "Simulation", "Personal"])

# Input form based on domain
with st.form(key="entry_form"):
    date = st.date_input("Date")
    if domain == "Fire Station":
        power_usage = st.number_input("Power Usage (kWh)", min_value=0.0)
        notes = st.text_input("Notes")
        submit = st.form_submit_button("Submit")
        if submit:
            add_entry(domain, date, power_usage, None, notes)
    elif domain == "Simulation":
        outage_duration = st.number_input("Outage Duration (hours)", min_value=0.0)
        result = st.text_input("Result")
        submit = st.form_submit_button("Submit")
        if submit:
            add_entry(domain, date, outage_duration, result, None)
    elif domain == "Personal":
        task = st.text_input("Task")
        notes = st.text_input("Notes")
        submit = st.form_submit_button("Submit")
        if submit:
            add_entry(domain, date, task, None, notes)

# Display all entries in a table
st.subheader("Logged Entries")
if not st.session_state.entries.empty:
    st.dataframe(st.session_state.entries)
else:
    st.info("No entries yet. Add one above!")

# Clear data button (optional)
if st.button("Clear All Entries"):
    st.session_state.entries = pd.DataFrame(columns=['Domain', 'Date', 'Field1', 'Field2', 'Notes'])
