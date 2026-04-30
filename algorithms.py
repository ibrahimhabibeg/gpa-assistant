from typing import List, Optional
from .models import (
    Course,
    LetterGrade,
    StudentTranscript,
    GRADE_POINT_MAP,
    OverallRating,
    RATING_THRESHOLDS,
)


def calculate_cumulative_gpa(transcript: StudentTranscript) -> float:
    all_courses = transcript.get_all_courses()
    all_courses = [c for c in all_courses if c.counts_toward_gpa()]
    total_quality_points = sum(c.get_grade_quality_points() for c in all_courses)
    total_hours = sum(c.credit_hours for c in all_courses)
    return total_quality_points / total_hours if total_hours > 0 else 0.0


def calculate_cumulative_gpa_from_list(courses: List[Course]) -> float:
    courses = [c for c in courses if c.counts_toward_gpa()]
    total_quality_points = sum(c.get_grade_quality_points() for c in courses)
    total_hours = sum(c.credit_hours for c in courses)
    return total_quality_points / total_hours if total_hours > 0 else 0.0


def calculate_total_credit_hours(transcript: StudentTranscript) -> float:
    return sum(course.credit_hours for course in transcript.get_all_courses())


def calculate_total_earned_hours(transcript: StudentTranscript) -> float:
    return sum(
        course.credit_hours
        for course in transcript.get_all_courses()
        if not course.is_failed()
    )


def calculate_total_earned_hours_counting_toward_gpa(
    transcript: StudentTranscript,
) -> float:
    return sum(
        course.credit_hours
        for course in transcript.get_all_courses()
        if not course.is_failed() and course.counts_toward_gpa()
    )


def calculate_remaining_hours_to_graduate(transcript: StudentTranscript) -> float:
    hours_needed = transcript.program_total_hours - calculate_total_earned_hours(
        transcript
    )
    return max(0.0, hours_needed)


def calculate_in_gpa_hours_to_graduate(transcript: StudentTranscript) -> float:
    hours_needed = (
        transcript.program_total_hours
        - transcript.non_gpa_hours
        - calculate_total_earned_hours_counting_toward_gpa(transcript)
    )
    return max(0.0, hours_needed)


def calculate_overall_rating(gpa: float) -> OverallRating:
    for threshold, rating in RATING_THRESHOLDS:
        if gpa >= threshold:
            return rating

    return OverallRating.TOO_WEAK


def calculate_max_possible_gpa(transcript: StudentTranscript) -> float:
    remaining_hours = calculate_in_gpa_hours_to_graduate(transcript)
    if remaining_hours <= 0:
        return transcript.get_cumulative_gpa()
    else:
        courses = transcript.get_all_courses()
        # Assume A+ for all remaining courses
        courses.append(
            Course(
                code="",
                name="",
                credit_hours=calculate_in_gpa_hours_to_graduate(transcript),
                grade_points=GRADE_POINT_MAP[LetterGrade.A_PLUS.value],
                letter_grade=LetterGrade.A_PLUS.value,
            )
        )
        return calculate_cumulative_gpa_from_list(courses)


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
        None,
    )
    return max_gpa >= target_threshold


def what_per_course_average_gpa_is_needed_for_rating(
    transcript: StudentTranscript, target_rating: OverallRating
) -> Optional[float]:
    target_threshold = next(
        (
            threshold
            for threshold, rating in RATING_THRESHOLDS
            if rating == target_rating
        ),
        None,
    )
    if target_threshold is None:
        return None

    current_quality_points = sum(
        c.get_grade_quality_points()
        for c in transcript.get_all_courses()
        if c.counts_toward_gpa()
    )
    current_hours = sum(
        c.credit_hours for c in transcript.get_all_courses() if c.counts_toward_gpa()
    )
    remaining_hours = calculate_in_gpa_hours_to_graduate(transcript)

    if remaining_hours <= 0:
        return None

    required_total_quality_points = target_threshold * (current_hours + remaining_hours)
    required_quality_points_from_remaining = (
        required_total_quality_points - current_quality_points
    )
    required_average_gpa = required_quality_points_from_remaining / remaining_hours

    return required_average_gpa


def if_i_continue_with_a_certain_gpa_for_remaining_courses(
    transcript: StudentTranscript, hypothetical_gpa: float
) -> float:
    current_quality_points = sum(
        c.get_grade_quality_points()
        for c in transcript.get_all_courses()
        if c.counts_toward_gpa()
    )
    current_hours = sum(
        c.credit_hours for c in transcript.get_all_courses() if c.counts_toward_gpa()
    )
    remaining_hours = calculate_in_gpa_hours_to_graduate(transcript)

    if remaining_hours <= 0:
        return calculate_overall_rating(
            current_quality_points / current_hours if current_hours > 0 else 0.0
        )

    hypothetical_quality_points_from_remaining = hypothetical_gpa * remaining_hours
    total_quality_points = (
        current_quality_points + hypothetical_quality_points_from_remaining
    )
    total_hours = current_hours + remaining_hours
    final_gpa = total_quality_points / total_hours if total_hours > 0 else 0.0

    return final_gpa


def gpa_to_letter_grade(gpa: float) -> str:
    closest_grade = min(
        GRADE_POINT_MAP.keys(), key=lambda grade: abs(GRADE_POINT_MAP[grade] - gpa)
    )
    return closest_grade
