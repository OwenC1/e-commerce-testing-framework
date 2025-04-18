# page_objects/inventory_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from .base_page import BasePage
import time

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

    # Then fix the sort_products method
    def sort_products(self, sort_option):
        """Sort products using the dropdown"""
        try:
           # Wait for the dropdown to be clickable
           sort_dropdown = WebDriverWait(self.driver, 10).until(
               EC.element_to_be_clickable(self.SORT_DROPDOWN)
            )
        
            # Use Select class
           select = Select(sort_dropdown)
        
            # Map values
           value_map = {
                "az": "az", 
                "za": "za",
                "lohi": "lohi",
                "hilo": "hilo",
                "Name (A to Z)": "az",
                "Name (Z to A)": "za",
                "Price (low to high)": "lohi",
                "Price (high to low)": "hilo"
            }
        
            # Try to find the correct value to select
           sort_value = value_map.get(sort_option, sort_option)
        
           try:
                select.select_by_value(sort_value)
           except Exception as select_error:
                print(f"Failed to select by value: {select_error}")
                try:
                    select.select_by_visible_text(sort_option)
                except Exception as text_error:
                    print(f"Failed to select by text: {text_error}")
        
            # Allow time for sort to complete
           time.sleep(1)
        
        except Exception as e:
            print(f"Error sorting products: {e}")
            # Don't re-raise without an active exception
        

    def add_item_to_cart(self, item_name):
        """Find an item by name and add it to the cart"""
        print(f"Looking for item: {item_name}")

        # Wait for inventory page to load fully
        WebDriverWait(self.driver, 10).until(
           EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
        )

        try:
            # Construct direct button ID
            item_id = item_name.lower().replace(" ", "-")
            button_id = f"add-to-cart-{item_id}"
            print(f"Trying button ID: {button_id}")
        
            # Wait for button to be clickable
            add_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, button_id))
            )
        
             # Scroll to the button to ensure it's in view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        
              # Use JavaScript to click the button (more reliable)
            self.driver.execute_script("arguments[0].click();", add_button)
            print(f"Added {item_name} to cart")
        
             # Wait for cart badge to be visible or updated
            try:
                # Wait for the DOM to update
                time.sleep(0.5)
            
                # Don't refresh - that can cause issues
                # Instead, just wait for badge to be present
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
                )
            except:
                print("Note: Cart badge may not be visible yet")
            
        except Exception as e:
            print(f"Error adding item to cart: {e}")
            raise
        
        return self  # Allow method chaining

    def get_cart_count(self):
        try:
            return self.get_text(self.CART_BADGE)
        except:
            return "0"

    def go_to_cart(self):
        """Click the cart icon and navigate to the cart page"""
        try:
            # Find and click cart link
            cart_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CART_LINK)
            )
        
            # Use JavaScript for more reliable clicking
            self.driver.execute_script("arguments[0].click();", cart_link)
            print("Clicked cart icon")
        
            # Wait for cart page URL
            WebDriverWait(self.driver, 10).until(
               EC.url_contains("cart.html")
            )
        
            # Wait for page to fully load
            WebDriverWait(self.driver, 10).until(
               EC.presence_of_element_located((By.CLASS_NAME, "cart_contents_container"))
            )
        
            print(f"Navigated to cart: {self.driver.current_url}")
        
            # Wait for items to load
            time.sleep(1)
        
            from .cart_page import CartPage
            return CartPage(self.driver)
        except Exception as e:
            print(f"Error navigating to cart: {e}")
            self.driver.save_screenshot("cart_navigation_error.png")
            raise

        
    def get_first_product_name(self):
        """Get the name of the first product in the listing"""
        first_product = self.find_element((By.CLASS_NAME, "inventory_item_name"))
        return first_product.text

    def get_all_product_prices(self):
        """Get a list of all product prices as floats"""
        try:
            # Wait for products to be visible
            self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item")))
        
            # Get price elements
            price_elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
            print(f"Found {len(price_elements)} price elements")
        
            # Extract prices
            prices = []
            for elem in price_elements:
                price_text = elem.text.replace("$", "")
                try:
                   prices.append(float(price_text))
                except ValueError as e:
                   print(f"Error converting price '{price_text}': {e}")
        
            print(f"Extracted prices: {prices}")
            return prices
        except Exception as e:
            print(f"Error getting product prices: {e}")
            return []
    
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