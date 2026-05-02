import pytest

from gpa_assist.config import GRADE_POINT_MAP
from gpa_assist.models import Course, Semester, StudentTranscript
from gpa_assist.config import LetterGrade


@pytest.mark.parametrize(
    "letter_grade,expected",
    [
        (LetterGrade.A_PLUS, GRADE_POINT_MAP[LetterGrade.A_PLUS]),
        (LetterGrade.B, GRADE_POINT_MAP[LetterGrade.B]),
        (LetterGrade.PASS, None),
    ],
)
def test_course_get_gpa_points(
    letter_grade: LetterGrade, expected: float | None
) -> None:
    course = Course(
        code="TEST",
        name="Test",
        credit_hours=3.0,
        degree=90.0,
        letter_grade=letter_grade,
    )
    assert course.get_gpa_points() == expected


@pytest.mark.parametrize(
    "letter_grade,credit_hours,expected",
    [
        (LetterGrade.A_PLUS, 3.0, 12.0),
        (LetterGrade.B, 2.0, 6.0),
        (LetterGrade.PASS, 4.0, 0.0),
    ],
)
def test_course_grade_quality_points(
    letter_grade: LetterGrade, credit_hours: float, expected: float
) -> None:
    course = Course(
        code="TEST",
        name="Test",
        credit_hours=credit_hours,
        degree=90.0,
        letter_grade=letter_grade,
    )
    assert course.get_grade_quality_points() == expected


@pytest.mark.parametrize(
    "letter_grade,expected",
    [
        (LetterGrade.FAIL, True),
        (LetterGrade.EXAM_FAIL, True),
        (LetterGrade.ABSENT, True),
        (LetterGrade.A, False),
    ],
)
def test_course_is_failed(letter_grade: LetterGrade, expected: bool) -> None:
    course = Course(
        code="TEST",
        name="Test",
        credit_hours=3.0,
        degree=90.0,
        letter_grade=letter_grade,
    )
    assert course.is_failed() is expected


@pytest.mark.parametrize(
    "letter_grade,expected",
    [
        (LetterGrade.PASS, False),
        (LetterGrade.A_MINUS, True),
        (LetterGrade.ABSENT, True),
    ],
)
def test_course_counts_toward_gpa(letter_grade: LetterGrade, expected: bool) -> None:
    course = Course(
        code="TEST",
        name="Test",
        credit_hours=3.0,
        degree=90.0,
        letter_grade=letter_grade,
    )
    assert course.counts_toward_gpa() is expected


def test_sample_a_plus_course(sample_a_plus_course: Course) -> None:
    assert sample_a_plus_course.code == "MAT102"
    assert sample_a_plus_course.name == "Statistics and Probability"
    assert sample_a_plus_course.credit_hours == 3.0
    assert sample_a_plus_course.degree == 99.0
    assert sample_a_plus_course.letter_grade == LetterGrade.A_PLUS
    assert sample_a_plus_course.get_gpa_points() == GRADE_POINT_MAP[LetterGrade.A_PLUS]
    assert (
        sample_a_plus_course.get_grade_quality_points()
        == GRADE_POINT_MAP[LetterGrade.A_PLUS] * 3.0
    )
    assert not sample_a_plus_course.is_failed()
    assert sample_a_plus_course.counts_toward_gpa()


def test_sample_b_course(sample_b_course: Course) -> None:
    assert sample_b_course.code == "MAT101"
    assert sample_b_course.name == "Discrete Mathematics"
    assert sample_b_course.credit_hours == 3.0
    assert sample_b_course.degree == 80.0
    assert sample_b_course.letter_grade == LetterGrade.B
    assert sample_b_course.get_gpa_points() == GRADE_POINT_MAP[LetterGrade.B]
    assert (
        sample_b_course.get_grade_quality_points()
        == GRADE_POINT_MAP[LetterGrade.B] * 3.0
    )
    assert not sample_b_course.is_failed()
    assert sample_b_course.counts_toward_gpa()


def test_sample_course_not_in_gpa(sample_course_not_in_gpa: Course) -> None:
    assert sample_course_not_in_gpa.code == "UNI102"
    assert sample_course_not_in_gpa.name == "Introduction to Quality"
    assert sample_course_not_in_gpa.credit_hours == 2.0
    assert sample_course_not_in_gpa.degree == 100.0
    assert sample_course_not_in_gpa.letter_grade == LetterGrade.PASS
    assert sample_course_not_in_gpa.get_gpa_points() is None
    assert sample_course_not_in_gpa.get_grade_quality_points() == 0.0
    assert not sample_course_not_in_gpa.is_failed()
    assert not sample_course_not_in_gpa.counts_toward_gpa()


def test_semester_quality_points():
    course1 = Course(
        code="CS101",
        name="CS",
        credit_hours=3.0,
        degree=96.0,
        letter_grade=LetterGrade.A_PLUS,
    )
    course2 = Course(
        code="MAT101",
        name="MATH",
        credit_hours=3.0,
        degree=95.0,
        letter_grade=LetterGrade.A,
    )
    semester = Semester(courses=[course1, course2])
    assert (
        semester.get_total_quality_points()
        == course1.get_grade_quality_points() + course2.get_grade_quality_points()
    )


def test_semester_credit_hours_counting_toward_gpa():
    course1 = Course(
        code="CS101",
        name="ABC",
        credit_hours=3.0,
        degree=96.0,
        letter_grade=LetterGrade.A_PLUS,
    )
    course2 = Course(
        code="MAT101",
        name="ABC",
        credit_hours=3.0,
        degree=95.0,
        letter_grade=LetterGrade.A,
    )
    course3 = Course(
        code="UNI101",
        name="ABC",
        credit_hours=2.0,
        degree=100.0,
        letter_grade=LetterGrade.PASS,
    )
    semester = Semester(courses=[course1, course2, course3])
    assert semester.get_total_credit_hours_counting_toward_gpa() == 6.0


def test_sample_semester(sample_semester: Semester) -> None:
    assert len(sample_semester.courses) == 3
    assert (
        sample_semester.get_total_quality_points()
        == 3 * GRADE_POINT_MAP[LetterGrade.A_PLUS] + 3 * GRADE_POINT_MAP[LetterGrade.B]
    )
    assert sample_semester.get_total_credit_hours_counting_toward_gpa() == 6.0
    assert sample_semester.courses[0].code == "MAT102"
    assert sample_semester.courses[1].code == "MAT101"
    assert sample_semester.courses[2].code == "UNI102"


def test_transcript_totals_and_gpa(sample_transcript: StudentTranscript) -> None:
    assert (
        sample_transcript.get_total_quality_points()
        == 3 * GRADE_POINT_MAP[LetterGrade.A_PLUS] + 3 * GRADE_POINT_MAP[LetterGrade.B]
    )
    assert sample_transcript.get_total_credit_hours_counting_toward_gpa() == 6.0
    assert sample_transcript.get_cumulative_gpa() == pytest.approx(
        (3 * GRADE_POINT_MAP[LetterGrade.A_PLUS] + 3 * GRADE_POINT_MAP[LetterGrade.B]) / 6.0
    )


def test_transcript_remaining_hours(sample_transcript: StudentTranscript) -> None:
    assert sample_transcript.get_remaining_hours_in_gpa_courses() == 143 - 9 - 6


def test_transcript_all_courses_order(sample_transcript: StudentTranscript) -> None:
    courses = sample_transcript.get_all_courses()
    assert [course.code for course in courses] == ["MAT102", "MAT101", "UNI102"]
