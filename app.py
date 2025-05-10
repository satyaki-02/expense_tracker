import streamlit as st
from streamlit_option_menu import option_menu

# ✅ This must be the first Streamlit command
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

# ✅ Removed duplicate set_page_config

selected = option_menu(
    menu_title=None,
    options=["Home", "Tracking", "Summary"],
    icons=["house", "bar-chart", "wallet2"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

# Import only the necessary function when selected
if selected == "Home":
    from pages.Home import show_home
    show_home()
elif selected == "Tracking":
    from pages.Tracking import show_tracking
    show_tracking()
elif selected == "Summary":
    from pages.Summary import show_summary
    show_summary()
