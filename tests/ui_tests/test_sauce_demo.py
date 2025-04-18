import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.login_page import LoginPage
from page_objects.inventory_page import InventoryPage
from test_data.test_data import DataManager
from config.environment import Environment  # Add this import

class TestSauceDemo:
    @pytest.fixture(scope="session")
    def env(self):
        return Environment()

    @pytest.fixture
    def driver(self, env, request):  # Add request parameter
        browser_options = env.get_browser_options()
        driver = webdriver.Chrome(options=browser_options)
        driver.maximize_window()
        driver.implicitly_wait(env.timeout)
        yield driver
        
        # Take screenshot on failure using request instead of pytest.current_test
        if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
            screenshot_path = os.path.join(
                env.get_screenshot_dir(), 
                f"{request.node.name}.png"
            )
            driver.save_screenshot(screenshot_path)
        
        driver.quit()

    @pytest.fixture
    def test_data(self):
        return DataManager()

    def test_valid_login(self, driver, env, test_data):
        login_page = LoginPage(driver)
        login_page.navigate(env.base_url)  # Pass base_url here
        
        user = test_data.get_user_credentials('valid_user')
        login_page.login(user['username'], user['password'])
        
        inventory_page = InventoryPage(driver)
        assert inventory_page.get_title() == "Products"

    def test_locked_out_user(self, driver, env, test_data):  # Add env parameter
        login_page = LoginPage(driver)
        login_page.navigate(env.base_url)  # Pass base_url here
        
        user = test_data.get_user_credentials('locked_user')
        login_page.login(user['username'], user['password'])
        assert "locked out" in login_page.get_error_message()

    def test_add_multiple_items_to_cart(self, driver, env, test_data):  # Add env parameter
        # Login first
        login_page = LoginPage(driver)
        login_page.navigate(env.base_url)  # Pass base_url here
        user = test_data.get_user_credentials('valid_user')
        login_page.login(user['username'], user['password'])
        
        # Add items to cart
        inventory_page = InventoryPage(driver)
        cart_items = test_data.get_cart_scenario('multiple_items')
        
        for item_key in cart_items:
            product = test_data.get_product_details(item_key)
            inventory_page.add_item_to_cart(product['name'])
        
        assert inventory_page.get_cart_count() == str(len(cart_items))

    @pytest.mark.parametrize("sort_option", DataManager().get_sort_options())
    def test_sort_products(self, driver, env, test_data, sort_option):  # Add env parameter
        # Login first
        login_page = LoginPage(driver)
        login_page.navigate(env.base_url)  # Pass base_url here
        user = test_data.get_user_credentials('valid_user')
        login_page.login(user['username'], user['password'])
        
        # Test sorting
        inventory_page = InventoryPage(driver)
        inventory_page.sort_products(sort_option)

    def test_logout(self, browser, env, test_data):  # If this is a class method, keep self
        """Test logout functionality"""
        # Login first
        login_page = LoginPage(browser)
        login_page.navigate(env.base_url)
        user = test_data.get_user_credentials('valid_user')
        login_page.login(user['username'], user['password'])
    
        # Verify we're logged in
        WebDriverWait(browser, 10).until(
           EC.url_contains("inventory.html")
        )
        print("Logged in successfully")
    
        # Click menu button with JavaScript for reliability
        menu_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
        )
        browser.execute_script("arguments[0].click();", menu_button)
        print("Clicked menu button")
    
        # Wait for menu to fully open
        time.sleep(1)
    
        # Click logout with JavaScript
        logout_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        browser.execute_script("arguments[0].click();", logout_link)
        print("Clicked logout link")
    
        # Wait for redirect to complete
        time.sleep(1)
    
        # Verify we're back at login page
        try:
           # Check URL first
           WebDriverWait(browser, 10).until(
              lambda driver: "saucedemo.com" in driver.current_url and 
                          ("index.html" in driver.current_url or 
                           driver.current_url.endswith("/"))
            )
           print(f"Redirected to: {browser.current_url}")
        
            # Then check for login button
           login_button = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.ID, "login-button"))
            )
           assert login_button.is_displayed()
           print("Login button found, logout successful")
        except Exception as e:
            print(f"Logout verification failed: {e}")
            browser.save_screenshot("logout_failure.png")
            raise

    def test_update_cart_quantity(self, driver, env, test_data):
        """Test updating item quantity in cart"""
        # Login first
        login_page = LoginPage(driver)
        login_page.navigate(env.base_url)
        login_page.login("standard_user", "secret_sauce")
        
        # Add item to cart and update quantity
        inventory_page = InventoryPage(driver)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")
        inventory_page.add_item_to_cart("Sauce Labs Bike Light")
        
        WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "2")
        )
        
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        print(f"Cart badge shows: {cart_badge.text}")
        assert cart_badge.text == "2"

        # echo "# Adding a comment to test hook" >> tests/ui_tests/test_sauce_demo.py
        # echo "practicing git worflow"
