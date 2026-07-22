import os
import json

import pandas as pd
import streamlit as st

from src.transcription import transcribe_audio
from src.diarization import assign_speaker_labels
from src.llm_analysis import analyze_call_with_llm

from src.database import (
    save_call_analysis,
    get_all_calls,
    get_total_calls,
    get_average_score,
    get_best_advisor,
    get_category_averages,
    get_advisor_performance
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FitNova AI Call Intelligence",
    page_icon="📞",
    layout="wide"
)


# ============================================================
# AUTHENTICATION CONFIGURATION
# ============================================================

USERNAME = "admin"
PASSWORD = "fitnova123"


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.title(
        "📞 FitNova AI Call Intelligence"
    )

    st.subheader(
        "🔐 Login to Continue"
    )

    st.write(
        "Please enter your credentials to access "
        "the FitNova AI Call Intelligence Platform."
    )

    st.divider()

    login_col1, login_col2, login_col3 = st.columns(
        [1, 2, 1]
    )

    with login_col2:

        username = st.text_input(
            "👤 Username"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        if st.button(
            "🚀 Login",
            type="primary",
            use_container_width=True
        ):

            if (
                username == USERNAME
                and password == PASSWORD
            ):

                st.session_state.logged_in = True

                st.success(
                    "✅ Login successful!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )

    st.info(
        "Demo Login: Username: admin | Password: fitnova123"
    )

    st.stop()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title(
    "📞 FitNova AI"
)

st.sidebar.write(
    "AI Call Intelligence Platform"
)

st.sidebar.divider()


st.sidebar.success(
    "🟢 Logged in as Admin"
)


if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False

    st.rerun()


st.sidebar.divider()


page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Dashboard",

        "📞 Analyze New Call",

        "👥 Advisor Performance",

        "📋 Call History"

    ]

)


st.sidebar.divider()


st.sidebar.info(

    "FitNova AI Call Intelligence\n\n"
    "Analyze calls, evaluate advisors, "
    "and generate AI-powered insights."

)


# ============================================================
# HEADER
# ============================================================

st.title(
    "📞 FitNova AI Call Intelligence"
)


st.write(

    "AI-powered sales call analysis for evaluating "
    "advisor performance, detecting issues, and "
    "generating actionable insights."

)


# ============================================================
# DASHBOARD PAGE
# ============================================================

if page == "🏠 Dashboard":

    st.header(
        "📊 Performance Dashboard"
    )

    try:

        total_calls = get_total_calls()

        average_score = get_average_score()

        best_advisor = get_best_advisor()

        category_averages = (
            get_category_averages()
        )

    except Exception as error:

        st.error(
            f"❌ Failed to load dashboard analytics: {error}"
        )

        total_calls = 0

        average_score = 0

        best_advisor = None

        category_averages = {

            "needs_discovery": 0,

            "product_knowledge": 0,

            "objection_handling": 0,

            "compliance": 0,

            "next_step_booking": 0

        }

    kpi_col1, kpi_col2, kpi_col3 = (
        st.columns(3)
    )

    with kpi_col1:

        st.metric(
            "📞 Total Calls Analyzed",
            total_calls
        )

    with kpi_col2:

        st.metric(
            "⭐ Average Score",
            f"{average_score}/100"
        )

    with kpi_col3:

        if best_advisor is not None:

            st.metric(
                "🏆 Best Advisor",
                best_advisor[0],
                f"{best_advisor[1]}/100"
            )

        else:

            st.metric(
                "🏆 Best Advisor",
                "No data"
            )

    st.divider()

    st.subheader(
        "📊 Average Category Performance"
    )

    category_data = {

        "Category": [

            "Needs Discovery",

            "Product Knowledge",

            "Objection Handling",

            "Compliance",

            "Next Step Booking"

        ],

        "Average Score": [

            category_averages[
                "needs_discovery"
            ],

            category_averages[
                "product_knowledge"
            ],

            category_averages[
                "objection_handling"
            ],

            category_averages[
                "compliance"
            ],

            category_averages[
                "next_step_booking"
            ]

        ]

    }

    category_dataframe = pd.DataFrame(
        category_data
    )

    st.bar_chart(

        category_dataframe.set_index(
            "Category"
        )

    )

    st.success(

        "Use the sidebar to navigate through "
        "the FitNova AI platform."

    )


