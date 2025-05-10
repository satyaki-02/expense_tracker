import streamlit as st

def apply_custom_theme():
    theme = st.session_state.get("theme_mode", "light")

    if theme == "dark":
        st.markdown("""
            <style>
                body {
                    background-color: #0e1117;
                    color: white;
                }
                .stApp {
                    background-color: #0e1117;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body {
                    background-color: white;
                    color: black;
                }
                .stApp {
                    background-color: white;
                }
            </style>
        """, unsafe_allow_html=True)

def theme_toggle():
    mode = st.sidebar.radio("🌓 Theme", ["light", "dark"])
    st.session_state["theme_mode"] = mode
    apply_custom_theme()
