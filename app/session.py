import streamlit as st

 
# Handles session persistence across page refreshes.
# Uses query params to restore login state on refresh.
# Call this at the top of every page.
def apply_session():
    # Save session to query params on every render
    if st.session_state.get("logged_in"):
        st.query_params["auth"] = "true"
        st.query_params["user"] = st.session_state.get("username", "admin")

    # Restore session from query params on refresh
    elif st.query_params.get("auth") == "true":
        st.session_state["logged_in"] = True
        st.session_state["username"]  = st.query_params.get("user", "admin")

    # Not logged in — redirect to login
    else:
        st.switch_page("main.py")