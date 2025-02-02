import pytest
from selenium import webdriver
from page_objects.login_page import LoginPage
from page_objects.inventory_page import InventoryPage
from test_data.test_data import DataManager
from config.environment import Environment

class TestSauceDemo:
    @pytest.fixture(scope="session")
    def env(self):
        return Environment()

    @pytest.fixture
    def driver(self, env, request):  # Add request parameter
        browser_options = env.get_browser_options()
        driver = webdriver.Chrome(options=browser_options)
        driver.maximize_window()
        driver.implicitly_wait(env.timeout)
        yield driver
        
        # Take screenshot on failure using request instead of pytest.current_test
        if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
            screenshot_path = os.path.join(
                env.get_screenshot_dir(), 
                f"{request.node.name}.png"
            )
            driver.save_screenshot(screenshot_path)
        
        driver.quit()

    @pytest.fixture
    def test_data(self):
        return DataManager()

    def test_valid_login(self, driver, env, test_data):
        login_page = LoginPage(driver)
        login_page.navigate(env.base_url)  # Pass base_url here
        
        user = test_data.get_user_credentials('valid_user')
        login_page.login(user['username'], user['password'])
        
        inventory_page = InventoryPage(driver)
        assert inventory_page.get_title() == "Products"

    def test_locked_out_user(self, driver, env, test_data):  # Add env parameter
        login_page = LoginPage(driver)
        login_page.navigate(env.base_url)  # Pass base_url here
        
        user = test_data.get_user_credentials('locked_user')
        login_page.login(user['username'], user['password'])
        assert "locked out" in login_page.get_error_message()

    def test_add_multiple_items_to_cart(self, driver, env, test_data):  # Add env parameter
        # Login first
        login_page = LoginPage(driver)
        login_page.navigate(env.base_url)  # Pass base_url here
        user = test_data.get_user_credentials('valid_user')
        login_page.login(user['username'], user['password'])
        
        # Add items to cart
        inventory_page = InventoryPage(driver)
        cart_items = test_data.get_cart_scenario('multiple_items')
        
        for item_key in cart_items:
            product = test_data.get_product_details(item_key)
            inventory_page.add_item_to_cart(product['name'])
        
        assert inventory_page.get_cart_count() == str(len(cart_items))

    @pytest.mark.parametrize("sort_option", DataManager().get_sort_options())
    def test_sort_products(self, driver, env, test_data, sort_option):  # Add env parameter
        # Login first
        login_page = LoginPage(driver)
        login_page.navigate(env.base_url)  # Pass base_url here
        user = test_data.get_user_credentials('valid_user')
        login_page.login(user['username'], user['password'])
        
        # Test sorting
        inventory_page = InventoryPage(driver)
        inventory_page.sort_products(sort_option)