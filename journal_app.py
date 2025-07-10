import streamlit as st
import pandas as pd
from datetime import datetime

# ======== Visualization Logic ========
class WellnessVisualizer:
    def count_domains(self, df):
        domain_mapping = {
            'Mind': 'Mind',
            'Body': 'Body',
            'Fuel': 'Fuel',
            'Rest': 'Rest',
            'Belong': 'Belong'
        }

        domain_counts = {k: 0 for k in domain_mapping.values()}
        for domain in df['Domain']:
            if domain in domain_counts:
                domain_counts[domain] += 1

        return domain_counts

    def create_dashboard(self, df):
        st.subheader("📊 HHAC Journal Insights")
        try:
            st.write("Logged
