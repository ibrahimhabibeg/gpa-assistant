from asyncio import wait

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
BASE_URL = "http://localhost:5173"

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
    file_path = os.path.abspath("test_files/MyU.html")

    file_input = driver.find_element(By.ID, "file-input")

    file_input.send_keys(file_path)
    yield driver
    driver.quit()

   