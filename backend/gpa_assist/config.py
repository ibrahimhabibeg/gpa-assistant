from enum import StrEnum


class LetterGrade(StrEnum):
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
    FAIL = "F"
    EXAM_FAIL = "BF"
    ABSENT = "Abs"
    PASS = "P"


class OverallRating(StrEnum):
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


GRADE_POINT_MAP: dict[LetterGrade, float] = {
    LetterGrade.A_PLUS: 4.0,
    LetterGrade.A: 3.7,
    LetterGrade.A_MINUS: 3.4,
    LetterGrade.B_PLUS: 3.2,
    LetterGrade.B: 3.0,
    LetterGrade.B_MINUS: 2.8,
    LetterGrade.C_PLUS: 2.6,
    LetterGrade.C: 2.4,
    LetterGrade.C_MINUS: 2.2,
    LetterGrade.D_PLUS: 2.0,
    LetterGrade.D: 1.5,
    LetterGrade.D_MINUS: 1.0,
    LetterGrade.FAIL: 0.0,
    LetterGrade.EXAM_FAIL: 0.0,
    LetterGrade.ABSENT: 0.0,
    # LetterGrade.PASS: 0.0,  # Don't count toward GPA
}

# WARNING: I am not 100% sure about the mapping for failed courses
ARABIC_TO_ENGLISH_GRADES: dict[str, LetterGrade] = {
    "أ+": LetterGrade.A_PLUS,
    "أ": LetterGrade.A,
    "أ-": LetterGrade.A_MINUS,
    "ب+": LetterGrade.B_PLUS,
    "ب": LetterGrade.B,
    "ب-": LetterGrade.B_MINUS,
    "ج+": LetterGrade.C_PLUS,
    "ج": LetterGrade.C,
    "ج-": LetterGrade.C_MINUS,
    "د+": LetterGrade.D_PLUS,
    "د": LetterGrade.D,
    "د-": LetterGrade.D_MINUS,
    "راسب": LetterGrade.FAIL,
    "BF": LetterGrade.EXAM_FAIL,
    "غائب": LetterGrade.ABSENT,
    "ناجح": LetterGrade.PASS,
}
