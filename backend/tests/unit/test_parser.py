import pytest
from bs4 import BeautifulSoup

from gpa_assist.config import LetterGrade
from gpa_assist.models import StudentTranscript
from gpa_assist.parser import (
    extract_course_from_row,
    extract_semester_from_table,
    parse_html_string,
)


@pytest.fixture
def html_english_basic() -> str:
    return """
    <table>
      <tr>
        <th>Code</th><th>Name</th><th>Credit Hours</th><th>Degree</th><th>Grade</th>
      </tr>
      <tr>
        <td>CS101</td><td>CS</td><td>3</td><td>90</td><td>A+</td>
      </tr>
      <tr>
        <td>Term GPA</td><td>...</td>
      </tr>
    </table>
    """


@pytest.fixture
def html_arabic_basic() -> str:
    return """
    <table>
      <tr>
        <th>الكود</th><th>المقرر</th><th>الساعات المعتمدة</th><th>الدرجة</th><th>التقدير</th>
      </tr>
      <tr>
        <td>UNI101</td><td>جودة</td><td>3</td><td>90</td><td>أ+</td>
      </tr>
      <tr>
        <td>المعدل الفصلى</td><td>...</td>
      </tr>
    </table>
    """


def test_parse_html_string_english(html_english_basic: str) -> None:
    transcript = parse_html_string(html_english_basic)
    assert len(transcript.semesters) == 1
    assert len(transcript.semesters[0].courses) == 1
    assert transcript.semesters[0].courses[0].letter_grade == LetterGrade.A_PLUS


def test_parse_html_string_arabic(html_arabic_basic: str) -> None:
    transcript = parse_html_string(html_arabic_basic)
    assert len(transcript.semesters) == 1
    assert len(transcript.semesters[0].courses) == 1
    assert transcript.semesters[0].courses[0].letter_grade == LetterGrade.A_PLUS


def test_extract_course_from_row_skips_missing_degree() -> None:
    html = """
    <table>
      <tr>
        <th>Code</th><th>Name</th><th>Credit Hours</th><th>Degree</th><th>Grade</th>
      </tr>
      <tr>
        <td>CS101</td><td>Intro</td><td>3</td><td></td><td>A+</td>
      </tr>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    row = soup.find_all("tr")[1]
    assert extract_course_from_row(row, is_arabic=False) is None


def test_extract_semester_from_table_skips_non_matching_header() -> None:
    html = """
    <table>
      <tr>
        <th>Test</th><th>Test</th>
      </tr>
      <tr>
        <td>1</td><td>2</td>
      </tr>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    assert extract_semester_from_table(table) is None


def test_english_and_arabic_parsing_consistency(
    parse_good_student_transcript: StudentTranscript,
    parse_good_student_transcript_english: StudentTranscript,
) -> None:
    assert len(parse_good_student_transcript.semesters) == len(
        parse_good_student_transcript_english.semesters
    )
    for sem_ar, sem_en in zip(
        parse_good_student_transcript.semesters,
        parse_good_student_transcript_english.semesters,
    ):
        assert len(sem_ar.courses) == len(sem_en.courses)
        for course_ar, course_en in zip(sem_ar.courses, sem_en.courses):
            assert course_ar.code == course_en.code
            assert course_ar.credit_hours == course_en.credit_hours
            assert course_ar.degree == course_en.degree
            assert course_ar.letter_grade == course_en.letter_grade

def test_very_good_parsing(
    parse_very_good_student_transcript: StudentTranscript,
) -> None:
    transcript = parse_very_good_student_transcript
    assert len(transcript.semesters) == 5
    assert round(transcript.get_cumulative_gpa(), 2) == 3.37
    assert transcript.semesters[0].courses[0].code == "UNI-101"
    assert transcript.semesters[0].courses[0].letter_grade == LetterGrade.PASS
    assert transcript.semesters[4].courses[0].code == "CSC-309"
    assert transcript.semesters[4].courses[0].letter_grade == LetterGrade.A_PLUS

def test_good_english_parsing(
    parse_good_student_transcript_english: StudentTranscript,
) -> None:
    transcript = parse_good_student_transcript_english
    assert len(transcript.semesters) == 6
    assert round(transcript.get_cumulative_gpa(), 2) == 2.88
    assert transcript.semesters[0].courses[0].code == "UNI-101"
    assert transcript.semesters[0].courses[0].letter_grade == LetterGrade.PASS
    assert transcript.semesters[5].courses[0].code == "CSC-309"
    assert transcript.semesters[5].courses[0].letter_grade == LetterGrade.A_PLUS