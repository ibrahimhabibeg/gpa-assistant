import os
import tempfile

import streamlit as st

from gpa_assist.algorithms import (
    calculate_max_possible_gpa,
    can_i_get_a_certain_rating,
    if_i_continue_with_a_certain_gpa_for_remaining_courses,
    max_achievable_rating,
    what_per_course_average_gpa_is_needed_for_rating,
    gpa_to_closest_letter_grade,
)
from gpa_assist.config import OverallRating
from gpa_assist.parser import parse_html_file


st.set_page_config(page_title="GPA Assistant", layout="wide")


QUESTION_MAX_GPA = "What is my maximum possible GPA?"
QUESTION_MAX_RATING = "What is the highest rating I can still achieve?"
QUESTION_CAN_REACH = "Can I still reach a specific rating?"
QUESTION_REQUIRED_AVERAGE = (
    "What average GPA do I need in remaining courses for a rating?"
)
QUESTION_HYPOTHETICAL_GPA = (
    "What will my final GPA be if I maintain a specific GPA in my remaining courses?"
)


def init_session_state() -> None:
    """Initialize all expected state keys once."""
    if "transcript" not in st.session_state:
        st.session_state.transcript = None
    if "program_hours" not in st.session_state:
        st.session_state.program_hours = 143.0
    if "non_gpa_hours" not in st.session_state:
        st.session_state.non_gpa_hours = 9.0
    if "uploaded_filename" not in st.session_state:
        st.session_state.uploaded_filename = ""
    if "selected_question" not in st.session_state:
        st.session_state.selected_question = QUESTION_MAX_GPA
    if "hypothetical_gpa" not in st.session_state:
        st.session_state.hypothetical_gpa = 3.50


def parse_uploaded_file(
    uploaded_file, program_hours: float, non_gpa_hours: float
) -> None:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name

        transcript = parse_html_file(
            tmp_path,
            program_total_hours=float(program_hours),
            non_gpa_hours=float(non_gpa_hours),
        )

        st.session_state.transcript = transcript
        st.session_state.program_hours = float(program_hours)
        st.session_state.non_gpa_hours = float(non_gpa_hours)
        st.session_state.uploaded_filename = uploaded_file.name
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


def get_overview_values() -> tuple[int, int, float]:
    transcript = st.session_state.transcript
    all_courses = transcript.get_all_courses()
    in_gpa_courses = [c for c in all_courses if c.counts_toward_gpa()]

    total_hours = sum(c.credit_hours for c in in_gpa_courses)
    total_quality_points = sum(c.get_grade_quality_points() for c in in_gpa_courses)
    current_gpa = total_quality_points / total_hours if total_hours > 0 else 0.0

    return len(transcript.semesters), len(all_courses), current_gpa


def format_rating(rating: OverallRating) -> str:
    return rating.value.replace("_", " ").title()


def render_max_possible_gpa_question(transcript) -> None:
    st.write(
        "This estimates your highest cumulative GPA assuming top performance ahead (4.0 GPA)."
    )
    max_gpa = calculate_max_possible_gpa(transcript)
    st.metric("Maximum Possible GPA:", f"{max_gpa:.2f}")
    if max_gpa >= 3.5:
        st.success("This ceiling can place you in the Excellent range.")
    elif max_gpa >= 3.0:
        st.info("This ceiling can place you in the Very Good range.")
    else:
        st.warning("Your GPA ceiling is below Very Good based on current data.")


def render_max_achievable_rating_question(transcript) -> None:
    st.write("This identifies the best overall academic rating you can still reach.")
    rating = max_achievable_rating(transcript)
    st.metric("Highest Achievable Rating:", format_rating(rating))

    if rating == OverallRating.EXCELLENT:
        st.success("You can still reach the Excellent range.")
    elif rating == OverallRating.VERY_GOOD:
        st.info("You can still reach the Very Good range.")
    elif rating == OverallRating.GOOD:
        st.info("You can still reach the Good range.")
    elif rating == OverallRating.ACCEPTED:
        st.warning("Your best reachable result is Accepted.")
    elif rating == OverallRating.WEAK:
        st.warning("Your best reachable result is Weak.")
    else:
        st.error("Your best reachable result is Too Weak.")


def render_can_reach_rating_question(transcript) -> None:
    rating_options = list(OverallRating)
    rating_label_map = {format_rating(r): r for r in rating_options}
    selected_label = st.selectbox(
        "Target rating",
        list(rating_label_map.keys()),
        key="select_target_can_reach",
    )
    target_rating = rating_label_map[selected_label]
    can_reach = can_i_get_a_certain_rating(transcript, target_rating)

    if can_reach:
        st.success(f"Reachable: {format_rating(target_rating)}")
    else:
        st.error(f"Not reachable: {format_rating(target_rating)}")


