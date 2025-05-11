import streamlit as st
from streamlit_option_menu import option_menu
from pages.Tracking import show_tracking
from pages.Download import show_download

st.set_page_config(page_title="Expense Tracker", layout="wide")

# Hide sidebar
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["Home", "Tracking", "Summary", 'Download Expense'],
    icons=["house", "bar-chart", "wallet2", 'download'],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

try:
    # Import only the necessary function when selected
    if selected == "Home":
        from pages.Home import show_home
        show_home()
    elif selected == "Tracking":
        show_tracking()
    elif selected == "Summary":
        from pages.Summary import show_summary
        show_summary()
    elif selected == "Download Expense":
        show_download()
except ImportError as e:
    st.error(f"Error importing page: {e}")
