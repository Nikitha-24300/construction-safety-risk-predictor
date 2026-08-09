"""Dashboard — safety overview."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import apply_filters, load_incidents
from utils.ui import (
    APP_SUBTITLE,
    APP_TITLE,
    DISCLAIMER,
    RISK_COLORS,
    kpi_card,
    page_header,
)

df, demo = load_incidents()

page_header(APP_TITLE, APP_SUBTITLE)
st.info(DISCLAIMER, icon="ℹ️")
if demo:
    st.warning("Demo Mode — using synthetic demonstration data.", icon="⚠️")

with st.expander("Filters", expanded=False):
    c1, c2, c3, c4 = st.columns(4)
    f_act = c1.multiselect("Activity", sorted(df["activity"].unique()))
    f_loc = c2.multiselect("Location type", sorted(df["location_type"].unique()))
    f_sev = c3.multiselect("Severity", ["Low", "Medium", "High"])
    f_shift = c4.multiselect("Shift", sorted(df["shift"].unique()))
    dmin, dmax = df["date"].min().date(), df["date"].max().date()
    f_dates = st.date_input("Time period", (dmin, dmax), min_value=dmin, max_value=dmax)

fdf = apply_filters(df, f_act, f_loc, f_sev, f_shift, f_dates if isinstance(f_dates, tuple) else None)

if fdf.empty:
    st.warning("No records match the selected filters. Adjust the filters to see data.")
    st.stop()

counts = fdf["risk_level"].value_counts()
top_hazard = fdf["primary_hazard"].mode().iat[0] if "primary_hazard" in fdf else "n/a"

st.markdown("<div class='csrp-section'>Safety overview</div>", unsafe_allow_html=True)
k = st.columns(5)
with k[0]:
    kpi_card("Total incidents analysed", f"{len(fdf):,}", "Historical records in scope")
with k[1]:
    kpi_card("High-risk activities", f"{counts.get('HIGH', 0):,}", "Model-scored ≥ 70%")
with k[2]:
    kpi_card("Medium-risk activities", f"{counts.get('MEDIUM', 0):,}", "Model-scored 40–69%")
with k[3]:
    kpi_card("Low-risk activities", f"{counts.get('LOW', 0):,}", "Model-scored < 40%")
with k[4]:
    kpi_card("Most observed hazard", top_hazard, "Highest recurrence in scope")

st.write("")
left, right = st.columns([1, 1.4])

with left:
    st.markdown("<div class='csrp-section'>Risk distribution</div>", unsafe_allow_html=True)
    dist = (
        fdf["risk_level"].value_counts()
        .reindex(["LOW", "MEDIUM", "HIGH"]).fillna(0).reset_index()
    )
    dist.columns = ["Risk level", "Records"]
    fig = px.bar(
        dist, x="Risk level", y="Records", color="Risk level",
        color_discrete_map=RISK_COLORS, text="Records",
    )
    fig.update_layout(showlegend=False, height=340, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("<div class='csrp-section'>Risk by activity</div>", unsafe_allow_html=True)
    by_act = (
        fdf.groupby(["activity", "risk_level"]).size().reset_index(name="Records")
    )
    fig2 = px.bar(
        by_act, x="activity", y="Records", color="risk_level",
        color_discrete_map=RISK_COLORS, barmode="stack",
        category_orders={"risk_level": ["LOW", "MEDIUM", "HIGH"]},
    )
    fig2.update_layout(
        height=340, xaxis_title="", legend_title="Risk level",
        margin=dict(t=10, b=10, l=10, r=10),
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<div class='csrp-section'>Top recurring hazards</div>", unsafe_allow_html=True)
haz = fdf["primary_hazard"].value_counts().head(6).reset_index()
haz.columns = ["Hazard", "Occurrences"]
fig3 = px.bar(haz.sort_values("Occurrences"), x="Occurrences", y="Hazard", orientation="h")
fig3.update_traces(marker_color="#1F4E79")
fig3.update_layout(height=320, yaxis_title="", margin=dict(t=10, b=10, l=10, r=10))
st.plotly_chart(fig3, use_container_width=True)

st.markdown(
    "<div class='csrp-section'>Recent high-risk activity</div>", unsafe_allow_html=True
)