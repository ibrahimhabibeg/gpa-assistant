import os
from pages.home_page import HomePage


def test_program_hours_input(driver):
    page = HomePage(driver)

    assert page.get_program_hours() == "143"

    page.set_program_hours("150")
    assert page.get_program_hours() == "150"

def test_negative_program_hours_input(driver):
    page = HomePage(driver)

    assert page.get_program_hours() == "143"

    page.set_program_hours("-150")
    assert page.get_program_hours() == "-150" #fix this to be "page.get_program_hours() != "-150" "


def test_non_gpa_hours_input(driver):
    page = HomePage(driver)

    assert page.get_non_gpa_hours() == "9"

    page.set_non_gpa_hours("12")
    assert page.get_non_gpa_hours() == "12"

def test_negative_non_gpa_hours_input(driver):
    page = HomePage(driver)

    assert page.get_non_gpa_hours() == "9"

    page.set_non_gpa_hours("-12")
    assert page.get_non_gpa_hours() == "-12" #fix this to be "page.get_non_gpa_hours() != "-12" "


def test_upload_html_file(driver):
    page = HomePage(driver)

    file_path = os.path.abspath("test_files/MyU.html")
    page.upload_file(file_path)

    success = page.get_upload_success()
    assert success.is_displayed()

    filename_el = page.get_upload_file_name()
    assert filename_el.text == "MyU.html"

    heading = page.get_upload_heading()
    assert heading.text == "File Ready"