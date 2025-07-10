import streamlit as st
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="HHAC Journal", layout="centered")
st.title("📝 Healing Hand AI Council – Daily Log")

# === Timestamp ===
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# === MIND ===
st.subheader("🧠 Mind")
emotion = st.selectbox("Current emotion:", ["Happy", "Angry", "Anxious", "Sad", "Overwhelmed", "Numb", "Grateful", "Motivated", "Other"])
clarity = st.slider("Mental clarity (1 = foggy, 10 = clear)", 1, 10, 5)
thoughts = st.text_area("Any thoughts or emotional triggers?")
intrusive = st.text_area("Intrusive thoughts or spirals?")
regulation_used = st.multiselect("Emotional regulation used:", ["Breathing", "Movement", "Talking", "Avoidance", "None"])
smiled = st.checkbox("Did you smile today?")

# === BODY ===
st.subheader("💪 Body")
pain = st.slider("Pain level (1 = none, 10 = worst)", 1, 10, 5)
pain_location = st.selectbox("Where is the pain?", ["Back", "Neck", "Hips", "Shoulder", "None", "Other"])
pain_description = st.text_area("Describe the discomfort:")
mobility = st.slider("Mobility today (1 = stiff, 10 = fluid)", 1, 10, 5)
body_care = st.multiselect("What did you use to support your body?", ["Heat", "Ice", "Movement", "Massage", "Medication", "None"])

# === FUEL ===
st.subheader("🥗 Fuel")
meals = st.text_area("What did you eat today?")
protein_first = st.selectbox("Did you eat protein first?", ["Yes", "No"])
hydration = st.slider("Hydration level (1 = dry, 10 = optimal)", 1, 10, 5)
consumed = st.multiselect("Did you consume any of these?", ["Sugar", "Dairy", "Gluten", "Processed Foods"])
supplements = st.text_area("Supplements taken:")
digest = st.selectbox("Did you feel satisfied or bloated after meals?", ["Satisfied", "Bloated", "Neutral"])

# === REST ===
st.subheader("🛌 Rest")
sleep_quality = st.slider("Sleep quality last night (1 = poor, 10 = great)", 1, 10, 5)
sleep_hours = st.text_input("Hours of sleep:")
night_routine = st.multiselect("Night routine followed:", ["Breathwork", "Screen limit", "Meditation", "Cold shower", "Journaling", "None"])
rest_disruptions = st.text_area("What disrupted your rest, if anything?")
woke_restored = st.selectbox("Did you wake up rested?", ["Yes", "No"])
hygiene = st.multiselect("Personal hygiene completed:", ["Shower", "Brushed Teeth", "Nails", "Shaved", "None"])

# === BELONG ===
st.subheader("🫂 Belong")
connection = st.selectbox("How connected did you feel today?", ["Isolated", "Neutral", "Connected", "Supported"])
interactions = st.text_area("Meaningful interactions (Who, how?)")
felt_seen = st.selectbox("Did you feel seen or heard?", ["Yes", "No"])
gave_support = st.selectbox("Did you offer support to someone else?", ["Yes", "No"])
relationship_notes = st.text_area("Any relationship stress or wins today?")
laughter = st.multiselect("Laughter moments?", ["Heard a joke", "Made someone laugh", "Smiled with someone", "None"])

# === Save Entry ===
if st.button("💾 Save Log Entry"):
    entry = {
        "Timestamp": timestamp,
        "Emotion": emotion,
        "Mental Clarity": clarity,
        "Thoughts": thoughts,
        "Intrusive Thoughts": intrusive,
        "Regulation Used": ", ".join(regulation_used),
        "Smiled": smiled,
        "Pain Level": pain,
        "Pain Location": pain_location,
        "Pain Description": pain_description,
        "Mobility": mobility,
        "Body Care": ", ".join(body_care),
        "Meals": meals,
        "Protein First": protein_first,
        "Hydration Level": hydration,
        "Consumed": ", ".join(consumed),
        "Supplements": supplements,
        "Digestion Feel": digest,
        "Sleep Quality": sleep_quality,
        "Sleep Hours": sleep_hours,
        "Night Routine": ", ".j