# ============================================================
# ANALYZE NEW CALL PAGE
# ============================================================

elif page == "📞 Analyze New Call":

    st.header(
        "📞 Analyze New Call"
    )

    st.subheader(
        "📋 Call Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        advisor_name = st.text_input(
            "Advisor Name",
            placeholder="Enter advisor name"
        )

    with col2:

        team_name = st.text_input(
            "Team Name",
            placeholder="Enter team name"
        )

    st.subheader(
        "🎙️ Upload Call Recording"
    )

    audio_file = st.file_uploader(

        "Upload an audio recording",

        type=[

            "mp3",

            "wav",

            "m4a",

            "ogg"

        ],

        help="Supported formats: MP3, WAV, M4A, OGG"

    )

    if st.button(

        "🚀 Analyze Call",

        type="primary",

        use_container_width=True

    ):

        if audio_file is None:

            st.warning(
                "Please upload a call recording first."
            )

        elif advisor_name.strip() == "":

            st.warning(
                "Please enter the advisor name."
            )

        elif team_name.strip() == "":

            st.warning(
                "Please enter the team name."
            )

        else:

            st.success(
                "✅ Call received successfully!"
            )

            st.subheader(
                "📋 Call Details"
            )

            st.write(
                f"**Advisor:** {advisor_name}"
            )

            st.write(
                f"**Team:** {team_name}"
            )

            st.write(
                f"**Audio File:** {audio_file.name}"
            )

            os.makedirs(
                "data",
                exist_ok=True
            )

            audio_file_path = os.path.join(

                "data",

                audio_file.name

            )

            with open(

                audio_file_path,

                "wb"

            ) as file:

                file.write(
                    audio_file.getbuffer()
                )

            with st.spinner(
                "🎙️ Transcribing audio..."
            ):

                transcript = transcribe_audio(
                    audio_file_path
                )

            st.success(
                "✅ Transcription completed!"
            )

            with st.spinner(
                "👥 Identifying speakers..."
            ):

                labeled_transcript = (
                    assign_speaker_labels(
                        transcript
                    )
                )

            st.success(
                "✅ Speaker labeling completed!"
            )

            st.subheader(
                "📝 Speaker-Labeled Transcript"
            )

            for segment in labeled_transcript:

                start_time = segment.get(
                    "start",
                    0
                )

                end_time = segment.get(
                    "end",
                    0
                )

                speaker = segment.get(
                    "speaker",
                    "Unknown"
                )

                text = segment.get(
                    "text",
                    ""
                )

                st.markdown(

                    f"**[{start_time:.2f}s - "
                    f"{end_time:.2f}s] "
                    f"{speaker}:** {text}"

                )

            try:

                with st.spinner(
                    "🤖 Gemini is analyzing the call..."
                ):

                    analysis_result = (
                        analyze_call_with_llm(
                            labeled_transcript
                        )
                    )

                st.success(
                    "✅ AI call analysis completed!"
                )

            except RuntimeError as error:

                st.error(
                    f"❌ AI analysis failed: {error}"
                )

                st.info(
                    "Please wait a few minutes and try again."
                )

                st.stop()

            try:

                save_call_analysis(

                    advisor=advisor_name,

                    team=team_name,

                    audio_file=audio_file.name,

                    analysis_result=analysis_result

                )

                st.success(
                    "💾 Call analysis saved to database!"
                )

            except Exception as error:

                st.error(
                    f"❌ Failed to save call analysis: {error}"
                )

            st.divider()

            st.header(
                "📊 Call Analysis"
            )

            st.metric(

                "Overall Score",

                f"{analysis_result.overall_score}/100"

            )

            st.subheader(
                "📈 Category Scores"
            )

            category_scores = (
                analysis_result.category_scores
            )

            score_col1, score_col2, score_col3 = (
                st.columns(3)
            )

            with score_col1:

                st.metric(
                    "Needs Discovery",
                    f"{category_scores.needs_discovery}/20"
                )

                st.metric(
                    "Product Knowledge",
                    f"{category_scores.product_knowledge}/20"
                )

            with score_col2:

                st.metric(
                    "Objection Handling",
                    f"{category_scores.objection_handling}/20"
                )

                st.metric(
                    "Compliance",
                    f"{category_scores.compliance}/20"
                )

            with score_col3:

                st.metric(
                    "Next Step Booking",
                    f"{category_scores.next_step_booking}/20"
                )

            st.subheader(
                "📝 AI Summary"
            )

            st.info(
                analysis_result.summary
            )

            st.subheader(
                "💪 Strengths"
            )

            if len(
                analysis_result.strengths
            ) == 0:

                st.info(
                    "No specific strengths identified."
                )

            else:

                for strength in (
                    analysis_result.strengths
                ):

                    st.success(
                        f"✅ {strength}"
                    )

            st.subheader(
                "⚠️ Detected Issues"
            )

            if len(
                analysis_result.issues
            ) == 0:

                st.success(
                    "No issues detected."
                )

            else:

                for issue in (
                    analysis_result.issues
                ):

                    with st.expander(

                        f"{issue.severity} - "
                        f"{issue.issue_type}"

                    ):

                        st.write(
                            f"**Timestamp:** "
                            f"{issue.timestamp}"
                        )

                        st.write(
                            f"**Exact Quote:** "
                            f"{issue.quote}"
                        )

                        st.write(
                            f"**Reason:** "
                            f"{issue.reason}"
                        )

                        st.write(
                            f"**Recommendation:** "
                            f"{issue.recommendation}"
                        )

            st.subheader(
                "🎯 Recommended Action Items"
            )

            if len(
                analysis_result.action_items
            ) == 0:

                st.success(
                    "No immediate action items."
                )

            else:

                for action_item in (
                    analysis_result.action_items
                ):

                    st.warning(
                        f"➡️ {action_item}"
                    )


