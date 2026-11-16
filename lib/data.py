"""Loads the prepared usage data and builds the monthly views used by every page."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent.parent / "data"
JAN23 = pd.Timestamp("2023-01-01")
JAN22 = pd.Timestamp("2022-01-01")
YEAR22 = (pd.Timestamp("2022-01-01"), pd.Timestamp("2022-12-01"))


@st.cache_data
def meta() -> dict:
    return json.loads((DATA / "meta.json").read_text(encoding="utf-8"))


@st.cache_data
def table(name: str) -> pd.DataFrame:
    return pd.read_parquet(DATA / f"{name}.parquet")


@st.cache_data
def usage() -> pd.DataFrame:
    return table("usage")


@st.cache_data
def monthly() -> pd.DataFrame:
    """Platform totals per month."""
    u = usage()
    m = u.groupby("month").agg(minutes=("minutes", "sum"), sessions=("sessions", "sum"),
                               customers=("customer", "nunique"), records=("date", "size")).reset_index()
    return m


@st.cache_data
def feature_monthly() -> pd.DataFrame:
    """Minutes per feature (columns) per month (rows)."""
    u = usage()
    return u.groupby(["month", "feature"])["minutes"].sum().unstack(fill_value=0)


@st.cache_data
def customer_monthly() -> pd.DataFrame:
    """Minutes per customer (rows) per month (columns), 0 where a customer had no activity."""
    u = usage()
    return u.groupby(["customer", "month"])["minutes"].sum().unstack(fill_value=0)


@st.cache_data
def drop_counts(threshold: float = 0.5) -> pd.Series:
    """For each month: how many customers used the product at least `threshold` less than their own previous
    12-month average. Shows how unusual January 2023 was."""
    c = customer_monthly()
    out = {}
    for i in range(12, c.shape[1]):
        base = c.iloc[:, i - 12:i].mean(axis=1)
        change = c.iloc[:, i] / base.where(base > 0) - 1
        out[c.columns[i]] = int((change < -threshold).sum())
    return pd.Series(out)
