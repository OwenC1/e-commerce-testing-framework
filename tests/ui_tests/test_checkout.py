import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from page_objects.login_page import LoginPage
from page_objects.inventory_page import InventoryPage
from page_objects.cart_page import CartPage
from page_objects.checkout_page import CheckoutPage
from page_objects.checkout_complete_page import CheckoutCompletePage

class TestCheckout:
    @pytest.fixture
    def setup_checkout(self, browser, env, test_data):  # Changed driver to browser
        # Login
        login_page = LoginPage(browser)
        login_page.navigate(env.base_url)
        user = test_data.get_user_credentials('valid_user')
        login_page.login(user['username'], user['password'])
    
        # Wait for inventory page to load
        WebDriverWait(browser, 10).until(
           EC.url_contains("inventory.html")
        )
    
        # Add item to cart with extra reliability
        inventory_page = InventoryPage(browser)
        product = test_data.get_product_details('backpack')
        inventory_page.add_item_to_cart(product['name'])
    
        # Go to cart with extra wait
        try:
            # Click cart link with JavaScript
            cart_link = WebDriverWait(browser, 10).until(
               EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
            )
            browser.execute_script("arguments[0].click();", cart_link)
        
            # Wait for cart page
            WebDriverWait(browser, 10).until(
               EC.url_contains("cart.html")
            )
        
            print(f"Navigated to cart: {browser.current_url}")
        except Exception as e:
            print(f"Error in setup_checkout: {e}")
            browser.save_screenshot("setup_checkout_error.png")
            raise
    
        return browser, test_data  # Return browser, not driver
    
    def test_successful_checkout(self, browser, env, test_data, setup_checkout):
        # Get setup datas
        driver, test_data = setup_checkout
        
        # Proceed from cart to checkout
        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()
        
        # Enter customer information and continue
        checkout_page = CheckoutPage(driver)
        customer = test_data.get_data('customers', 'standard_customer')
        checkout_page.enter_customer_info(
            customer['first_name'], 
            customer['last_name'], 
            customer['zip_code']
        )
        checkout_page.continue_checkout()
        
        # Complete checkout
        checkout_page.finish_checkout()
        
        # Verify order confirmation
        complete_page = CheckoutCompletePage(driver)
        confirmation_message = complete_page.get_confirmation_message()
        assert "Thank you for your order" in confirmation_message