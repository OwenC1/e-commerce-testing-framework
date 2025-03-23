# page_objects/inventory_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
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
         # Find the dropdown element
         sort_dropdown = self.find_element(self.SORT_DROPDOWN)
         # Use Select class to handle the dropdown properly
         select = Select(sort_dropdown)
         # Select by visible text
         select.select_by_visible_text(sort_option)
        

    def add_item_to_cart(self, item_name):
        """Find an item by name and add it to the cart"""
        print(f"Looking for item: {item_name}")
    
        # Wait for the inventory container to be visible
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_container")))
        
        # Try a simpler selector first
        button_id = f"add-to-cart-sauce-labs-backpack"
        if item_name == "Sauce Labs Backpack":
            print(f"Using direct button ID: {button_id}")
            add_button = self.driver.find_element(By.ID, button_id)
            self.click(add_button)
            return
        
        # If it's not the backpack, use a more dynamic approach
        # Use a more precise XPath that matches the current structure of the site
        item_xpath = f"//div[contains(@class, 'inventory_item_name') and text()='{item_name}']/ancestor::div[contains(@class, 'inventory_item')]"
        print(f"Using XPath: {item_xpath}")
        
        item_container = self.driver.find_element(By.XPATH, item_xpath)
        add_button = item_container.find_element(By.XPATH, ".//button[contains(@id, 'add-to-cart')]")
        self.click(add_button)

    def get_cart_count(self):
        try:
            return self.get_text(self.CART_BADGE)
        except:
            return "0"

    def go_to_cart(self):
         """Click the cart icon and navigate to the cart page"""
         self.click(self.CART_LINK)  # Assuming CART_LINK is defined in your InventoryPage
         from .cart_page import CartPage
         return CartPage(self.driver)
        
    def get_first_product_name(self):
        """Get the name of the first product in the listing"""
        first_product = self.find_element((By.CLASS_NAME, "inventory_item_name"))
        return first_product.text

    def get_all_product_prices(self):
        """Get a list of all product prices as floats"""
        price_elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    
    # Convert price text (e.g., "$29.99") to float (29.99)
        prices = []
        for elem in price_elements:
            price_text = elem.text.replace("$", "")
            prices.append(float(price_text))
    
        return prices
    
    def view_product_details(self, product_name):
         """
         Click on a product name to view its details.
    
         Args:
            product_name: The name of the product to view
         """
        # Locate the product name element using XPath
         product_link_locator = (By.XPATH, f"//div[contains(@class, 'inventory_item_name') and text()='{product_name}']")
    
        # Use the click method from BasePage
         self.click(product_link_locator)