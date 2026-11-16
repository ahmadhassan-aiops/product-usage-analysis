"""Customers: were particular customers behind January 2023, or is per-customer variation normal?"""

import pandas as pd
import streamlit as st

from lib import charts, data
from lib.ui import cap, chart, footer, header, insight, note, section


def render() -> None:
    c = data.customer_monthly()

    header("Customers", "Did particular customers drive the drop?",
           "Each customer's January 2023 usage compared with their own average month in 2022.")

    base = c.loc[:, data.YEAR22[0]:data.YEAR22[1]].mean(axis=1)
    jan = c[data.JAN23]
    change = (jan / base.where(base > 0) - 1).dropna()

    section("January 2023 vs each customer's 2022 average", "Customers grouped by how much their usage changed.")
    bins = [-1.01, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 1, 100]
    names = ["-75% or more", "-50 to -75%", "-25 to -50%", "-25 to 0%", "0 to +25%", "+25 to +50%", "+50 to +100%",
             "More than doubled"]
    grp = pd.cut(change, bins, labels=names).value_counts().reindex(names)
    chart(charts.bars(names, grp.values, highlight=[i < 2 for i in range(len(names))],
                      hover="%{x}<br><b>%{y}</b> customers", ytitle="Customers"))
    insight(f"<b>{(change < -0.5).sum()} customers</b> used the product less than half as much as their 2022 "
            f"average, {(jan == 0).sum()} of them not at all. But {(change > 0.5).sum()} used it more than 50% more. "
            "Individual customers swing a lot from month to month.")

    section("Is that unusual?", "Customers below half their previous-12-month average, every month.")
    drops = data.drop_counts()
    drops = drops[drops.index >= "2019-01-01"]
    chart(charts.bars(drops.index.strftime("%b %Y"), drops.values, highlight=(drops.index == data.JAN23).tolist(),
                      hover="%{x}<br><b>%{y}</b> customers far below their usual level", ytitle="Customers")
          .update_xaxes(nticks=12))
    insight(f"In a typical month about <b>{drops.median():.0f}</b> customers are this far below their usual level; "
            f"January 2023 had {drops.loc[data.JAN23]}. There is <b>no unusual group of customers</b> behind January: "
            "each customer has only one or two records a month, so big individual swings are normal.")
    note("The original notebook flagged eight \"significant drop\" customers by comparing their whole-January total "
         "with their average for a single day's record in earlier years. That compares a month with a day, so the "
         "list mostly shows customers who happened to be quiet in January.")

    section("Look up a customer", "Monthly minutes for one customer.")
    who = st.selectbox("Customer", list(c.index), index=0, key="who")
    s = c.loc[who]
    s = s[s.index >= "2021-01-01"]
    chart(charts.bars(s.index.strftime("%b %y"), s.values, highlight=(s.index == data.JAN23).tolist(),
                      hover="%{x}<br><b>%{y:,.0f}</b> minutes", ytitle="Minutes"))
    cap("Customer labels replace the original usernames.")

    footer()