# ============================================================
# ADVISOR PERFORMANCE PAGE
# ============================================================

elif page == "👥 Advisor Performance":

    st.header(
        "👥 Advisor Performance"
    )

    try:

        advisor_performance = (
            get_advisor_performance()
        )

    except Exception as error:

        st.error(
            f"❌ Failed to load advisor performance: {error}"
        )

        advisor_performance = []

    if len(
        advisor_performance
    ) == 0:

        st.info(
            "No advisor performance data available."
        )

    else:

        advisor_dataframe = pd.DataFrame(
            advisor_performance
        )

        advisor_dataframe.index = (
            advisor_dataframe.index + 1
        )

        advisor_dataframe.index.name = "Rank"

        advisor_dataframe = (
            advisor_dataframe.rename(

                columns={

                    "advisor": "Advisor",

                    "average_score": "Average Score",

                    "total_calls": "Total Calls"

                }

            )
        )

        st.dataframe(
            advisor_dataframe,
            use_container_width=True
        )

        st.subheader(
            "📊 Advisor Average Scores"
        )

        advisor_chart_data = (

            advisor_dataframe[

                [

                    "Advisor",

                    "Average Score"

                ]

            ]

            .set_index(
                "Advisor"
            )

        )

        st.bar_chart(
            advisor_chart_data
        )


# ============================================================
# CALL HISTORY PAGE
# ============================================================

