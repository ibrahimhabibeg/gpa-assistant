from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):

    HERO_HEADING = (By.ID, "hero-heading")
    HERO_SUBTITLE = (By.ID, "hero-subtitle")

    PROGRAM_INPUT = (By.ID, "program-hours-input")
    NON_GPA_INPUT = (By.ID, "non-gpa-hours-input")

    FILE_INPUT = (By.ID, "file-input")
    GITHUB_LINK = (By.ID, "github-link")
    
    UPLOAD_SUCCESS = (By.ID, "upload-status-success")
    UPLOAD_FILENAME = (By.ID, "upload-success-filename")
    UPLOAD_HEADING  = (By.ID, "upload-success-heading")

    def get_heading_text(self):
        return self.get_text(*self.HERO_HEADING)

    def is_subtitle_visible(self):
        return self.find(*self.HERO_SUBTITLE).is_displayed()

    def set_program_hours(self, value):
        el = self.find(*self.PROGRAM_INPUT)
        el.clear()
        el.send_keys(value)

    def get_program_hours(self):
        return self.find(*self.PROGRAM_INPUT).get_attribute("value")

    def get_upload_success(self):
        return self.find(*self.UPLOAD_SUCCESS)
    
    def get_upload_file_name(self):
        return self.find(*self.UPLOAD_FILENAME)
    
    def get_upload_heading(self):
        return self.find(*self.UPLOAD_HEADING)
    
    def set_non_gpa_hours(self, value):
        el = self.find(*self.NON_GPA_INPUT)
        el.clear()
        el.send_keys(value)

    def get_non_gpa_hours(self):
        return self.find(*self.NON_GPA_INPUT).get_attribute("value")

    def upload_file(self, path):
        self.find(*self.FILE_INPUT).send_keys(path)

    def open_github(self):
        link =self.find(*self.GITHUB_LINK)
        link.click()
        self.driver.switch_to.window(self.driver.window_handles[1])