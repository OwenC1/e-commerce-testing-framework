import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from page_objects.login_page import LoginPage
from page_objects.inventory_page import InventoryPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="session")
def browser():
    """
    Create a WebDriver instance for the entire test session.
    
    This fixture creates a single browser instance that will be reused across
    all tests in the session, which significantly improves test execution time.
    """
    options = Options()
    
    # Add additional options as needed
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Ensure the browser is visible and doesn't close automatically
    options.add_experimental_option("detach", True)  # Keep browser open after test
    
    # Make sure no headless mode is enabled
    options.add_argument("--window-size=1920,1080")  # Set a specific window size
    
    # Create the driver
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    
    # Yield the driver to tests
    yield driver
    
    # Quit the driver after all tests are complete
    driver.quit()

@pytest.fixture
def setup(browser):
    """
    Setup for each test - navigates to the website.
    
    This uses the session-scoped browser fixture but navigates
    to a fresh page for each test.
    """
    browser.get("https://www.saucedemo.com/")
    return browser

@pytest.fixture
def logged_in_browser(browser):
    """
    Setup for tests requiring logged in state.
    
    This fixture handles the login process to prepare the browser
    for tests that need to start from a logged-in state.
    """
    browser.get("https://www.saucedemo.com/")
    login_page = LoginPage(browser)
    login_page.login("standard_user", "secret_sauce")
    return browser

@pytest.fixture
def inventory_page(logged_in_browser):
    """
    Initialize the inventory page after login.
    
    This fixture provides a pre-configured InventoryPage object 
    that tests can use directly without handling login.
    """
    return InventoryPage(logged_in_browser)

@pytest.fixture
def inventory_page(browser):
    """Initialize the inventory page after login"""
    browser.get("https://www.saucedemo.com/")
    
    # Create login page and log in
    from page_objects.login_page import LoginPage
    login_page = LoginPage(browser)
    login_page.login("standard_user", "secret_sauce")
    
    # Verify we're on the inventory page
    WebDriverWait(browser, 10).until(
        EC.url_contains("inventory.html")
    )
    
    # Create and return the inventory page
    from page_objects.inventory_page import InventoryPage
    return InventoryPage(browser)

def pytest_addoption(parser):
    parser.addoption("--use_browserstack", action="store_true", default=False,
                     help="Run tests on BrowserStack")
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests on")
    parser.addoption("--browser_version", action="store", default="latest",
                     help="Browser version to use")
    parser.addoption("--os", action="store", default="Windows",
                     help="Operating system")
    parser.addoption("--os_version", action="store", default="10",
                     help="OS version")
    parser.addoption("--device", action="store", default=None,
                     help="Mobile device name (for mobile testing)")
    parser.addoption("--real_mobile", action="store_true", default=False,
                     help="Use real mobile device instead of emulator")
    parser.addoption("--resolution", action="store", default="1920x1080",
                     help="Screen resolution")

@pytest.fixture(scope="session")
def browser(request):
    use_browserstack = request.config.getoption("--use_browserstack")
    
    if use_browserstack:
        # BrowserStack configuration
        browserstack_username = os.environ.get("BROWSERSTACK_USERNAME")
        browserstack_access_key = os.environ.get("BROWSERSTACK_ACCESS_KEY")
        
        browser_name = request.config.getoption("--browser")
        browser_version = request.config.getoption("--browser_version")
        os_name = request.config.getoption("--os")
        os_version = request.config.getoption("--os_version")
        device = request.config.getoption("--device")
        real_mobile = request.config.getoption("--real_mobile")
        resolution = request.config.getoption("--resolution")
        
        # Build capabilities for BrowserStack
        capabilities = {}
        
        # For mobile testing
        if device:
            capabilities.update({
                'browserName': browser_name if browser_name != "chrome" else "chrome",
                'deviceName': device,
                'realMobile': 'true' if real_mobile else 'false',
                'osVersion': os_version,
            })
        # For desktop testing
        else:
            capabilities.update({
                'browserName': browser_name,
                'browserVersion': browser_version,
                'os': os_name,
                'osVersion': os_version,
                'resolution': resolution,
            })
        
        # Common capabilities
        capabilities.update({
            'projectName': 'E-Commerce Testing Framework',
            'buildName': 'Build 1.0',
            'sessionName': 'Test Run',
            'local': 'false',
            'seleniumVersion': '4.0.0',
            'debug': 'true',
            'networkLogs': 'true',
            'consoleLogs': 'info'
        })
        
        # BrowserStack URL with authentication
        url = f'https://{browserstack_username}:{browserstack_access_key}@hub-cloud.browserstack.com/wd/hub'
        
        # Create remote WebDriver instance
        options = webdriver.ChromeOptions()
        options.set_capability('bstack:options', capabilities)
        driver = webdriver.Remote(command_executor=url, options=options)
        
    else:
        # Local WebDriver (your existing implementation)
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
    
    yield driver
    driver.quit()