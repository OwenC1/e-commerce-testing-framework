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
    
        # Wait for inventory page to load
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_container")))
    
        try:
          # Construct direct button ID dynamically
          item_id = item_name.lower().replace(" ", "-")
          button_id = f"add-to-cart-{item_id}"
          print(f"Trying direct button ID: {button_id}")
        
          add_button = WebDriverWait(self.driver, 5).until(
             EC.element_to_be_clickable((By.ID, button_id))
          )
          add_button.click()
          print("Clicked add-to-cart button using ID.")
    
        except Exception as e:
          print(f"Direct ID not found or not clickable: {e}")
          print("Falling back to XPath method.")
        
          # Fallback: locate item card and add-to-cart button using XPath
          item_xpath = f"//div[contains(@class, 'inventory_item_name') and text()='{item_name}']/ancestor::div[contains(@class, 'inventory_item')]"
        
          item_container = WebDriverWait(self.driver, 5).until(
             EC.presence_of_element_located((By.XPATH, item_xpath))
          )
          add_button = item_container.find_element(By.XPATH, ".//button[contains(@id, 'add-to-cart')]")
          add_button.click()
          print("Clicked add-to-cart button using XPath.")

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