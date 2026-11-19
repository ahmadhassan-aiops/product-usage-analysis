"""Data & method: the usage logs, preparation, how each question was answered, limits."""

import pandas as pd
import streamlit as st

from lib import data
from lib.site import NOTEBOOK_URL
from lib.ui import footer, header, md, section


def render() -> None:
    m = data.meta()

    header(
        "Data & method",
        "How the analysis was done",
        "The data, the preparation, how each question was answered and the limits of the data. "
        f'The full Python work is in the <a href="{NOTEBOOK_URL}" target="_blank">notebook</a>.',
    )

    section("The data")
    md(f"**{m['raw_shape'][0]:,} records** from {m['first']} to {m['last']}: one row per customer, feature and day "
       f"of activity, for {m['customers']} customers and six features ({', '.join(m['features'])}).")
    st.table(pd.DataFrame([
        ("Date", "Day of activity"),
        ("Username", "Customer (replaced here by \"Customer 001\" style labels)"),
        ("Feature", "Which part of the product was used"),
        ("Sessions", "Number of sessions that day"),
        ("Time spent", "Minutes spent that day"),
        ("Average time spent", "Minutes per session (Time spent ÷ Sessions; verified)"),
    ], columns=["Column", "Meaning"]), hide_index=True, border="horizontal")
    with st.expander("Look at the data (50 random records)"):
        st.dataframe(data.table("sample_usage"), hide_index=True, height=300)

    section("Preparation")
    st.table(pd.DataFrame([
        ("Quality checks", f"{m['missing']} missing values, {m['duplicates']} duplicate rows", "Nothing to fix"),
        ("Usernames", "Personal-looking handles", "Replaced with neutral customer labels before publishing"),
        ("Feature name", "\"Account Managment\"", "Spelling corrected"),
        ("Fractional minutes", f"{m['fractional_minutes']} records have minutes with decimals", "Kept as they are"),
        ("Time", "Daily dates", "Summed per month, per feature and per customer"),
    ], columns=["Item", "What was found", "How it was handled"]), hide_index=True, border="horizontal")

    section("How each question was answered")
    st.table(pd.DataFrame([
        ("Was January 2023 a drop?", "Compared with every earlier January and with the same month a year before: lowest January in the data, "
         "about 20% down, but the fall started in June 2022"),
        ("Which customers?", "January vs the customer's own average month; checked against how many customers dip that far in a "
         "normal month. No unusual group"),
        ("Which feature?", "Each feature against its own history: Roadmap halved from June 2022 and explains about three quarters "
         "of the drop; Automation is always the lowest"),
    ], columns=["Question", "How it was answered, and the result"]), hide_index=True, border="horizontal")

    section("Limits of this data")
    md("- **What, not why.** The logs show Roadmap usage halving in June 2022 but not the reason; that needs "
       "release notes, support tickets or customer interviews.\n"
       "- **Sparse per customer.** One or two records per customer per month make individual trends noisy.\n"
       "- **Usage, not revenue or churn.** The data can't say whether lower usage led to cancellations.")

    section("How this app is built")
    md("Python, pandas and Plotly in a Streamlit app. `build_data.py` anonymises the CSV and saves it as a Parquet "
       f"file that ships with the app. Data built on {m['built']}.")

    footer()
