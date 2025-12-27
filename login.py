import streamlit as st

def show():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.success("Login successful (Demo)")
            st.rerun()
        else:
            st.error("Please enter username and password")
