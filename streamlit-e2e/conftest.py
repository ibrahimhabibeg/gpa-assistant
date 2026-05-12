from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import os


BASE_URL = "http://localhost:8501"

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

@pytest.fixture
def driver_with_input():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    file_path = os.path.abspath("tests/e2e/test_files/MyU.html")

    file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='stFileUploaderDropzoneInput']")))

    file_input.send_keys(file_path)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".st-key-parse_transcript_button")))

    send_button = WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.CSS_SELECTOR, ".st-key-parse_transcript_button button") ))
    send_button.click()

    yield driver
    driver.quit()