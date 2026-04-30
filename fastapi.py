from fastapi import FastAPI, File, UploadFile
from .models import StudentTranscript, OverallRating
from .parser import parse_html_string
from .algorithms import (
    calculate_max_possible_gpa,
    can_i_get_a_certain_rating,
    if_i_continue_with_a_certain_gpa_for_remaining_courses,
    max_achievable_rating,
    what_per_course_average_gpa_is_needed_for_rating,
    calculate_cumulative_gpa,
)

app = FastAPI()


@app.post("/parse-transcript")
async def parse_transcript(
    html_file: UploadFile = File(...),
    program_total_hours: float = 143.0,
    non_gpa_hours: float = 9.0,
) -> StudentTranscript:
    content = await html_file.read()
    html_string = content.decode("utf-8")
    transcript = parse_html_string(
        html_string,
        program_total_hours=program_total_hours,
        non_gpa_hours=non_gpa_hours,
    )
    return transcript


@app.post("/maximum-gpa")
def maximum_gpa(transcript: StudentTranscript) -> float:
    return calculate_max_possible_gpa(transcript)


@app.post("/rating-possibility")
def rating_possibility(
    transcript: StudentTranscript, target_rating: OverallRating
) -> bool:
    return can_i_get_a_certain_rating(transcript, target_rating)


@app.post("/hypothetical-gpa-outcome")
def hypothetical_gpa_outcome(
    transcript: StudentTranscript, hypothetical_gpa: float
) -> float:
    return if_i_continue_with_a_certain_gpa_for_remaining_courses(
        transcript, hypothetical_gpa
    )


@app.post("/max-achievable-rating")
def max_achievable_rating_endpoint(transcript: StudentTranscript) -> OverallRating:
    return max_achievable_rating(transcript)


@app.post("/required-average-gpa-for-rating")
def required_average_gpa_for_rating(
    transcript: StudentTranscript, target_rating: OverallRating
) -> float:
    return what_per_course_average_gpa_is_needed_for_rating(transcript, target_rating)


@app.post("/calculate-gpa")
def calculate_gpa(transcript: StudentTranscript) -> float:
    return calculate_cumulative_gpa(transcript)
