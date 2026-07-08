import streamlit as st
from auth.token import make_token, verify_token


# call at the top of every protected page:
# restores login from the signed url token on refresh, bounces to login
# if absent/invalid, and re-attaches the token to the url so it survives
# switch_page navigation and page refreshes
def require_login():
    if not st.session_state.get("logged_in"):
        username = verify_token(st.query_params.get("auth", ""))
        if username:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.switch_page("main.py")

    # st.switch_page drops query params, so put the token back in the url
    if "auth" not in st.query_params:
        st.query_params["auth"] = make_token(st.session_state.get("username", "admin"))
