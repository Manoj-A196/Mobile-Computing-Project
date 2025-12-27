import streamlit as st

st.title("Device Control")

device = st.selectbox(
    "Select Device",
    ["Air Conditioner", "Fan", "Light", "Washing Machine"]
)

power = st.toggle("Power ON / OFF")

mode = st.selectbox("Mode", ["Normal", "Eco", "Turbo"])

temp = st.slider("Temperature", 16, 30)

st.success(f"{device} updated successfully (Demo)")
