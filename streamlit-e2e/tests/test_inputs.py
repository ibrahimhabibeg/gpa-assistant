from pages.home_page import HomePage
import constants


def test_initial_values(driver):
    page = HomePage(driver)

    assert page.get_heading_text() == constants.EXPECTED_TITLE
    assert page.get_program_hours() == constants.DEFAULT_PROGRAM_HOURS
    assert page.get_non_gpa_hours() == constants.DEFAULT_NON_GPA_HOURS


def test_change_program_hours(driver):
    page = HomePage(driver)
    page.set_program_hours("150")
    assert page.get_program_hours() == "150"


def test_change_non_gpa_hours(driver):
    page = HomePage(driver)
    page.set_non_gpa_hours("12")
    assert page.get_non_gpa_hours() == "12"
def test_negative_program_hours(driver):
    page = HomePage(driver)
    page.set_program_hours("-150")
    assert page.get_program_hours() != "150"


def test_negative_non_gpa_hours(driver):
    page = HomePage(driver)
    page.set_non_gpa_hours("-12")
    assert page.get_non_gpa_hours() != "12"