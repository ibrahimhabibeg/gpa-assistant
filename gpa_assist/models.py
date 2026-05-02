from pydantic import BaseModel, Field
from typing import List, Optional
from gpa_assist.config import GRADE_POINT_MAP, LetterGrade

# WARNING
# Since there is no indicatorin the transcript for non-GPA courses
# I am assuming that any non-GPA course will have a letter grade of "P" (Pass)
# i.e. No one fails on a non-GPA course


class Course(BaseModel):
    code: str = Field()
    name: str = Field()
    credit_hours: float = Field()
    degree: float = Field()
    letter_grade: LetterGrade = Field()

    # Returns None for non-GPA courses (Pass)
    def get_gpa_points(self) -> Optional[float]:
        return GRADE_POINT_MAP.get(self.letter_grade)

    def get_grade_quality_points(self) -> float:
        return (self.get_gpa_points() or 0) * self.credit_hours

    def is_failed(self) -> bool:
        return (
            self.letter_grade == LetterGrade.FAIL
            or self.letter_grade == LetterGrade.EXAM_FAIL
            or self.letter_grade == LetterGrade.ABSENT
        )

    def counts_toward_gpa(self) -> bool:
        return (
            self.letter_grade != LetterGrade.PASS
        )  # Assumes no fails on non-GPA courses


class Semester(BaseModel):
    courses: List[Course] = Field()

    def get_total_quality_points(self) -> float:
        return sum(course.get_grade_quality_points() for course in self.courses)

    def get_total_credit_hours_counting_toward_gpa(self) -> float:
        return sum(
            course.credit_hours for course in self.courses if course.counts_toward_gpa()
        )


class StudentTranscript(BaseModel):
    semesters: List[Semester] = Field()
    program_total_hours: float = Field()
    non_gpa_hours: float = Field()

    def get_total_credit_hours_counting_toward_gpa(self) -> float:
        return sum(
            semester.get_total_credit_hours_counting_toward_gpa()
            for semester in self.semesters
        )

    def get_total_quality_points(self) -> float:
        return sum(semester.get_total_quality_points() for semester in self.semesters)

    def get_all_courses(self) -> List[Course]:
        all_courses = []
        for semester in self.semesters:
            all_courses.extend(semester.courses)
        return all_courses

    def get_cumulative_gpa(self) -> float:
        sum_quality_points = self.get_total_quality_points()
        sum_credit_hours = self.get_total_credit_hours_counting_toward_gpa()
        return sum_quality_points / sum_credit_hours if sum_credit_hours > 0 else 0.0

    def get_remaining_hours_in_gpa_courses(self) -> float:
        completed_hours = self.get_total_credit_hours_counting_toward_gpa()
        return max(0.0, self.program_total_hours - self.non_gpa_hours - completed_hours)
