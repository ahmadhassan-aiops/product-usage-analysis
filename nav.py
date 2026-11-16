"""Page registry, shared by app.py and pages that link to other pages."""

import streamlit as st

from views import customers, features, findings, method, trend

FINDINGS = st.Page(findings.render, title="Key findings", icon=":material/insights:", url_path="findings", default=True)
TREND = st.Page(trend.render, title="Usage over time", icon=":material/show_chart:", url_path="trend")
FEATURES = st.Page(features.render, title="Features", icon=":material/widgets:", url_path="features")
CUSTOMERS = st.Page(customers.render, title="Customers", icon=":material/group:", url_path="customers")
METHOD = st.Page(method.render, title="Data & method", icon=":material/dataset:", url_path="method")

PAGES = [FINDINGS, TREND, FEATURES, CUSTOMERS, METHOD]
