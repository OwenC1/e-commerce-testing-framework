# page_objects/cart_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    # Locators - these are specific to the Cart page
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    REMOVE_BUTTON = (By.XPATH, "//button[text()='Remove']")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    
    def __init__(self, driver):
        # Reusing code: This constructor calls the parent BasePage constructor
        super().__init__(driver)
    
    def proceed_to_checkout(self):
        # Reusing code: This uses the click method from BasePage
        self.click(self.CHECKOUT_BUTTON)
    
    def continue_shopping(self):
        # Reusing code: This uses the click method from BasePage
        self.click(self.CONTINUE_SHOPPING_BUTTON)
    
    def remove_item(self, item_index=0):
        # New code: This is specific to the cart page functionality
        remove_buttons = self.driver.find_elements(*self.REMOVE_BUTTON)
        if len(remove_buttons) > item_index:
            remove_buttons[item_index].click()
    
    def get_cart_items(self):
        # New code: This provides cart-specific functionality
        items = self.driver.find_elements(*self.CART_ITEMS)
        cart_contents = []
        
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
            cart_contents.append({"name": name, "price": price})
            
        return cart_contents
    
    def get_total_price(self):
        # New code: Calculate the total price of items in cart
        items = self.get_cart_items()
        total = 0
        
        for item in items:
            # Convert price from "$29.99" format to float
            price = float(item["price"].replace("$", ""))
            total += price
            
        return total