# tests/ui_tests/test_element_practice.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from page_objects.login_page import LoginPage

def test_find_elements():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com")
    
    # Practice finding elements
    login_button = driver.find_element(By.ID, "login-button")
    #error_message = driver.find_element(By.XPATH, "//h3[@data-test='error']")

def login(self, username, password):
    self.input_text(self.USERNAME_INPUT, username)
    self.input_text(self.PASSWORD_INPUT, password)
    self.click(self.LOGIN_BUTTON)
    
    driver.quit()