import streamlit as st

# Set config
st.set_page_config(page_title="Expense Tracker", layout="wide")

# Hide Streamlit UI elements
st.markdown("""
    <style>
        #MainMenu, header, footer, [data-testid="stSidebar"] {
            display: none;
        }
        .block-container {
            padding-top: 6rem;
        }
        .navbar-container {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
        }
        .navbar {
            display: flex;
            background: #f8f9fa;
            padding: 10px 16px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            gap: 20px;
        }
        .navbar button {
            border: none;
            background: #e9ecef;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            position: relative;
        }
        .navbar button:hover {
            transform: scale(1.2);
            background: #dee2e6;
        }
        .navbar button span {
            position: absolute;
            bottom: -22px;
            background: #343a40;
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            white-space: nowrap;
            opacity: 0;
            transition: opacity 0.2s;
        }
        .navbar button:hover span {
            opacity: 1;
        }
    </style>
""", unsafe_allow_html=True)

# Import display functions
from src.Home import show_home
from src.Tracking import show_tracking
from src.Summary import show_summary
from src.Download import show_download

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navbar UI
with st.container():
    st.markdown('<div class="navbar-container"><div class="navbar">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button("🏠", help="Home"):
            st.session_state.page = "home"
    with col2:
        if st.button("📊", help="Tracking"):
            st.session_state.page = "tracking"
    with col3:
        if st.button("📅", help="Summary"):
            st.session_state.page = "summary"
    with col4:
        if st.button("⬇️", help="Download"):
            st.session_state.page = "download"

    st.markdown('</div></div>', unsafe_allow_html=True)

# Route to selected page
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "tracking":
    show_tracking()
elif st.session_state.page == "summary":
    show_summary()
elif st.session_state.page == "download":
    show_download()
else:
    st.error("Page not found.")
