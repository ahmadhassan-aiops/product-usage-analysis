"""Landing page: the question, what the data really shows, and what to do about it."""

import streamlit as st

from lib import data
from lib.ui import cap, finding, footer, header, md, note


def render() -> None:
    from nav import CUSTOMERS, FEATURES, METHOD, TREND

    m = data.meta()
    mon = data.monthly().set_index("month")
    f = data.feature_monthly()
    jan = mon.loc[mon.index.month == 1, "minutes"]
    j23, j22 = mon.loc[data.JAN23, "minutes"], mon.loc[data.JAN22, "minutes"]
    prev_jans = jan[jan.index < data.JAN23]
    yoy = f.loc[data.JAN23] - f.loc[data.JAN22]
    road_share = yoy["Roadmap"] / yoy.sum()
    road_before = f.loc["2021-06-01":"2022-05-01", "Roadmap"].mean()
    road_after = f.loc["2022-06-01":"2023-01-01", "Roadmap"].mean()
    drops = data.drop_counts()

    header(
        "Product analytics · Python, pandas",
        "What really happened to product usage in January 2023?",
        f"A software company saw usage look weak in January 2023 and asked why. Using {m['customers']} customers' "
        "daily usage of six product features since 2017, I checked whether the drop was real, when it started, "
        "and which feature and which customers were behind it.",
    )

    k = st.columns(4)
    k[0].metric("Minutes used, Jan 2023", f"{j23:,.0f}", delta=f"{j23 / j22 - 1:+.0%} vs Jan 2022", border=True)
    k[1].metric(f"Januaries {prev_jans.index.min().year}-2022", f"{prev_jans.min() / 1000:,.1f}k-{prev_jans.max() / 1000:,.1f}k",
                border=True, help="Minutes used in each earlier January")
    k[2].metric("Roadmap minutes a month", f"{road_after:,.0f}", delta=f"{road_after / road_before - 1:+.0%} since June 2022",
                border=True)
    k[3].metric("Customers active, Jan 2023", f"{mon.loc[data.JAN23, 'customers']}", border=True)

    st.subheader("Key findings", anchor=False)
    a = st.columns(3)
    finding(a[0], f"{j23 / j22 - 1:+.0%}", "January 2023 vs January 2022",
            "The drop is real, but only against last year",
            f"Every January from {prev_jans.index.min().year} to 2022 had {prev_jans.min():,.0f}-{prev_jans.max():,.0f} "
            f"minutes; January 2023 had {j23:,.0f}. Against December it is only "
            f"{j23 / mon.loc['2022-12-01', 'minutes'] - 1:+.0%}: usage had been sliding for months.",
            TREND, "Usage over time")
    finding(a[1], f"{road_share:.0%}", "of the year-on-year drop comes from one feature",
            "Roadmap lost half its usage in June 2022",
            f"Roadmap went from about {road_before:,.0f} minutes a month to about {road_after:,.0f} in June 2022 and "
            "never recovered. The other five features, Automation included, barely changed.",
            FEATURES, "Features")
    finding(a[2], f"{drops.loc[data.JAN23]} vs {drops.median():.0f}", "customers far below their usual level: Jan 2023 vs a typical month",
            "No unusual group of customers",
            "In any month, about a third of customers use the product less than half as much as usual, because "
            "activity per customer is sparse. January 2023 was a normal month on this measure.",
            CUSTOMERS, "Customers")

    st.subheader("What I would recommend", anchor=False)
    md("1. **Investigate what changed in Roadmap in June 2022**: a release, a redesign, a pricing or permission "
       "change, or a competitor. That is where the lost usage is.\n"
       "2. **Watch feature-level usage month by month**, not just the total: a break in one feature was hidden "
       "for seven months inside a total that looked roughly stable.\n"
       "3. **Compare each month with the same month last year** as well as the month before, so seasonal highs "
       "like January are judged fairly.")
    note("This re-analysis reaches a different conclusion from the original notebook, which pointed to the "
         "Automation feature and a list of eight customers. Data & method explains the difference.")
    cap("Usage data only: the logs say what changed and when, not why.")
    with st.container(border=True):
        md("**How this was done.** Daily usage records were summed per month, per feature and per customer, and "
           "each month was compared with the same month a year earlier and with each customer's and feature's own "
           "history.")
        st.page_link(METHOD, label="Data & method", icon=":material/arrow_forward:")

    footer()
