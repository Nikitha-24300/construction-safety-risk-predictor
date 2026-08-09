"""Risk Patterns — historical pattern analysis."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import apply_filters, load_incidents
from utils.ui import RISK_COLORS, page_header

df, demo = load_incidents()

page_header(
    "Risk Patterns",
    "How historical incident data shapes the model's view of recurring risk",
)
if demo:
    st.warning("Demo Mode — using synthetic demonstration data.", icon="⚠️")

with st.expander("Filters", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    f_act = c1.multiselect("Activity", sorted(df["activity"].unique()))
    f_loc = c2.multiselect("Location type", sorted(df["location_type"].unique()))
    f_sev = c3.multiselect("Severity", ["Low", "Medium", "High"])
    f_shift = c4.multiselect("Shift", sorted(df["shift"].unique()))
    dmin, dmax = df["date"].min().date(), df["date"].max().date()
    f_dates = st.date_input("Time period", (dmin, dmax), min_value=dmin, max_value=dmax)
    grain = st.radio("Time grain", ["Day", "Week", "Month"], index=2, horizontal=True)

fdf = apply_filters(df, f_act, f_loc, f_sev, f_shift, f_dates if isinstance(f_dates, tuple) else None)
if fdf.empty:
    st.warning("No records match the selected filters.")
    st.stop()

c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='csrp-section'>Risk by activity</div>", unsafe_allow_html=True)
    d = fdf.groupby(["activity", "risk_level"]).size().reset_index(name="Records")
    fig = px.bar(d, x="activity", y="Records", color="risk_level", barmode="group",
                 color_discrete_map=RISK_COLORS,
                 category_orders={"risk_level": ["LOW", "MEDIUM", "HIGH"]})
    fig.update_layout(height=330, xaxis_title="", legend_title="Risk level",
                      margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("<div class='csrp-section'>Incidents by severity</div>", unsafe_allow_html=True)
    sev = fdf["severity"].value_counts().reindex(["Low", "Medium", "High"]).fillna(0).reset_index()
    sev.columns = ["Severity", "Records"]
    fig = px.bar(sev, x="Severity", y="Records", color="Severity", text="Records",
                 color_discrete_map={"Low": RISK_COLORS["LOW"], "Medium": RISK_COLORS["MEDIUM"],
                                     "High": RISK_COLORS["HIGH"]})
    fig.update_layout(height=330, showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='csrp-section'>Incidents over time</div>", unsafe_allow_html=True)
freq = {"Day": "D", "Week": "W", "Month": "MS"}[grain]
ts = fdf.set_index("date").resample(freq).size().reset_index(name="Incidents")
fig = px.line(ts, x="date", y="Incidents", markers=grain != "Day")
fig.update_traces(line_color="#1F4E79")
fig.update_layout(height=320, xaxis_title="", margin=dict(t=10, b=10, l=10, r=10))
st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown("<div class='csrp-section'>Risk by location type</div>", unsafe_allow_html=True)
    d = fdf.groupby(["location_type", "risk_level"]).size().reset_index(name="Records")
    fig = px.bar(d, x="location_type", y="Records", color="risk_level", barmode="stack",
                 color_discrete_map=RISK_COLORS,
                 category_orders={"risk_level": ["LOW", "MEDIUM", "HIGH"]})
    fig.update_layout(height=320, xaxis_title="", legend_title="Risk level",
                      margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.markdown("<div class='csrp-section'>Risk by shift</div>", unsafe_allow_html=True)
    d = fdf.groupby(["shift", "risk_level"]).size().reset_index(name="Records")
    fig = px.bar(d, x="shift", y="Records", color="risk_level", barmode="group",
                 color_discrete_map=RISK_COLORS,
                 category_orders={"risk_level": ["LOW", "MEDIUM", "HIGH"]})
    fig.update_layout(height=320, xaxis_title="", legend_title="Risk level",
                      margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='csrp-section'>Recurring hazards</div>", unsafe_allow_html=True)
rows = []
for hazard, count in fdf["primary_hazard"].value_counts().items():
    subset = fdf[fdf["primary_hazard"] == hazard]
    share_high = (subset["risk_level"] == "HIGH").mean()
    rows.append(
        {
            "Hazard": hazard,
            "Incident count": int(count),
            "Risk association": "High" if share_high >= 0.30 else "Medium",
            "Share high-risk": f"{share_high:.0%}",
        }
    )
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
