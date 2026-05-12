from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class HomePage(BasePage):
    HERO_HEADING = (By.CSS_SELECTOR, "h1#ibn-al-haitham-gpa-assistant")
    GITHUB_LINK = (By.LINK_TEXT, "ibrahimhabibeg/gpa-assistant")
    TRELLO_LINK = (By.CSS_SELECTOR, "a[href*='trello.com']")
    JIRA_LINK = (By.CSS_SELECTOR, "a[href*='atlassian.net']")

    PROGRAM_HOURS_INPUT = (By.CSS_SELECTOR, "input[aria-label='Program hours']")
    NON_GPA_HOURS_INPUT = (By.CSS_SELECTOR, "input[aria-label='Non GPA hours']")
    FILE_INPUT = (By.CSS_SELECTOR, "input[data-testid='stFileUploaderDropzoneInput']")
    PARSE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='stBaseButton-primary']")

    DROPDOWN_LIST = (By.CSS_SELECTOR, 'div[data-baseweb="select"] input')

    # HELP !
    SEMESTERS_METRIC = ""
    COURSES_METRIC = ""
    CURRENT_GPA_METRIC = ""

    def get_heading_text(self):
        return self.get_text(*self.HERO_HEADING)

    def _set_number_input(self, locator, value):
        el = self.find(*locator)
        el.click()
        el.send_keys(Keys.CONTROL + "a")  # it works so dont ask :)
        el.send_keys(str(value))

    def set_program_hours(self, value):
        self._set_number_input(self.PROGRAM_HOURS_INPUT, value)

    def get_program_hours(self):
        return self.find(*self.PROGRAM_HOURS_INPUT).get_attribute("value")

    def set_non_gpa_hours(self, value):
        self._set_number_input(self.NON_GPA_HOURS_INPUT, value)

    def get_non_gpa_hours(self):
        return self.find(*self.NON_GPA_HOURS_INPUT).get_attribute("value")

    def upload_file(self, path):
        self.find(*self.FILE_INPUT).send_keys(path)

    def click_parse(self):
        self.click(*self.PARSE_BUTTON)

    def get_semesters_count(self):
        return self.get_text(*self.SEMESTERS_METRIC)

    def get_courses_count(self):
        return self.get_text(*self.COURSES_METRIC)

    def get_current_gpa(self):
        return self.get_text(*self.CURRENT_GPA_METRIC)

    def open_github(self):
        self.find(*self.GITHUB_LINK).click()
        self.driver.switch_to.window(self.driver.window_handles[1])

    def open_trello(self):
        self.find(*self.TRELLO_LINK).click()
        self.driver.switch_to.window(self.driver.window_handles[1])

    def open_jira(self):
        self.find(*self.JIRA_LINK).click()
        self.driver.switch_to.window(self.driver.window_handles[1])
