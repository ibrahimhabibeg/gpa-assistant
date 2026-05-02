from bs4 import BeautifulSoup
from typing import List, Optional
from gpa_assist.models import Course, Semester, StudentTranscript, LetterGrade
from gpa_assist.config import ARABIC_TO_ENGLISH_GRADES


ARABIC_HEADERS = {"الكود", "الساعات المعتمدة", "الدرجة"}
ENGLISH_HEADERS = {"Code", "Credit Hours", "Grade"}
ARABIC_BOTTOM_ROW_KEYWORDS = {"المعدل الفصلى", "الساعات"}
ENGLISH_BOTTOM_ROW_KEYWORDS = {"Term GPA", "Attempted Hours"}


def parse_html_file(
    html_path: str, program_total_hours: float = 143.0, non_gpa_hours: float = 9.0
) -> StudentTranscript:
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    semesters = extract_semesters_from_soup(soup)

    return StudentTranscript(
        semesters=semesters,
        program_total_hours=program_total_hours,
        non_gpa_hours=non_gpa_hours,
    )


def parse_html_string(
    html_content: str, program_total_hours: float = 143.0, non_gpa_hours: float = 9.0
) -> StudentTranscript:
    soup = BeautifulSoup(html_content, "html.parser")
    semesters = extract_semesters_from_soup(soup)

    return StudentTranscript(
        semesters=semesters,
        program_total_hours=program_total_hours,
        non_gpa_hours=non_gpa_hours,
    )


def extract_course_from_row(row, is_arabic: bool) -> Optional[Course]:
    cols = row.find_all(["td", "th"])
    texts = [col.get_text(strip=True) for col in cols]

    if not texts or len(texts) < 2:
        return None

    if is_arabic and any(keyword in texts[0] for keyword in ARABIC_BOTTOM_ROW_KEYWORDS):
        return None
    if not is_arabic and any(
        keyword in texts[0] for keyword in ENGLISH_BOTTOM_ROW_KEYWORDS
    ):
        return None

    if len(texts) >= 5:
        code = texts[0].strip()
        name = texts[1].strip()
        credit_hours_str = texts[2].strip().replace(",", ".")
        degree_str = texts[3].strip()
        letter_grade_str: str = texts[4].strip()

        if not degree_str:
            return None

        try:
            credit_hours = float(credit_hours_str)
            degree = float(degree_str)

            if is_arabic:
                letter_grade: LetterGrade = ARABIC_TO_ENGLISH_GRADES.get(letter_grade_str) # type: ignore
            else:
                letter_grade = LetterGrade(letter_grade_str)

            return Course(
                code=code,
                name=name,
                credit_hours=credit_hours,
                degree=degree,
                letter_grade=letter_grade,
            )
        except ValueError:
            return None

    return None


def extract_semester_from_table(table) -> Optional[Semester]:
    rows = table.find_all("tr")
    if len(rows) < 2:
        return None

    header = rows[0]
    header_texts = [col.get_text(strip=True) for col in header.find_all(["td", "th"])]

    is_arabic = any(text in header_texts for text in ARABIC_HEADERS)
    is_english = any(text in header_texts for text in ENGLISH_HEADERS)

    if not (is_arabic or is_english):
        return None

    courses = [extract_course_from_row(row, is_arabic) for row in rows[1:]]
    courses = [course for course in courses if course is not None]

    return Semester(courses=courses) if len(courses) > 0 else None


def extract_semesters_from_soup(
    soup: BeautifulSoup,
) -> List[Semester]:
    semesters = []

    tables = soup.find_all("table")[::-1]

    for table in tables:
        semester = extract_semester_from_table(table)
        if semester:
            semesters.append(semester)

    return semesters
