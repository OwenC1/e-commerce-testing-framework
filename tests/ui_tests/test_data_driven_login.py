# tests/ui_tests/test_data_driven_login.py
import pytest
from selenium import webdriver
from page_objects.login_page import LoginPage
from test_data.data_reader import DataReader

class TestDataDrivenLogin:
    @pytest.fixture
    def login_data(self):
        """Fixture to load login test data"""
        return DataReader.load_data("ui/login_data.json")
    
    @pytest.fixture
    def driver(self):
        """Fixture to set up and tear down the WebDriver"""
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        driver.quit()
    
    @pytest.mark.parametrize("scenario", ["valid_login", "locked_user", "invalid_password", "empty_username", "empty_password"])
    def test_login_scenarios(self, driver, login_data, scenario):
        """
        Test different login scenarios using data-driven approach.
        
        This single test function can handle multiple test cases based on the
        scenario parameter and corresponding test data.
        """
        # Get the test data for this scenario
        data = login_data[scenario]
        
        # Set up login page
        login_page = LoginPage(driver)
        login_page.navigate("https://www.saucedemo.com")
        
        # Perform login with data from our test data file
        login_page.login(data["username"], data["password"])
        
        # Verify results based on expected outcome
        if data["expected_result"] == "success":
            # For successful login, we should be redirected
            assert data["expected_url"] in driver.current_url, f"Login should redirect to {data['expected_url']}"
        else:
            # For failed login, we should see an error message
            error_message = login_page.get_error_message()
            assert data["expected_error"] in error_message, f"Error message should contain '{data['expected_error']}'"