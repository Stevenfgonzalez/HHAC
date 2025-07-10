import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="HHAC Journal", page_icon="📝", layout="centered")

# Load or create log file
LOG_FILE = "journal_log.csv"
if os.path.exists(LOG_FILE):
    journal_df = pd.read_csv(LOG_FILE)
else:
    journal_df = pd.DataFrame(columns=["Timestamp", "Domain", "Rating", "Notes"])

# App title
st.title("HHAC Journal Logger")

# Domain options
domain_options = ["Mind", "Body", "Fuel", "Rest", "Belong"]
domain = st.selectbox("Which domain are you logging?", domain_options)

# Rating scale
rating = st.slider("How are you doing in this domain (1 = struggling, 10 = thriving)?", 1, 10, 5)

# Notes
notes = st.text_area("Any notes or context you want to add?")

# Submit entry
if st.button("Log Entry"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([[timestamp, domain, rating, notes]], columns=journal_df.columns)
    journal_df = pd.concat([journal_df, new_entry], ignore_index=True)
    journal_df.to_csv(LOG_FILE, index=False)
    st.success("Entry logged!")

# Optional: View recent entries
if st.checkbox("Show recent entries"):
    st.dataframe(journal_df.tail(10))
