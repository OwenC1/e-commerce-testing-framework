import pytest
from selenium.webdriver.common.by import By
from page_objects.login_page import LoginPage
from page_objects.inventory_page import InventoryPage

class TestProductDetails:
    """Tests for the product details functionality"""
    
    def test_view_product_details(self, browser, env, test_data):
        """
        Test that a user can view product details.
        
        This test verifies:
        1. User can navigate to the inventory page
        2. User can click on a product name
        3. Product details page loads with correct information
        """
        # --- ARRANGE ---
        # Start by navigating to the site and logging in
        login_page = LoginPage(browser)
        login_page.navigate(env.base_url)
        
        # Get user credentials from test data
        user = test_data.get_user_credentials('valid_user')
        login_page.login(user['username'], user['password'])
        
        # --- ACT ---
        # Once logged in, we should be on the inventory page
        inventory_page = InventoryPage(browser)
        
        # Select a specific product to test with
        product_name = "Sauce Labs Backpack"
        
        # Click on the product name to view details
        # For this test, we might need to add a new method to the InventoryPage class
        inventory_page.view_product_details(product_name)
        
        # --- ASSERT ---
        # Verify we're on the correct page
        # First, check the URL contains the expected pattern
        assert "inventory-item.html" in browser.current_url
        
        # Check that the product name is displayed correctly
        product_title = browser.find_element(By.CLASS_NAME, "inventory_details_name").text
        assert product_title == product_name
        
        # Verify that product has a description
        product_description = browser.find_element(By.CLASS_NAME, "inventory_details_desc").text
        assert product_description != ""
        
        # Verify that product has a price
        product_price = browser.find_element(By.CLASS_NAME, "inventory_details_price").text
        assert "$" in product_price
        
        # Verify that the "Add to cart" button is present
        add_to_cart_button = browser.find_element(By.CSS_SELECTOR, "button[id^='add-to-cart']")
        assert add_to_cart_button.is_displayed()