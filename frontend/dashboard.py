import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="CineOps",
    layout="wide"
)

st.title("🎬 CineOps — Agentic Production Control Room")

st.caption(
    "Gemini-powered multi-agent production analytics for film and media operations"
)

st.markdown(
    "Operational intelligence for production teams — combining schedule, budget, and executive decision agents."
)

if st.button("Analyze Production"):

    response = requests.post("http://127.0.0.1:8000/analyze")
    result = response.json()

    # -------------------------
    # KPI CARDS
    # -------------------------

    st.subheader("Production Health")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
     st.metric("Primary Constraint", result["primary_constraint"])

    with col2:
     st.metric(
        "Completion Rate",
        f'{result["schedule_kpis"]["completion_rate"]}%'
    )

    with col3:
     st.metric(
        "Schedule Pressure",
        result["time_pressure_score"]
    )

    with col4:
     st.metric(
        "Budget Pressure",
        result["budget_pressure_score"]
    )

    st.divider()

    # -------------------------
    # AGENT PANELS
    # -------------------------

    st.subheader("Agent Analysis")

    schedule_col, budget_col = st.columns(2)

    with schedule_col:
        st.markdown("### Schedule Agent")

        schedule = result["schedule_agent"]

        if schedule["risk"] == "HIGH":
            st.error(f'Risk: {schedule["risk"]}')
        elif schedule["risk"] == "MEDIUM":
            st.warning(f'Risk: {schedule["risk"]}')
        else:
            st.success(f'Risk: {schedule["risk"]}')

        st.write("**Finding**")
        st.write(schedule["finding"])

        st.write("**Recommended Action**")
        st.write(schedule["action"])

    with budget_col:
        st.markdown("### Budget Agent")

        budget = result["budget_agent"]

        if budget["risk"] == "HIGH":
            st.error(f'Risk: {budget["risk"]}')
        elif budget["risk"] == "MEDIUM":
            st.warning(f'Risk: {budget["risk"]}')
        else:
            st.success(f'Risk: {budget["risk"]}')

        st.write("**Finding**")
        st.write(budget["finding"])

        st.write("**Recommended Action**")
        st.write(budget["action"])

    st.divider()

    # -------------------------
    # EXECUTIVE PANEL
    # -------------------------


st.divider()

st.subheader("Executive Decision")

executive = result["executive_agent"]

if executive["overall_risk"] == "HIGH":
    st.error(f'OVERALL RISK: {executive["overall_risk"]}')
elif executive["overall_risk"] == "MEDIUM":
    st.warning(f'OVERALL RISK: {executive["overall_risk"]}')
else:
    st.success(f'OVERALL RISK: {executive["overall_risk"]}')

with st.container(border=True):

    st.markdown("### Priority Action")
    st.markdown(f"**{executive['priority_action']}**")

    st.markdown("### Executive Summary")
    st.write(executive["executive_summary"])

    confidence = executive["confidence"]

    st.markdown("### Confidence")
    st.write(
        f'**{confidence["level"]}** — {confidence["reason"]}'
    )