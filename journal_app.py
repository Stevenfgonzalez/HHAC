import streamlit as st
import pandas as pd
from datetime import datetime

# ========== Visualizer ==========
class WellnessVisualizer:
    def count_domain_entries(self, df):
        domain_mapping = {
            'Mind': ['emotion', 'clarity', 'thoughts', 'intrusive_thoughts'],
            'Body': ['pain_level', 'pain_location', 'mobility'],
            'Fuel': ['meals', 'hydration', 'digestion', 'supplements'],
            'Rest': ['sleep_quality', 'sleep_routine', 'hygiene'],
            'Belong': ['connection', 'support', 'social_moments']
        }
        domain_counts = {}
        for domain, fields in domain_mapping.items():
            count = sum(1 for field in fields if field in df.columns)
            if count > 0:
                domain_counts[domain] = count
        return domain_counts

    def create_dashboard(self):
        st.subheader("📊 HHAC Insights")
        try:
            df = pd.read_csv("journal_log.csv")
            st.write("📋 Recent Entries", df.tail())
            domain_counts = self.count_domain_entries(df)
            st.write("📈 Entry Count by Domain", domain_counts)
        except Exception as e:
            st.error(f"Error loading dashboard: {e}")

# ========== Streamlit App ==========
st.set_page_config(page_title="Healing Hand – Daily Log")

tab1, tab2 = st.tabs(["📓 Journal Entry", "📊 Insights"])

with tab :
