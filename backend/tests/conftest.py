import os

import pytest
from gpa_assist.models import Course, Semester, StudentTranscript
from gpa_assist.config import LetterGrade
from gpa_assist.parser import parse_html_string


@pytest.fixture
def sample_a_plus_course() -> Course:
    return Course(
        code="MAT102",
        name="Statistics and Probability",
        credit_hours=3.0,
        degree=99.0,
        letter_grade=LetterGrade.A_PLUS,
    )


@pytest.fixture
def sample_b_course() -> Course:
    return Course(
        code="MAT101",
        name="Discrete Mathematics",
        credit_hours=3.0,
        degree=80.0,
        letter_grade=LetterGrade.B,
    )


@pytest.fixture
def sample_course_not_in_gpa() -> Course:
    return Course(
        code="UNI102",
        name="Introduction to Quality",
        credit_hours=2.0,
        degree=100.0,
        letter_grade=LetterGrade.PASS,
    )


@pytest.fixture
def sample_semester(
    sample_a_plus_course: Course,
    sample_b_course: Course,
    sample_course_not_in_gpa: Course,
) -> Semester:
    return Semester(
        courses=[sample_a_plus_course, sample_b_course, sample_course_not_in_gpa]
    )


@pytest.fixture
def sample_transcript(sample_semester: Semester) -> StudentTranscript:
    return StudentTranscript(
        semesters=[sample_semester],
        program_total_hours=143.0,
        non_gpa_hours=9.0,
    )


@pytest.fixture
def sample_transcript_completed_low_gpa(sample_semester: Semester) -> StudentTranscript:
    return StudentTranscript(
        semesters=[sample_semester], program_total_hours=8.0, non_gpa_hours=2.0
    )


file_dir = os.path.dirname(__file__)


@pytest.fixture
def parse_good_student_transcript() -> StudentTranscript:
    return parse_html_string(
        open(os.path.join(file_dir, "sample_transcripts/Good.html"), "r").read()
    )


@pytest.fixture
def parse_very_good_student_transcript() -> StudentTranscript:
    return parse_html_string(
        open(os.path.join(file_dir, "sample_transcripts/Very_Good.html"), "r").read()
    )


@pytest.fixture
def parse_good_student_transcript_english() -> StudentTranscript:
    return parse_html_string(
        open(os.path.join(file_dir, "sample_transcripts/Good_English.html"), "r").read()
    )
