import pytest
from page_objects.login_page import LoginPage
from page_objects.inventory_page import InventoryPage
from page_objects.cart_page import CartPage
from page_objects.checkout_page import CheckoutPage
from page_objects.checkout_complete_page import CheckoutCompletePage

class TestCheckout:
    @pytest.fixture
    def setup_checkout(self, driver, env, test_data):
        # Login
        login_page = LoginPage(driver)
        login_page.navigate(env.base_url)
        user = test_data.get_user_credentials('valid_user')
        login_page.login(user['username'], user['password'])
        
        # Add item to cart
        inventory_page = InventoryPage(driver)
        product = test_data.get_product_details('backpack')
        inventory_page.add_item_to_cart(product['name'])
        
        # Go to cart
        inventory_page.go_to_cart()
        
        return driver, test_data
    
    def test_successful_checkout(self, driver, env, test_data, setup_checkout):
        # Get setup data
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
        assert "THANK YOU FOR YOUR ORDER" in confirmation_message