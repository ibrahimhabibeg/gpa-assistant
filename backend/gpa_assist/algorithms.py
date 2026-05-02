from backend.gpa_assist.models import (
    Course,
    LetterGrade,
    Semester,
    StudentTranscript,
)
from backend.gpa_assist.config import GRADE_POINT_MAP, RATING_THRESHOLDS, OverallRating


def calculate_overall_rating(gpa: float) -> OverallRating:
    for threshold, rating in RATING_THRESHOLDS:
        if gpa >= threshold:
            return rating

    return OverallRating.TOO_WEAK


def gpa_to_closest_letter_grade(gpa: float) -> str:
    closest_grade = min(
        GRADE_POINT_MAP.keys(), key=lambda grade: abs(GRADE_POINT_MAP[grade] - gpa)
    )
    return closest_grade


def calculate_max_possible_gpa(transcript: StudentTranscript) -> float:
    remaining_hours = transcript.get_remaining_hours_in_gpa_courses()
    if remaining_hours <= 0:
        return transcript.get_cumulative_gpa()
    else:
        new_course = Course(
            code="HYPOTHETICAL",
            name="Hypothetical Course",
            credit_hours=remaining_hours,
            degree=0.0,
            letter_grade=LetterGrade.A_PLUS,
        )
        hypothetical_transcript = StudentTranscript(
            semesters=transcript.semesters + [Semester(courses=[new_course])],
            program_total_hours=transcript.program_total_hours,
            non_gpa_hours=transcript.non_gpa_hours,
        )
        return hypothetical_transcript.get_cumulative_gpa()


def max_achievable_rating(transcript: StudentTranscript) -> OverallRating:
    max_gpa = calculate_max_possible_gpa(transcript)
    return calculate_overall_rating(max_gpa)


def can_i_get_a_certain_rating(
    transcript: StudentTranscript, target_rating: OverallRating
) -> bool:
    max_gpa = calculate_max_possible_gpa(transcript)
    target_threshold = next(
        (
            threshold
            for threshold, rating in RATING_THRESHOLDS
            if rating == target_rating
        ),
        0.0,
    )
    return max_gpa >= target_threshold


def what_per_course_average_gpa_is_needed_for_rating(
    transcript: StudentTranscript, target_rating: OverallRating
) -> float:
    target_threshold = next(
        (
            threshold
            for threshold, rating in RATING_THRESHOLDS
            if rating == target_rating
        ),
        0.0,
    )

    current_quality_points = transcript.get_total_quality_points()
    current_hours = transcript.get_total_credit_hours_counting_toward_gpa()
    remaining_hours = transcript.get_remaining_hours_in_gpa_courses()

    if remaining_hours <= 0:
        return 0.0

    required_total_quality_points = target_threshold * (current_hours + remaining_hours)
    required_quality_points_from_remaining = (
        required_total_quality_points - current_quality_points
    )
    required_average_gpa = required_quality_points_from_remaining / remaining_hours

    return required_average_gpa


def if_i_continue_with_a_certain_gpa_for_remaining_courses(
    transcript: StudentTranscript, hypothetical_gpa: float
) -> float:
    current_quality_points = transcript.get_total_quality_points()
    current_hours = transcript.get_total_credit_hours_counting_toward_gpa()
    remaining_hours = transcript.get_remaining_hours_in_gpa_courses()

    if remaining_hours <= 0:
        return transcript.get_cumulative_gpa()

    hypothetical_quality_points_from_remaining = hypothetical_gpa * remaining_hours
    total_quality_points = (
        current_quality_points + hypothetical_quality_points_from_remaining
    )
    total_hours = current_hours + remaining_hours
    final_gpa = total_quality_points / total_hours if total_hours > 0 else 0.0

    return final_gpa
