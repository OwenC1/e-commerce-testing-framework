# page_objects/checkout_complete_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutCompletePage(BasePage):
    # Locators
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_confirmation_message(self):
        return self.get_text(self.COMPLETE_HEADER)
    
    def back_to_products(self):
        self.click(self.BACK_HOME_BUTTON)