elif page == "📋 Call History":

    st.header(
        "📋 Call History"
    )

    try:

        calls = get_all_calls()

    except Exception as error:

        st.error(
            f"❌ Failed to load call history: {error}"
        )

        calls = []

    if len(calls) == 0:

        st.info(
            "No previous call analyses found."
        )

    else:

        st.write(
            f"Total Calls Analyzed: {len(calls)}"
        )

        st.subheader(
            "🔍 Filter Call History"
        )

        advisors = sorted(

            list(

                set(

                    call[1]

                    for call in calls

                )

            )

        )

        teams = sorted(

            list(

                set(

                    call[2]

                    for call in calls

                )

            )

        )

        filter_col1, filter_col2, filter_col3 = (
            st.columns(3)
        )

        with filter_col1:

            selected_advisor = st.selectbox(

                "👤 Advisor",

                options=[

                    "All Advisors"

                ] + advisors

            )

        with filter_col2:

            selected_team = st.selectbox(

                "👥 Team",

                options=[

                    "All Teams"

                ] + teams

            )

        with filter_col3:

            minimum_score = st.slider(

                "🎯 Minimum Score",

                min_value=0,

                max_value=100,

                value=0,

                step=5

            )

        filtered_calls = []

        for call in calls:

            advisor = call[1]

            team = call[2]

            overall_score = call[4]

            advisor_matches = (

                selected_advisor == "All Advisors"

                or advisor == selected_advisor

            )

            team_matches = (

                selected_team == "All Teams"

                or team == selected_team

            )

            score_matches = (

                overall_score >= minimum_score

            )

            if (

                advisor_matches

                and team_matches

                and score_matches

            ):

                filtered_calls.append(
                    call
                )

        st.info(

            f"Showing "

            f"{len(filtered_calls)} "

            f"of "

            f"{len(calls)} "

            f"calls"

        )

        if len(filtered_calls) == 0:

            st.warning(
                "No calls match the selected filters."
            )

        else:

            for call in filtered_calls:

                call_id = call[0]

                advisor = call[1]

                team = call[2]

                audio_filename = call[3]

                overall_score = call[4]

                needs_discovery = call[5]

                product_knowledge = call[6]

                objection_handling = call[7]

                compliance = call[8]

                next_step_booking = call[9]

                summary = call[10]

                strengths_json = call[11]

                issues_json = call[12]

                action_items_json = call[13]

                created_at = call[14]

                with st.expander(

                    f"#{call_id} | "

                    f"{advisor} | "

                    f"{team} | "

                    f"{overall_score}/100"

                ):

                    st.write(
                        f"**Advisor:** {advisor}"
                    )

                    st.write(
                        f"**Team:** {team}"
                    )

                    st.write(
                        f"**Audio File:** {audio_filename}"
                    )

                    st.write(
                        f"**Analyzed At:** {created_at}"
                    )

                    st.divider()

                    st.subheader(
                        "📊 Overall Score"
                    )

                    st.metric(
                        "Overall Score",
                        f"{overall_score}/100"
                    )

                    st.subheader(
                        "📈 Category Scores"
                    )

                    history_col1, history_col2, history_col3 = (
                        st.columns(3)
                    )

                    with history_col1:

                        st.metric(
                            "Needs Discovery",
                            f"{needs_discovery}/20"
                        )

                        st.metric(
                            "Product Knowledge",
                            f"{product_knowledge}/20"
                        )

                    with history_col2:

                        st.metric(
                            "Objection Handling",
                            f"{objection_handling}/20"
                        )

                        st.metric(
                            "Compliance",
                            f"{compliance}/20"
                        )

                    with history_col3:

                        st.metric(
                            "Next Step Booking",
                            f"{next_step_booking}/20"
                        )

                    st.subheader(
                        "📝 AI Summary"
                    )

                    st.info(
                        summary
                    )

                    st.subheader(
                        "💪 Strengths"
                    )

                    try:

                        strengths = json.loads(
                            strengths_json
                        )

                    except Exception:

                        strengths = []

                    if len(strengths) == 0:

                        st.info(
                            "No specific strengths identified."
                        )

                    else:

                        for strength in strengths:

                            st.success(
                                f"✅ {strength}"
                            )

                    st.subheader(
                        "⚠️ Detected Issues"
                    )

                    try:

                        issues = json.loads(
                            issues_json
                        )

                    except Exception:

                        issues = []

                    if len(issues) == 0:

                        st.success(
                            "No issues detected."
                        )

                    else:

                        for issue in issues:

                            with st.expander(

                                f"{issue.get('severity', 'Unknown')} - "

                                f"{issue.get('issue_type', 'Unknown')}"

                            ):

                                st.write(

                                    f"**Timestamp:** "

                                    f"{issue.get('timestamp', '')}"

                                )

                                st.write(

                                    f"**Exact Quote:** "

                                    f"{issue.get('quote', '')}"

                                )

                                st.write(

                                    f"**Reason:** "

                                    f"{issue.get('reason', '')}"

                                )

                                st.write(

                                    f"**Recommendation:** "

                                    f"{issue.get('recommendation', '')}"

                                )

                    st.subheader(
                        "🎯 Recommended Action Items"
                    )

                    try:

                        action_items = json.loads(
                            action_items_json
                        )

                    except Exception:

                        action_items = []

                    if len(action_items) == 0:

                        st.success(
                            "No immediate action items."
                        )

                    else:

                        for action_item in action_items:

                            st.warning(
                                f"➡️ {action_item}"
                            )