def render_required_average_question(transcript) -> None:
    rating_options = list(OverallRating)
    rating_label_map = {format_rating(r): r for r in rating_options}
    selected_label = st.selectbox(
        "Target rating",
        list(rating_label_map.keys()),
        key="select_target_required_avg",
    )
    target_rating = rating_label_map[selected_label]
    required_avg = what_per_course_average_gpa_is_needed_for_rating(
        transcript, target_rating
    )
    equivalent_letter_grade = (
        gpa_to_closest_letter_grade(required_avg) if required_avg is not None else "N/A"
    )

    if required_avg is None:
        st.warning("A required average could not be computed for this target.")
    else:
        cols = st.columns(2)
        with cols[0]:
            st.metric("Required Average GPA", f"{required_avg:.2f}")
        with cols[1]:
            st.metric("Equivalent Letter Grade", f"≈ {equivalent_letter_grade}")
        if required_avg > 4.0:
            st.error("The required average is above 4.00, so the target is impossible.")
        elif required_avg >= 3.5:
            st.info("This target requires consistently high performance.")
        else:
            st.success("This target appears achievable with steady performance.")


def render_hypothetical_gpa_question(transcript) -> None:
    st.write(
        "This estimates your final cumulative GPA if you maintain a chosen GPA for the remaining in-GPA courses."
    )

    hypothetical_gpa = st.number_input(
        "Hypothetical GPA for remaining in-GPA courses",
        min_value=0.0,
        max_value=4.0,
        step=0.05,
        value=3.50,
        key="hypothetical_gpa_input",
    )
    st.session_state.hypothetical_gpa = float(hypothetical_gpa)

    predicted_final_gpa = if_i_continue_with_a_certain_gpa_for_remaining_courses(
        transcript, st.session_state.hypothetical_gpa
    )

    st.metric("Predicted Final GPA", f"{predicted_final_gpa:.2f}")

    if predicted_final_gpa >= 3.5:
        st.success("This keeps you in a strong GPA range.")
    elif predicted_final_gpa >= 3.0:
        st.info("This keeps you in a solid GPA range.")
    elif predicted_final_gpa >= 2.0:
        st.warning("This GPA would be acceptable but still leaves room to improve.")
    else:
        st.error("This GPA would be low and may limit your overall outcome.")


def render_upload_section() -> None:
    st.subheader("Step 2: Upload Transcript")
    st.write(
        "Upload your Ibn Al-Haitham HTML export, then provide program requirements before parsing."
    )

    upload_col, settings_col = st.columns([3, 2])

    with upload_col:
        uploaded_file = st.file_uploader(
            "Ibn Al-Haitham HTML file",
            type=["html"],
            accept_multiple_files=False,
            key="file_uploader",
        )

    with settings_col:
        program_hours = st.number_input(
            "Program hours",
            min_value=1.0,
            step=1.0,
            value=float(st.session_state.program_hours),
            key="program_hours_input",
        )
        non_gpa_hours = st.number_input(
            "Non GPA hours",
            min_value=0.0,
            step=1.0,
            value=float(st.session_state.non_gpa_hours),
            key="non_gpa_hours_input",
        )

    st.session_state.program_hours = float(program_hours)
    st.session_state.non_gpa_hours = float(non_gpa_hours)
    if st.session_state.transcript is not None:
        st.session_state.transcript.program_total_hours = float(program_hours)
        st.session_state.transcript.non_gpa_hours = float(non_gpa_hours)

    parse_clicked = st.button(
        "Parse transcript",
        disabled=uploaded_file is None,
        width="stretch",
        type="primary",
        key="parse_transcript_button",
    )
    if parse_clicked and uploaded_file is not None:
        with st.spinner("Parsing transcript"):
            try:
                parse_uploaded_file(uploaded_file, program_hours, non_gpa_hours)
                st.success("Transcript parsed successfully.")
            except Exception as exc:
                st.error(f"Parsing failed: {exc}")


def render_question_section() -> None:
    if st.session_state.transcript is None:
        st.info("Parse a transcript first to start asking questions.")
        return

    st.subheader("Step 3: Ask a Question")
    st.caption(
        "Answers update automatically when you change a question or its related parameters."
    )
    semesters_count, courses_count, current_gpa = get_overview_values()

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Semesters", semesters_count)
    with metric_col2:
        st.metric("Courses", courses_count)
    with metric_col3:
        st.metric("Current GPA", f"{current_gpa:.2f}")

    st.selectbox(
        "Choose a predefined question",
        [
            QUESTION_MAX_GPA,
            QUESTION_MAX_RATING,
            QUESTION_CAN_REACH,
            QUESTION_REQUIRED_AVERAGE,
            QUESTION_HYPOTHETICAL_GPA,
        ],
        key="selected_question",
    )


