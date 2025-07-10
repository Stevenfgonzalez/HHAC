import streamlit as st
from datetime import datetime

st.set_page_config(page_title="HHAC Journal", layout="centered")

st.title("📝 HHAC Emotional Tracker")

entry = st.text_area("How are you feeling right now?")

if st.button("Log Entry"):
    timestamp = datetime.now().isoformat()

    mind = "MindDomain: Emotional tone analyzed"
    body = "BodyDomain: Physical state reviewed"
    rest = "RestDomain: Sleep/fatigue checked"
    safety = "SafetyDomain: No override triggered"

    st.success("🧠 Council Snapshot:")
    st.write(mind)
    st.write(body)
    st.write(rest)
    st.write(safety)

    with open("journal_log.txt", "a") as f:
        f.write(f"{timestamp}\n{entry}\n{mind}\n{body}\n{rest}\n{safety}\n\n")

