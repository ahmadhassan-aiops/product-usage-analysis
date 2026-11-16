"""Features: which feature drove the change, and when it started."""

import streamlit as st

from lib import charts, data
from lib.ui import chart, footer, header, insight, note, section


def render() -> None:
    f = data.feature_monthly()

    header("Features", "Which feature changed?",
           "The product has six features. Splitting the monthly total by feature shows where the lost minutes went.")

    section("What changed between January 2022 and January 2023", "Change in minutes, by feature.")
    yoy = (f.loc[data.JAN23] - f.loc[data.JAN22]).sort_values()
    chart(charts.bars(yoy.index, yoy.values, horizontal=True, highlight=(yoy.index == "Roadmap").tolist(),
                      customdata=(yoy / f.loc[data.JAN22]).values[:, None],
                      hover="<b>%{y}</b><br>%{x:+,.0f} minutes (%{customdata[0]:+.0%})",
                      xtitle="Change in minutes, Jan 2023 vs Jan 2022"))
    insight(f"The total fell by {-yoy.sum():,.0f} minutes. <b>Roadmap alone lost {-yoy['Roadmap']:,.0f}</b> "
            f"({yoy['Roadmap'] / f.loc[data.JAN22, 'Roadmap']:+.0%}), about {yoy['Roadmap'] / yoy.sum():.0%} of the "
            "drop. Automation changed by only "
            f"{yoy['Automation']:+,.0f} minutes.")

    section("Feature usage month by month", "Pick up to three features to compare.")
    pick = st.multiselect("Features", list(f.columns), default=["Roadmap", "Reporting", "Automation"],
                          max_selections=3, key="feat")
    recent = f[f.index >= "2020-01-01"]
    if pick:
        chart(charts.lines(recent.index.strftime("%b %Y"), {p: recent[p].round(0) for p in pick}, hover_fmt=",.0f",
                           ytitle="Minutes per month", markers=False).update_xaxes(nticks=12))
    before = f.loc["2021-06-01":"2022-05-01", "Roadmap"].mean()
    after = f.loc["2022-06-01":"2023-01-01", "Roadmap"].mean()
    insight(f"Roadmap ran at about <b>{before:,.0f} minutes a month</b> until May 2022, then dropped to about "
            f"<b>{after:,.0f}</b> from June 2022 and stayed there. No other feature shows a break like this.")

    section("Average time per session", "Minutes per session, January 2023 against each feature's 2022 average.")
    u = data.usage()
    per = u.assign(per=u["minutes"] / u["sessions"]).groupby(["month", "feature"])["per"].mean().unstack()
    base = per.loc[data.YEAR22[0]:data.YEAR22[1]].mean()
    comp = (per.loc[data.JAN23] / base - 1).sort_values()
    chart(charts.bars(comp.index, comp.values, horizontal=True, highlight=(comp.index == "Roadmap").tolist(),
                      hover="<b>%{y}</b><br>%{x:+.0%} vs 2022 average", xtitle="Change in minutes per session")
          .update_xaxes(tickformat="+.0%"))
    insight("Measured per session, Roadmap again moves most. Account Management and Automation are also lower; "
            "Automation sessions have always been the shortest, and its January figure is within its normal "
            "month-to-month range.")
    note("The original notebook ranked features by their average time in January 2023 and concluded that "
         "Automation, the lowest, caused the decline. But Automation is the lowest-time feature in every month. "
         "Comparing each feature with its own history points to Roadmap instead.")

    footer()
