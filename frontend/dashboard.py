import os

import pandas as pd
import requests
import streamlit as st


API_URL = os.getenv(
    "CINEOPS_API_URL",
    "http://127.0.0.1:8000/analyze",
)

st.set_page_config(
    page_title="CineOps",
    layout="wide",
)

st.title("🎬 CineOps — Agentic Production Control Room")

st.caption(
    "Gemini-powered multi-agent production analytics "
    "for film and media operations"
)

st.markdown(
    "Operational intelligence for production teams — combining "
    "schedule, budget, and executive decision agents."
)


if st.button("Analyze Production", type="primary"):
    result = None

    try:
        with st.spinner("Analyzing production data..."):
            response = requests.post(
                API_URL,
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()

    except requests.exceptions.Timeout:
        st.error("Unable to complete production analysis.")
        st.info("The analysis took too long. Please try again.")

    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the CineOps backend.")
        st.info("Please verify that the API is running and try again.")

    except requests.exceptions.HTTPError:
        st.error("Unable to complete production analysis.")
        st.info(
            f"The backend returned status code "
            f"{response.status_code}. Please try again."
        )

    except requests.exceptions.RequestException:
        st.error("Unable to complete production analysis.")
        st.info("A network error occurred. Please try again.")

    except ValueError:
        st.error("Unable to read the production analysis.")
        st.info("The backend returned an invalid response.")

    if result is not None:
        try:
            # -------------------------
            # KPI CARDS
            # -------------------------

            st.subheader("Production Health")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Primary Constraint",
                    result["primary_constraint"],
                )

            with col2:
                st.metric(
                    "Completion Rate",
                    f'{result["schedule_kpis"]["completion_rate"]}%',
                )

            with col3:
                st.metric(
                    "Schedule Pressure",
                    result["time_pressure_score"],
                )

            with col4:
                st.metric(
                    "Budget Pressure",
                    result["budget_pressure_score"],
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

            st.subheader("Executive Decision")

            executive = result["executive_agent"]

            if executive["overall_risk"] == "HIGH":
                st.error(
                    f'OVERALL RISK: {executive["overall_risk"]}'
                )
            elif executive["overall_risk"] == "MEDIUM":
                st.warning(
                    f'OVERALL RISK: {executive["overall_risk"]}'
                )
            else:
                st.success(
                    f'OVERALL RISK: {executive["overall_risk"]}'
                )

            with st.container(border=True):
                st.markdown("### Priority Action")
                st.markdown(
                    f"**{executive['priority_action']}**"
                )

                st.markdown("### Executive Summary")
                st.write(executive["executive_summary"])

                confidence = executive["confidence"]

                st.markdown("### Confidence")
                st.write(
                    f'**{confidence["level"]}** — '
                    f'{confidence["reason"]}'
                )

            st.divider()

            # -------------------------
            # PRODUCTION TREND
            # -------------------------

            reports = pd.DataFrame(result["recent_reports"])

            required_columns = {
                "report_date",
                "scenes_scheduled",
                "scenes_completed",
            }

            if (
                not reports.empty
                and required_columns.issubset(reports.columns)
            ):
                reports["report_date"] = pd.to_datetime(
                    reports["report_date"]
                )
                reports = reports.sort_values("report_date")

                reports["scenes_scheduled"] = pd.to_numeric(
                    reports["scenes_scheduled"],
                    errors="coerce",
                ).fillna(0)

                reports["scenes_completed"] = pd.to_numeric(
                    reports["scenes_completed"],
                    errors="coerce",
                ).fillna(0)

                reports["Cumulative Scheduled"] = (
                    reports["scenes_scheduled"].cumsum()
                )

                reports["Cumulative Completed"] = (
                    reports["scenes_completed"].cumsum()
                )

                trend_data = reports.set_index("report_date")[
                    [
                        "Cumulative Scheduled",
                        "Cumulative Completed",
                    ]
                ]

                st.subheader("Production Progress Trend")
                st.caption(
                    "Planned versus completed scenes "
                    "during the current analysis window."
                )

                st.line_chart(trend_data)

        except (KeyError, TypeError):
            st.error("Unable to display the production analysis.")
            st.info(
                "The backend response is missing required data."
            )