# tests/ui_tests/test_login.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin:
    @pytest.fixture
    def setup(self):
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        yield driver
        driver.quit()

    def test_valid_login(self, setup):
        driver = setup
        # Navigate to the website
        driver.get("https://www.saucedemo.com/")
        
        # Find elements and login
        username = driver.find_element(By.ID, "user-name")
        password = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")
        
        # Enter credentials
        username.send_keys("standard_user")
        password.send_keys("secret_sauce")
        login_button.click()
        
        # Verify successful login
        products_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        assert products_title.text == "Products"