def render_answer_section() -> None:
    if st.session_state.transcript is None:
        return

    st.subheader("Step 4: Get Answer")
    transcript = st.session_state.transcript
    question = st.session_state.selected_question

    try:
        if question == QUESTION_MAX_GPA:
            render_max_possible_gpa_question(transcript)
        elif question == QUESTION_MAX_RATING:
            render_max_achievable_rating_question(transcript)
        elif question == QUESTION_CAN_REACH:
            render_can_reach_rating_question(transcript)
        elif question == QUESTION_REQUIRED_AVERAGE:
            render_required_average_question(transcript)
        elif question == QUESTION_HYPOTHETICAL_GPA:
            render_hypothetical_gpa_question(transcript)
    except Exception as exc:
        st.error(f"Computation error: {exc}")


def render_project_info_section():
    st.title("Ibn Al-Haitham GPA Assistant")
    st.write("""
    This app is our submission for the course project for the course Software Requirements Engineering (SEN 302) at the Suez Canal University in the spring semester of 2026.    
    
    The code can be found on GitHub at [ibrahimhabibeg/gpa-assistant](https://github.com/ibrahimhabibeg/gpa-assistant).
    
    As a part of our submission, 
    [this](https://trello.com/b/THUbWFxZ/gpa-assistant) is the link to our Trello board and
    [this](https://gpaassistant.atlassian.net/jira/software/projects/KAN/boards/2?cloudId=c97a5841-2645-426a-819e-0bce433584d6&atlOrigin=eyJpIjoiZWQyMDkwMGM4OTBhNDFmMWEzYzIwNmUwZjBiZjZlMmUiLCJwIjoiaiJ9)
    is the link to our Jira board (Accessible only to project members and instructors).
    """)

    cols = st.columns(2)
    with cols[0]:
        st.subheader("Project Team")
        st.write("""
        - Ibrahim Habib
        - Zeyad Mohamed
        - Youssef Ahmed
        - Youssef Mahmoud
        - Mohamed Essam
        """)
    with cols[1]:
        st.subheader("Course Information")
        st.write("""
        - **Instructor**: Dr. Mohamed Mead
        - **Teaching Assistant**: Eng. Merhan Hisham
        - **Course**: Software Requirements Engineering (SEN 302)
        - **Program**: Software Engineering, Suez Canal University
        - **Semester**: Spring 2026
        """)

    expander = st.expander("Project Motivation and Overview", key="motivation_expander")

    with expander:
        st.subheader("Motivation and Project Overview")
        st.write("""
        University students usually have uncustomary questions regarding their academic performance and how it relates to their future goals.
        While many LMS provide basic GPA calculations, they are usually quite basic and don't answer the more complex questions students have and "what-if" scenarios they want to explore.
        Simply stated, these systems don't understand students' mind and the questions they have.
        
        To fix this gap, we decided to create a project that solves the real needs of students, an we have decided to tailor it specifically
        to our community.
        
        Most public universities in Egypt use an SIS called Ibn Al-Haitham. Since manually inputting data from the transcript is tedious and
        error-prone and there is no API or structured export format available, we decided to build a parser for the transcript page of our system.
        After uploading the transcript, students can chose from a set of relevant questions regarding their academic performance and future goals.
        
        The program assumes the rules and regulations of the Faculty of Computers and Information at Suez Canal University,
        but it is expected to be adaptable to other faculties and universities with similar grading systems and requirements with minimal adjustments.
        
        This project is open source and we encourage students at other universities using Ibn Al-Haitham to create forks with adjustments to fit their specific
        university rules.
        """)


def render_getting_started_section():
    st.subheader("Step 1: Getting the HTML File")
    st.write("""
    To get the HTML file of your transcript from Ibn Al-Haitham, follow these steps:
    1. Navigate to [https://myu.suez.edu.eg/](https://myu.suez.edu.eg/) and log in with your account.
    2. Go to the "Course Grades" page.
    3. Click CTRL+S (or CMD+S on Mac) to save the page.
    4. In the save dialog, choose "Web Page, Complete" as the format. A folder called 'MyU_files' will be created alongside the 'MyU.html' file.
    5. Upload the 'MyU.html' file to this app using the upload section below.
    """)


def main() -> None:
    init_session_state()

    render_project_info_section()
    st.divider()
    render_getting_started_section()
    st.divider()
    render_upload_section()
    st.divider()
    render_question_section()
    st.divider()
    render_answer_section()


if __name__ == "__main__":
    main()
