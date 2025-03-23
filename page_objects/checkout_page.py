# page_objects/checkout_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutPage(BasePage):
    # Locators
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    ZIP_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")
    
    # Step two locators
    FINISH_BUTTON = (By.ID, "finish")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def enter_customer_info(self, first_name, last_name, zip_code):
        self.input_text(self.FIRST_NAME_INPUT, first_name)
        self.input_text(self.LAST_NAME_INPUT, last_name)
        self.input_text(self.ZIP_CODE_INPUT, zip_code)
    
    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)
    
    def cancel_checkout(self):
        self.click(self.CANCEL_BUTTON)
    
    def finish_checkout(self):
        self.click(self.FINISH_BUTTON)
    
    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
    
    def get_item_total(self):
        total_text = self.get_text(self.ITEM_TOTAL)
        # Extract just the number from text like "Item total: $29.99"
        return float(total_text.split('$')[1])