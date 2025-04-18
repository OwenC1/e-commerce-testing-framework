# page_objects/cart_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage
import time
from page_objects.inventory_page import InventoryPage


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
        
        try:
            WebDriverWait(driver, 10).until(
                EC.url_contains("cart.html")
            )
        except Exception as e:
            print(f"Warning: Cart page URL check failed: {e}")
    
    def proceed_to_checkout(self):
        """Proceed to checkout page"""
        try:
            # Ensure we're on the cart page
            if "cart.html" not in self.driver.current_url:
                print(f"Warning: Not on cart page. Current URL: {self.driver.current_url}")
                # Try to navigate to cart first
                self.driver.get(self.driver.current_url.split("/cart.html")[0] + "/cart.html")
                WebDriverWait(self.driver, 10).until(
                   EC.url_contains("cart.html")
                )
        
            # Find and click checkout button
            checkout_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", checkout_button)
            print("Clicked checkout button")
        
            # Wait for checkout page to load
            WebDriverWait(self.driver, 10).until(
               EC.url_contains("checkout-step-one.html")
            )
            print(f"Navigated to checkout page: {self.driver.current_url}")
        
            # Wait for the form to be visible
            WebDriverWait(self.driver, 10).until(
               EC.visibility_of_element_located((By.ID, "first-name"))
            )
        except Exception as e:
            print(f"Error proceeding to checkout: {e}")
            self.driver.save_screenshot("checkout_navigation_error.png")
            raise
    
    def continue_shopping(self):
        # Reusing code: This uses the click method from BasePage
        """
        Click the continue shopping button and return to inventory page
        """
        try:
            # Find and click the continue shopping button
            continue_button = WebDriverWait(self.driver, 10).until(
               EC.element_to_be_clickable(self.CONTINUE_SHOPPING_BUTTON)
            )
        
             # Use JavaScript for more reliable clicking
            self.driver.execute_script("arguments[0].click();", continue_button)
            print("Clicked continue shopping button")
        
            # Wait for navigation to inventory page
            WebDriverWait(self.driver, 10).until(
               EC.url_contains("inventory.html")
            )
        
            print(f"Navigated back to inventory: {self.driver.current_url}")
        
            # Import here to avoid circular imports
            from .inventory_page import InventoryPage
            return InventoryPage(self.driver)
        except Exception as e:
            print(f"Error navigating back to inventory: {e}")
            self.driver.save_screenshot("continue_shopping_error.png")
            # If navigation fails, try direct URL
            try:
                self.driver.get(self.driver.current_url.replace("cart.html", "inventory.html"))
                WebDriverWait(self.driver, 10).until(
                   EC.url_contains("inventory.html")
                )
                print(f"Forced navigation to inventory page: {self.driver.current_url}")
                from .inventory_page import InventoryPage
                return InventoryPage(self.driver)
            except Exception as direct_error:
                print(f"Failed even with direct URL: {direct_error}")
                raise e
        
    
    def remove_item(self, item_name):
       #Removes an item from the cart using the item's name.
       # Example: "Sauce Labs Backpack" → "remove-sauce-labs-backpack"
       """Removes an item from the cart using the item's name."""
       # Convert name to ID for removal
       item_id = item_name.lower().replace(" ", "-")
       button_id = f"remove-{item_id}"
       try:
           # Find and click the remove button
           remove_button = WebDriverWait(self.driver, 10).until(
               EC.element_to_be_clickable((By.ID, button_id))
           )
        
            # Use JavaScript to click for reliability
           self.driver.execute_script("arguments[0].click();", remove_button)
           print(f"Removed item: {item_name}")
        
           # Important: Wait for the item to be removed from the DOM
           WebDriverWait(self.driver, 10).until_not(
              EC.presence_of_element_located((By.ID, button_id))
            )
        
            # Wait for any animations or updates to complete
           time.sleep(1)
        
            # Force a page refresh to ensure state is updated
           self.driver.refresh()
        
           # Wait for page to reload
           WebDriverWait(self.driver, 10).until(
               EC.presence_of_element_located((By.CLASS_NAME, "cart_contents_container"))
            )
        
       except Exception as e:
           print(f"Error removing item: {e}")
           self.driver.save_screenshot("remove_item_error.png")
           raise
    
    def get_cart_items(self):
        try:
            # Ensure we're on cart page
            WebDriverWait(self.driver, 10).until(
               EC.url_contains("cart.html")
            )
            print(f"Checking cart items on: {self.driver.current_url}")
        
            # Wait for cart page to fully load
            WebDriverWait(self.driver, 10).until(
               EC.visibility_of_element_located((By.CLASS_NAME, "cart_contents_container"))
            )
        
            # Try with a slight delay
            time.sleep(1)
        
            # Find all cart items
            items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
            print(f"Found {len(items)} cart items")
        
            if not items:
               # If no items found, check if page is truly empty or if there's an issue
               empty_cart = len(self.driver.find_elements(By.CLASS_NAME, "removed_cart_item")) > 0
               if empty_cart:
                   print("Cart appears to be empty (removed items found)")
               else:
                   print("No cart items found but cart doesn't appear empty")
                   # Take a screenshot for debugging
                   self.driver.save_screenshot("empty_cart_debug.png")
        
            cart_contents = []
            for item in items:
                try:
                    name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                    price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
                    print(f"Cart item: {name}, {price}")
                    cart_contents.append({"name": name, "price": price})
                except Exception as e:
                    print(f"Error getting cart item details: {e}")
        
            return cart_contents
        except Exception as e:
            print(f"Error getting cart items: {e}")
            self.driver.save_screenshot("cart_items_error.png")
            return []
    
    def get_total_price(self):
        # New code: Calculate the total price of items in cart
        items = self.get_cart_items()
        total = 0
        
        for item in items:
            # Convert price from "$29.99" format to float
            price = float(item["price"].replace("$", ""))
            total += price
            
        return total