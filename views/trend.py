"""Usage over time: monthly totals, Januaries compared, year-on-year change."""

import streamlit as st

from lib import charts, data
from lib.ui import chart, footer, header, insight, section


def render() -> None:
    mon = data.monthly()
    labels = mon["month"].dt.strftime("%b %Y")

    header("Trend", "Usage over time",
           "Total minutes customers spent in the product each month, June 2017 to January 2023.")

    metric = st.segmented_control("Measure", ["Minutes", "Sessions", "Active customers"], default="Minutes",
                                  key="measure", label_visibility="collapsed") or "Minutes"
    col = {"Minutes": "minutes", "Sessions": "sessions", "Active customers": "customers"}[metric]

    section(f"{metric} per month", "January 2023 highlighted.")
    chart(charts.bars(labels, mon[col].values, highlight=(mon["month"] == data.JAN23).tolist(),
                      hover="%{x}<br><b>%{y:,.0f}</b>", ytitle=metric).update_xaxes(nticks=12))
    if col == "minutes":
        insight("Usage was steady at about 3,350-4,150 minutes a month from 2018 to May 2022, then <b>stepped down "
                "in June 2022</b> to around 2,950-3,350. January 2023 continues that lower level; it is not a sudden "
                "fall.")
    elif col == "sessions":
        insight("Sessions jump around from month to month (for example December 2022 is unusually low), so they "
                "are a noisier measure than minutes. They show no clear break in January 2023.")
    else:
        insight("The number of active customers stays between about 70 and 87 a month throughout; January 2023 (78) "
                "is normal. Fewer minutes did not come from fewer customers.")

    left, right = st.columns(2, gap="large")
    with left:
        section("Every January compared", "Minutes used in January of each year.")
        jan = mon[mon["month"].dt.month == 1]
        chart(charts.bars(jan["month"].dt.year.astype(str), jan["minutes"].values,
                          highlight=(jan["month"] == data.JAN23).tolist(),
                          text=[f"{v:,.0f}" for v in jan["minutes"]], hover="January %{x}<br><b>%{y:,.0f}</b> minutes",
                          ytitle="Minutes in January"))
        insight("January 2023 is the <b>lowest January in the data</b>, about 20% below the others, which all sit "
                "within a narrow band.")
    with right:
        section("Year-on-year change", "Each month against the same month a year earlier.")
        s = mon.set_index("month")["minutes"]
        yoy = (s / s.shift(12) - 1).dropna()
        yoy = yoy[yoy.index >= "2021-01-01"]
        chart(charts.bars(yoy.index.strftime("%b %y"), yoy.values, highlight=(yoy < -0.1).tolist(),
                          hover="%{x}<br><b>%{y:+.0%}</b> vs a year earlier", ytitle="Change vs same month last year")
              .update_yaxes(tickformat="+.0%"))
        insight("Highlighted months are more than 10% below the year before. They start in <b>June 2022</b>, not in "
                "January 2023.")

    footer()
