# page_objects/cart_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    # Locators
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_BUTTON = (By.XPATH, "//button[text()='Remove']")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_cart_items(self):
        """Get all items currently in the cart"""
        items = self.driver.find_elements(*self.CART_ITEMS)
        return [item.find_element(*self.ITEM_NAME).text for item in items]
    
    def remove_item(self, item_name):
        """Remove a specific item from the cart"""
        # Find the cart item container that contains this item name
        item_xpath = f"//div[@class='cart_item'][.//div[@class='inventory_item_name' and text()='{item_name}']]"
        item_container = self.driver.find_element(By.XPATH, item_xpath)
        
        # Find and click the remove button within this container
        remove_button = item_container.find_element(*self.REMOVE_BUTTON)
        self.click(remove_button)
    
    def continue_shopping(self):
        """Click the continue shopping button and return to inventory page"""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        from .inventory_page import InventoryPage
        return InventoryPage(self.driver)
    
    def checkout(self):
        """Click the checkout button and proceed to checkout"""
        self.click(self.CHECKOUT_BUTTON)
        # Assuming we have a CheckoutPage class
        from .checkout_page import CheckoutPage
        return CheckoutPage(self.driver)