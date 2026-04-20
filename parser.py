from bs4 import BeautifulSoup
from typing import List, Optional
from models import Course, Semester, StudentTranscript, TermType


ARABIC_HEADERS = {"الكود", "الساعات المعتمدة", "الدرجة"}
ENGLISH_HEADERS = {"Code", "Credit Hours", "Grade"}

ARABIC_SEMESTER_TYPES = {
    "الأول": "FALL",
    "الثانى": "SPRING",
    "الصيفي": "SUMMER",
}

ENGLISH_SEMESTER_TYPES = {
    "Fall": "FALL",
    "Spring": "SPRING",
    "Summer": "SUMMER",
}

ARABIC_TO_ENGLISH_GRADES = {
    "أ+": "A+",
    "أ": "A",
    "أ-": "A-",
    "ب+": "B+",
    "ب": "B",
    "ب-": "B-",
    "ج+": "C+",
    "ج": "C",
    "ج-": "C-",
    "د+": "D+",
    "د": "D",
    "د-": "D-",
    "ف": "F",
    "ناجح": "Pass",
}

ENGLISH_ABBREVIATIONS = {
    "P": "Pass",
}


def parse_html_file(
    html_path: str, program_total_hours: float = 140.0, non_gpa_hours: float = 9.0
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
    html_content: str, program_total_hours: float = 140.0, non_gpa_hours: float = 9.0
) -> StudentTranscript:
    soup = BeautifulSoup(html_content, "html.parser")
    semesters = extract_semesters_from_soup(soup)

    return StudentTranscript(
        semesters=semesters,
        program_total_hours=program_total_hours,
        non_gpa_hours=non_gpa_hours,
    )


def extract_semesters_from_soup(
    soup: BeautifulSoup,
) -> List[Semester]:
    semesters = []

    tables = soup.find_all("table")[::-1]

    for table in tables:
        rows = table.find_all("tr")
        if len(rows) < 2:
            continue

        header = rows[0]
        header_texts = [
            col.get_text(strip=True) for col in header.find_all(["td", "th"])
        ]

        is_arabic = any(text in header_texts for text in ARABIC_HEADERS)
        is_english = any(text in header_texts for text in ENGLISH_HEADERS)

        if not (is_arabic or is_english):
            continue

        courses = []

        for row in rows[1:]:
            cols = row.find_all(["td", "th"])
            texts = [col.get_text(strip=True) for col in cols]

            if not texts or len(texts) < 2:
                continue

            if is_arabic:
                if "المعدل الفصلى" in texts[0] or "الساعات" in texts[0]:
                    continue
            else:  # English
                if "Term GPA" in texts[0] or "Attempted Hours" in texts[0]:
                    continue

            if len(texts) >= 5:
                code = texts[0].strip()
                name = texts[1].strip()
                credit_hours_str = texts[2].strip().replace(",", ".")
                grade_str = texts[3].strip()
                letter_grade = texts[4].strip() if len(texts) > 4 else ""

                if not grade_str:
                    continue

                try:
                    credit_hours = float(credit_hours_str)

                    grade_points = float(grade_str)

                    if is_arabic:
                        english_letter_grade = ARABIC_TO_ENGLISH_GRADES.get(
                            letter_grade, letter_grade
                        )

                    else:
                        english_letter_grade = ENGLISH_ABBREVIATIONS.get(
                            letter_grade, letter_grade
                        )

                    course = Course(
                        code=code,
                        name=name,
                        credit_hours=credit_hours,
                        grade_points=grade_points,
                        letter_grade=english_letter_grade,
                    )
                    courses.append(course)
                except ValueError:
                    continue

        if len(courses) > 0:
            term_type = extract_term_type_from_table(table)

            semester = Semester(term_type=term_type, courses=courses)
            semesters.append(semester)

    return semesters


def extract_term_type_from_table(table) -> Optional[TermType]:
    try:
        ancestor = table
        for _ in range(4):
            ancestor = ancestor.parent
            if ancestor is None:
                return None

        title = ancestor.find("h5", class_="card-title")

        if title:
            spans = title.find_all("span")
            if spans:
                semester_name = spans[0].get_text(strip=True)
                if semester_name in ARABIC_SEMESTER_TYPES:
                    term_str = ARABIC_SEMESTER_TYPES[semester_name]
                    return TermType[term_str]

                if semester_name in ENGLISH_SEMESTER_TYPES:
                    term_str = ENGLISH_SEMESTER_TYPES[semester_name]
                    return TermType[term_str]
        return None
    except Exception:
        return None
