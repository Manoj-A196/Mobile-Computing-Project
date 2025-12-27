import streamlit as st

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username and password:
        st.success("Login Successful (Demo)")
    else:
        st.error("Please enter all details")
