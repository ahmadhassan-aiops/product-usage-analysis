"""
What happened to product usage in January 2023? An interactive analysis by Ahmad Hassan.
All data ships with the app.
"""

import streamlit as st

st.set_page_config(
    page_title="Product usage analysis | Ahmad Hassan",
    page_icon=":material/monitoring:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from lib.ui import inject_css  # noqa: E402
from nav import PAGES  # noqa: E402

inject_css()
st.navigation(PAGES, position="top").run()
