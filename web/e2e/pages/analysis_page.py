from selenium.webdriver.common.by import By
from .base_page import BasePage

class AnalysisPage(BasePage):

    BTN_CAN_REACH = (By.ID, "question-btn-can-reach")
    BTN_REQUIRED_AVG = (By.ID, "question-btn-required-avg")

    RATING = {
        "excellent": (By.ID, "rating-btn-excellent"),
        "good": (By.ID, "rating-btn-good"),
        "very_good": (By.ID, "rating-btn-very-good"),
        "accepted": (By.ID, "rating-btn-accepted"),
        "weak": (By.ID, "rating-btn-weak"),
        "too_weak": (By.ID, "rating-btn-too-weak"),
    }

    RESULT = (By.ID, "analysis-result-text")

    def choose_question(self, question):
        if question == "can_reach":
            self.click(*self.BTN_CAN_REACH)
        elif question == "required_avg":
            self.click(*self.BTN_REQUIRED_AVG)

    def choose_rating(self, rating):
        self.click(*self.RATING[rating])

    def get_result(self):
        return self.get_text(*self.RESULT)