"""Landing page: the question, what the data really shows, and what to do about it."""

import plotly.graph_objects as go
import streamlit as st

from lib import charts, data
from lib.ui import cap, finding, footer, header, method_card, note, recommendations, spotlight


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
        chips=[("code", "Python, pandas"), ("show_chart", "Time series"), ("widgets", "6 features"),
               ("history", "2017 to 2023")],
    )

    k = st.columns(4)
    k[0].metric("Minutes used, Jan 2023", f"{j23:,.0f}", delta=f"{j23 / j22 - 1:+.0%} vs Jan 2022", border=True)
    k[1].metric(f"Januaries {prev_jans.index.min().year}-2022", f"{prev_jans.min() / 1000:,.1f}k-{prev_jans.max() / 1000:,.1f}k",
                border=True, help="Minutes used in each earlier January")
    k[2].metric("Roadmap minutes a month", f"{road_after:,.0f}", delta=f"{road_after / road_before - 1:+.0%} since June 2022",
                border=True)
    k[3].metric("Customers active, Jan 2023", f"{mon.loc[data.JAN23, 'customers']}", border=True)

    recent = f[f.index >= "2021-01-01"]
    x = recent.index.strftime("%b %Y")
    fig = go.Figure()
    for feat in [c for c in recent.columns if c != "Roadmap"] + ["Roadmap"]:
        hi = feat == "Roadmap"
        fig.add_trace(go.Scatter(
            x=x, y=recent[feat].round(0), name=feat, mode="lines",
            line=dict(color=charts.BLUE if hi else charts.QUIET, width=3.5 if hi else 1.8),
            hovertemplate=f"{feat}: %{{y:,.0f}} min<extra></extra>",
        ))
    fig.add_annotation(x=x[-1], y=recent["Roadmap"].iloc[-1], text="<b>Roadmap</b>", showarrow=False, xanchor="left",
                       xshift=8, font=dict(color=charts.BLUE, size=13))
    charts.style(fig, height=380)
    fig.update_layout(hovermode="x unified", margin=dict(r=90))
    fig.update_xaxes(nticks=10, showspikes=True, spikecolor=charts.AXIS, spikethickness=1)
    fig.update_yaxes(title="Minutes per month")
    charts.vline(fig, "Jun 2022", "June 2022: Roadmap halves")
    spotlight("One feature broke, seven months before anyone asked",
              f"Monthly minutes for the six features since 2021. <b>Roadmap</b> (teal) fell from about "
              f"{road_before:,.0f} to {road_after:,.0f} minutes a month in June 2022 and stayed there; the other five "
              "(grey) carried on as before.", fig, key="spot")

    st.subheader("Key findings", anchor=False)
    a = st.columns(3)
    finding(a[0], f"{j23 / j22 - 1:+.0%}", "January 2023 vs January 2022",
            "The drop is real, but only against last year",
            f"Every January from {prev_jans.index.min().year} to 2022 had {prev_jans.min():,.0f}-{prev_jans.max():,.0f} "
            f"minutes; January 2023 had {j23:,.0f}. Against December it is only "
            f"{j23 / mon.loc['2022-12-01', 'minutes'] - 1:+.0%}: usage had been sliding for months.",
            TREND, "Usage over time", card_icon="trending_down")
    finding(a[1], f"{road_share:.0%}", "of the year-on-year drop comes from one feature",
            "Roadmap lost half its usage in June 2022",
            f"Roadmap went from about {road_before:,.0f} minutes a month to about {road_after:,.0f} in June 2022 and "
            "never recovered. The other five features, Automation included, barely changed.",
            FEATURES, "Features", card_icon="map")
    finding(a[2], f"{drops.loc[data.JAN23]} vs {drops.median():.0f}", "customers far below their usual level: Jan 2023 vs a typical month",
            "No unusual group of customers",
            "In any month, about a third of customers use the product less than half as much as usual, because "
            "activity per customer is sparse. January 2023 was a normal month on this measure.",
            CUSTOMERS, "Customers", card_icon="group")

    st.subheader("What I would recommend", anchor=False)
    recommendations([
        ("search", "Investigate Roadmap in June 2022",
         "A release, a redesign, a pricing or permission change, or a competitor: that is where the lost usage is."),
        ("monitoring", "Watch usage feature by feature",
         "A break in one feature stayed hidden for <b>seven months</b> inside a total that looked roughly stable."),
        ("compare_arrows", "Compare with the same month last year",
         "As well as the month before, so seasonal highs like January are judged fairly."),
    ])
    cap("Usage data only: the logs say what changed and when, not why.")
    method_card("<b>How this was done.</b> Daily usage records were summed per month, per feature and per customer, "
                "and each month was compared with the same month a year earlier and with each customer's and "
                "feature's own history.", METHOD, tools=["pandas", "Plotly", "Year-on-year comparison", "Baselines per customer"])

    footer()
