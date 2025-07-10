import streamlit as st
import plotly.express as px
import pandas as pd

st.title("HHAC Journal: IERS, SECIT, CEDARS")
st.write("Track restoration, contributions, and energy metrics.")

# CEDARS Section
st.header("CEDARS Energy Tracker")
solar_output = st.slider("Solar Output (kWh)", 0, 100, 50)
contribution = st.text_area("Energy Contribution (e.g., solar maintenance)")
if contribution:
    st.success("Contribution logged: 10 energy credits earned!")

# IERS Section
st.header("IERS Restoration Tracker")
soil_health = st.slider("Soil Health (1-10)", 1, 10, 5)
water_retention = st.slider("Water Retention (1-10)", 1, 10, 5)

# SECIT Section
st.header("SECIT Contribution Tracker")
social_contribution = st.text_area("Social Contribution (e.g., elder care)")

# Save Data
if "journal_data" not in st.session_state:
    st.session_state.journal_data = []
st.session_state.journal_data.append({
    "Solar": solar_output,
    "Soil": soil_health,
    "Water": water_retention,
    "Social": social_contribution
})
st.write("Data saved!")

# Visualization
df = pd.DataFrame(st.session_state.journal_data)
fig = px.line(df, x=df.index, y=["Solar", "Soil", "Water"], title="Cross-Patent Metrics")
st.plotly_chart(fig)
