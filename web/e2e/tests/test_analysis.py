from pages.analysis_page import AnalysisPage
import constants

def test_can_reach_excellent(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("can_reach")
    page.choose_rating("excellent")

    assert constants.EXPECTED_can_achieve_excellent in page.get_result()

def test_can_reach_very_good(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("can_reach")
    page.choose_rating("very_good")

    assert constants.EXPECTED_can_achieve_very_good in page.get_result()

 

def test_can_reach_good(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("can_reach")
    page.choose_rating("good")

    assert constants.EXPECTED_can_achieve_good in page.get_result()


def test_can_reach_accepted(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("can_reach")
    page.choose_rating("accepted")

    assert constants.EXPECTED_can_achieve_accepted in page.get_result()


def test_can_reach_weak(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("can_reach")
    page.choose_rating("weak")

    assert constants.EXPECTED_can_achieve_weak in page.get_result()


def test_can_reach_too_weak(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("can_reach")
    page.choose_rating("too_weak")

    assert constants.EXPECTED_can_achieve_too_weak in page.get_result()


def test_required_avg_excellent(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("required_avg")
    page.choose_rating("excellent")

    assert constants.EXPECTED_What_average_GPA_I_need_excellent in page.get_result()

def test_required_avg_very_good(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("required_avg")
    page.choose_rating("very_good")

    assert constants.EXPECTED_What_average_GPA_I_need_very_good in page.get_result()

def test_required_avg_good(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("required_avg")
    page.choose_rating("good")

    assert constants.EXPECTED_What_average_GPA_I_need_good in page.get_result()

def test_required_avg_accepted(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("required_avg")
    page.choose_rating("accepted")

    assert constants.EXPECTED_What_average_GPA_I_need_accepted in page.get_result()

def test_required_avg_weak(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("required_avg")
    page.choose_rating("weak")

    assert constants.EXPECTED_What_average_GPA_I_need_weak in page.get_result()

def test_required_avg_too_weak(driver_with_input):
    page = AnalysisPage(driver_with_input)

    page.choose_question("required_avg")
    page.choose_rating("too_weak")

    assert constants.EXPECTED_What_average_GPA_I_need_too_weak in page.get_result()
