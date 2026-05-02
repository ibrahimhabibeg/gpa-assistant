import pytest

from gpa_assist.algorithms import (
    calculate_overall_rating,
    gpa_to_closest_letter_grade,
    calculate_max_possible_gpa,
    max_achievable_rating,
    can_i_get_a_certain_rating,
    what_per_course_average_gpa_is_needed_for_rating,
    if_i_continue_with_a_certain_gpa_for_remaining_courses,
)
from gpa_assist.config import OverallRating
from gpa_assist.models import StudentTranscript
from gpa_assist.config import LetterGrade


@pytest.mark.parametrize(
    "gpa,expected",
    [
        (4.0, OverallRating.EXCELLENT),
        (3.5, OverallRating.EXCELLENT),
        (3.49, OverallRating.VERY_GOOD),
        (3.0, OverallRating.VERY_GOOD),
        (2.99, OverallRating.GOOD),
        (2.5, OverallRating.GOOD),
        (2.49, OverallRating.ACCEPTED),
        (2.0, OverallRating.ACCEPTED),
        (1.99, OverallRating.WEAK),
        (1.0, OverallRating.WEAK),
        (0.99, OverallRating.TOO_WEAK),
        (0.0, OverallRating.TOO_WEAK),
    ],
)
def test_calculate_overall_rating(gpa: float, expected: OverallRating) -> None:
    assert calculate_overall_rating(gpa) == expected


@pytest.mark.parametrize(
    "gpa,expected",
    [
        (4.0, LetterGrade.A_PLUS),
        (3.85, LetterGrade.A_PLUS),
        (3.84, LetterGrade.A),
        (3.7, LetterGrade.A),
        (3.55, LetterGrade.A),
        (3.54, LetterGrade.A_MINUS),
        (3.4, LetterGrade.A_MINUS),
        (3.3, LetterGrade.A_MINUS),
        (3.29, LetterGrade.B_PLUS),
        (3.2, LetterGrade.B_PLUS),
        (3.1, LetterGrade.B_PLUS),
        (3.09, LetterGrade.B),
        (3.0, LetterGrade.B),
        (1.5, LetterGrade.D),
        (1.25, LetterGrade.D),
        (1.24, LetterGrade.D_MINUS),
        (1.0, LetterGrade.D_MINUS),
        (0.5, LetterGrade.D_MINUS),
        (0.49, LetterGrade.FAIL),
        (0.0, LetterGrade.FAIL),
    ],
)
def test_gpa_to_closest_letter_grade(gpa: float, expected: LetterGrade) -> None:
    assert gpa_to_closest_letter_grade(gpa) == expected, (
        f"Expected {expected} for GPA {gpa}"
    )


def test_calculate_max_possible_gpa(sample_transcript: StudentTranscript) -> None:
    max_gpa = calculate_max_possible_gpa(sample_transcript)
    expected = (21.0 + (4.0 * 128.0)) / 134.0
    assert max_gpa == pytest.approx(expected)


def test_calculate_max_possible_gpa_no_remaining(
    sample_transcript_completed_low_gpa: StudentTranscript,
) -> None:
    max_gpa = calculate_max_possible_gpa(sample_transcript_completed_low_gpa)
    assert max_gpa == sample_transcript_completed_low_gpa.get_cumulative_gpa()


def test_max_achievable_rating(sample_transcript: StudentTranscript) -> None:
    assert max_achievable_rating(sample_transcript) == OverallRating.EXCELLENT


@pytest.mark.parametrize(
    "target_rating,expected",
    [
        (OverallRating.EXCELLENT, True),
        (OverallRating.VERY_GOOD, True),
    ],
)
def test_can_i_get_a_certain_rating(
    sample_transcript_completed_low_gpa: StudentTranscript,
    target_rating: OverallRating,
    expected: bool,
) -> None:
    assert (
        can_i_get_a_certain_rating(sample_transcript_completed_low_gpa, target_rating)
        is expected
    )


def test_what_per_course_average_gpa_is_needed_for_rating(
    sample_transcript: StudentTranscript,
) -> None:
    required = what_per_course_average_gpa_is_needed_for_rating(
        sample_transcript, OverallRating.EXCELLENT
    )
    assert required == pytest.approx(3.5)


def test_what_per_course_average_gpa_is_needed_for_rating_no_remaining(
    sample_transcript_completed_low_gpa: StudentTranscript,
) -> None:
    required = what_per_course_average_gpa_is_needed_for_rating(
        sample_transcript_completed_low_gpa, OverallRating.EXCELLENT
    )
    assert required == 0.0


@pytest.mark.parametrize(
    "hypothetical_gpa,expected",
    [
        (4.0, (21.0 + (4.0 * 128.0)) / 134.0),
        (3.0, (21.0 + (3.0 * 128.0)) / 134.0),
        (2.0, (21.0 + (2.0 * 128.0)) / 134.0),
    ],
)
def test_if_i_continue_with_a_certain_gpa_for_remaining_courses(
    sample_transcript: StudentTranscript, hypothetical_gpa: float, expected: float
) -> None:
    final_gpa = if_i_continue_with_a_certain_gpa_for_remaining_courses(
        sample_transcript, hypothetical_gpa
    )
    assert final_gpa == pytest.approx(expected)
