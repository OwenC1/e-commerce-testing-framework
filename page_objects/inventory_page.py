# page_objects/inventory_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class InventoryPage(BasePage):
    # Locators
    TITLE = (By.CLASS_NAME, "title")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        super().__init__(driver)

    def get_title(self):
        return self.get_text(self.TITLE)

    def sort_products(self, sort_option):
        sort_dropdown = self.find_element(self.SORT_DROPDOWN)
        sort_dropdown.click()
        option = (By.XPATH, f"//option[text()='{sort_option}']")
        self.click(option)

    def add_item_to_cart(self, item_name):
        item_button = (By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button")
        self.click(item_button)

    def get_cart_count(self):
        try:
            return self.get_text(self.CART_BADGE)
        except:
            return "0"

    def go_to_cart(self):
        self.click(self.CART_LINK)