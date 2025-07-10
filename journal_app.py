import streamlit as st
import pandas as pd
from datetime import datetime

# ---------- Visualization Logic ----------
class WellnessVisualizer:
    def count_domain_entries(self, df):
        domain_mapping = {
            'Mind': ['emotion', 'clarity', 'thoughts', 'intrusions'],
            'Body': ['pain_level', 'pain_location', 'mobility'],
            'Fuel': ['meals', 'hydration', 'digestion', 'supplements'],
            'Rest': ['sleep_quality', 'sleep_routine', 'hygiene'],
            'Belong': ['connection', 'support', 'social_moment']
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
            st.write("Latest Entries", df.tail(10))

            domain_counts = self.count_domain_entries(df)
            st.write("Entries by HHAC Domain", domain_counts)

            if "pain_level" in df.columns:
                st.line_chart(df["pain_level"])

            if "emotion" in df.columns:
                st.bar_chart(df["emotion"].value_counts())

        except Exception as e:
            st.error(f"Erro
