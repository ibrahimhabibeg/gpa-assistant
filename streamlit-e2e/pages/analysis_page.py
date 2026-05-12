from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


QUESTION_LABELS = {
    "max_gpa": (By.ID, ""),
    "max_rating":   (By.ID, ""),
    "can_reach":    (By.ID, ""),
    "required_avg": (By.ID, ""),
    "hypothetical": (By.ID, ""),
}

RATING_LABELS = {
    "excellent": (By.ID, ""),
    "good": (By.ID, ""),
    "very_good": (By.ID, ""),
    "accepted": (By.ID, ""),
    "weak": (By.ID, ""),
    "too_weak": (By.ID, ""),
}


class AnalysisPage(BasePage):

   class AnalysisPage(BasePage):

    QUESTION_SELECTBOX = (By.CSS_SELECTOR,"")

    RATING_SELECTBOX = (By.CSS_SELECTOR,"")

    HYPOTHETICAL_GPA_INPUT = (By.CSS_SELECTOR,"")

    RESULT_METRIC = (By.CSS_SELECTOR, "div[data-testid='stMetric']")
   

    def choose_question(self, question_key: str):
       return None


    def choose_rating(self, rating):
       return None

    def set_hypothetical_gpa(self, value):
     return None
