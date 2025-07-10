import streamlit as st
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="HHAC Journal", layout="centered")

st.title("📝 HHAC Personal Journal")

# Emotion selector
emotion = st.selectbox("How are you feeling right now?", [
    "😃 Happy", "😔 Sad", "😡 Angry", "😰 Anxious", "😐 Neutral", "🤯 Overwhelmed", "❤️ Grateful"
])

# Pain level slider
pain_level = st.slider("Physical pain level (1 = none, 10 = extreme)", 1, 10, 5)

# Thought log
thoughts = st.text_area("What’s on your mind? (Triggers, thoughts, events)", height=150)

# Timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Save to CSV
if st.button("💾 Save Entry"):
    entry = {
        "Timestamp": timestamp,
        "Emotion": emotion,
        "Pain Level": pain_level,
        "Thoughts": thoughts
    }
    df = pd.DataFrame([entry])

    # Append to local CSV file
    if not os.path.exists("journal_log.csv"):
        df.to_csv("journal_log.csv", index=False)
    else:
        df.to_csv("journal_log.csv", mode='a', header=False, index=False)

    st.success("✅ Entry saved!")
