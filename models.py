from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class LetterGrade(str, Enum):

    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D_PLUS = "D+"
    D = "D"
    D_MINUS = "D-"
    F = "F"
    PASS = "Pass"


class TermType(str, Enum):

    FALL = "fall"
    SPRING = "spring"
    SUMMER = "summer"


class OverallRating(str, Enum):

    EXCELLENT = "excellent"
    VERY_GOOD = "very_good"
    GOOD = "good"
    ACCEPTED = "accepted"
    WEAK = "weak"
    TOO_WEAK = "too_weak"


RATING_THRESHOLDS = [
    (3.5, OverallRating.EXCELLENT),
    (3.0, OverallRating.VERY_GOOD),
    (2.5, OverallRating.GOOD),
    (2.0, OverallRating.ACCEPTED),
    (1.0, OverallRating.WEAK),
    (0.0, OverallRating.TOO_WEAK),
]



GRADE_POINT_MAP = {
    "A+": 4.0,
    "A": 3.7,
    "A-": 3.4,
    "B+": 3.2,
    "B": 3.0,
    "B-": 2.8,
    "C+": 2.6,
    "C": 2.4,
    "C-": 2.2,
    "D+": 2.0,
    "D": 1.5,
    "D-": 1.0,
    "F": 0.0,
    "BF": 0.0,
    "Abs": 0.0,
    "Pass": 0.0,  # Don't count toward GPA
}


class Course(BaseModel):

    code: str = Field()
    name: str = Field()
    credit_hours: float = Field()
    grade_points: float = Field()
    letter_grade: str = Field()

    def get_gpa_points(self) -> float:
        return GRADE_POINT_MAP.get(self.letter_grade, 0.0)

    def get_grade_quality_points(self) -> float:
        return self.get_gpa_points() * self.credit_hours
    
    def is_failed(self) -> bool:
        return self.get_gpa_points() == 0 and self.letter_grade != LetterGrade.PASS.value
    
    def counts_toward_gpa(self) -> bool:
        return self.letter_grade != LetterGrade.PASS.value


class Semester(BaseModel):

    term_type: TermType = Field()
    courses: List[Course] = Field()

    def get_total_credit_hours(self) -> float:
        return sum(course.credit_hours for course in self.courses)

    def get_earned_credit_hours(self) -> float:
        return sum(
            course.credit_hours
            for course in self.courses
            if not course.is_failed()
        )
    
    def get_passed_courses(self) -> List[Course]:
        return [c for c in self.courses if not c.is_failed()]
    
    def get_in_gpa_courses(self) -> List[Course]:
        return [c for c in self.courses if c.counts_toward_gpa()]

    def get_semester_gpa(self) -> float:
        courses_in_gpa = self.get_in_gpa_courses()
        total_quality_points = sum(c.get_grade_quality_points() for c in courses_in_gpa)
        total_hours = sum(c.credit_hours for c in courses_in_gpa)
        return total_quality_points / total_hours if total_hours > 0 else 0.0
    
    def get_total_quality_points_counting_toward_gpa(self) -> float:
        return sum(course.get_grade_quality_points() for course in self.get_in_gpa_courses())
    
    def get_total_hours_counting_toward_gpa(self) -> float:
        return sum(course.credit_hours for course in self.get_in_gpa_courses())
    

class StudentTranscript(BaseModel):
    semesters: List[Semester] = Field()
    program_total_hours: float = Field()
    non_gpa_hours: float = Field()

    def get_total_credit_hours(self) -> float:
        return sum(sem.get_total_credit_hours() for sem in self.semesters)

    def get_earned_credit_hours(self) -> float:
        return sum(sem.get_earned_credit_hours() for sem in self.semesters)

    def get_all_courses(self) -> List[Course]:
        all_courses = []
        for semester in self.semesters:
            all_courses.extend(semester.courses)
        return all_courses

    def get_failed_courses(self) -> List[Course]:
        """Get all failed courses (grade F)."""
        return [
            c
            for c in self.get_all_courses()
            if c.get_gpa_points() == 0 and c.letter_grade != LetterGrade.PASS.value
        ]        

    def get_remaining_hours_to_graduate(self) -> float:
        hours_needed = self.program_total_hours - self.get_earned_credit_hours()
        return max(0.0, hours_needed)
