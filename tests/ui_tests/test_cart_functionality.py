import pytest
from page_objects.inventory_page import InventoryPage
from page_objects.cart_page import CartPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestCartFunctionality:
    """Tests for the shopping cart functionality"""
    
    def test_add_and_remove_item(self, inventory_page):
        # Print the current URL to verify we're on the inventory page
        print(f"Current URL: {inventory_page.driver.current_url}")
        """
        Test that items can be added to the cart and then removed.
        
        This test verifies that:
        1. We can add a specific item to the cart
        2. The item appears correctly in the cart
        3. We can remove the item from the cart
        4. The cart is empty after removal
        """
        # Setup - decide which product to test with
        test_item = "Sauce Labs Backpack"
        
        # Add a breakpoint before adding the item to cart
        # breakpoint()
        
        # Add the item to the cart
        inventory_page.add_item_to_cart(test_item)
        
        # Add another breakpoint after adding to cart
        # breakpoint()
        
        
        # Navigate to the cart
        cart_page = inventory_page.go_to_cart()
        
        # Verify the item is in the cart
        cart_items = cart_page.get_cart_items()
        assert test_item in cart_items, f"Expected {test_item} to be in the cart, but found: {cart_items}"
        
        # Remove the item from the cart
        cart_page.remove_item(test_item)
        
        # Verify the cart is now empty
        updated_cart_items = cart_page.get_cart_items()
        assert len(updated_cart_items) == 0, f"Expected cart to be empty, but found: {updated_cart_items}"
        
        # Return to inventory page for potential further testing
        inventory_page = cart_page.continue_shopping()
        
        # Verify we're back at the inventory page (optional assertion)
        assert "inventory" in inventory_page.driver.current_url