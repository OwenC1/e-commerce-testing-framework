import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# Use webdriver_manager to handle driver installation
from webdriver_manager.chrome import ChromeDriverManager
from page_objects.login_page import LoginPage
from page_objects.inventory_page import InventoryPage
from config.environment import Environment


# ----------------------------
# Custom CLI options for pytest
# These let you switch between local and BrowserStack easily
# Example: pytest --use_browserstack --browser chrome
# ----------------------------
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
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run in headless mode")


# Hook to capture test status for screenshots
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def env():
    """Return the environment configuration"""
    return Environment()


# ----------------------------
# Main browser fixture
# Creates a WebDriver instance (local or BrowserStack)
# ----------------------------
@pytest.fixture(scope="function")
def browser(request, env):
    use_browserstack = request.config.getoption("--use_browserstack")
    headless = request.config.getoption("--headless")

    # If running on BrowserStack
    if use_browserstack:
        browserstack_username = os.getenv("BROWSERSTACK_USERNAME")
        browserstack_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

        capabilities = {
            "browserName": request.config.getoption("--browser"),
            "browserVersion": request.config.getoption("--browser_version"),
            "bstack:options": {
                "os": request.config.getoption("--os"),
                "osVersion": request.config.getoption("--os_version"),
                "projectName": "E-Commerce Testing Framework",
                "buildName": "Build 1.0",
                "sessionName": "Test Run",
                "local": "false",
                "seleniumVersion": "4.0.0",
                "debug": "true",
                "networkLogs": "true",
                "consoleLogs": "info"
            }
        }

        # BrowserStack remote URL with credentials
        url = f"https://{browserstack_username}:{browserstack_access_key}@hub-cloud.browserstack.com/wd/hub"
        driver = webdriver.Remote(command_executor=url, desired_capabilities=capabilities)

    else:
        # Local Chrome WebDriver configuration
        options = Options()
        # Optional: Only set binary_location if Chrome is not in standard location
        # Use the actual path to Chrome on your machine if needed
        # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if headless:
            options.add_argument("--headless=new")  # Updated headless flag for newer Chrome versions
        options.add_argument("--window-size=1920,1080")
        
        try:
            # Use WebDriver Manager to install ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"Error creating Chrome driver with WebDriverManager: {e}")
            # Fallback to default Chrome driver
            driver = webdriver.Chrome(options=options)

    # Maximize browser window
    driver.maximize_window()
    
    # Set implicit wait from environment config
    driver.implicitly_wait(env.timeout)

    # Yield WebDriver instance to tests
    yield driver

    # Take screenshot on failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_dir = env.get_screenshot_dir()
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{request.node.name}.png")
        try:
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

    # Quit browser after tests finish
    driver.quit()


# ----------------------------
# Base fixture: Open home page
# ----------------------------
@pytest.fixture
def setup(browser, env):
    """
    Setup for each test - navigates to the website.
    """
    browser.get(env.base_url)
    return browser


# ----------------------------
# Fixture: Login and return browser
# Useful for tests that need to start from a logged-in state
# ----------------------------
@pytest.fixture
def logged_in_browser(browser, env):
    """
    Setup for tests requiring logged in state.
    """
    browser.get(env.base_url)
    login_page = LoginPage(browser)
    
    # Get credentials from environment
    user_creds = env.get_credentials('standard_user')
    username = user_creds.get('username', 'standard_user')
    password = user_creds.get('password', 'secret_sauce')
    
    login_page.login(username, password)
    
    # Verify login was successful
    WebDriverWait(browser, env.timeout).until(
        EC.url_contains("inventory.html")
    )
    
    return browser


# ----------------------------
# Fixture: Login and return InventoryPage object
# Reusable across multiple tests
# ----------------------------
@pytest.fixture
def inventory_page(logged_in_browser):
    """
    Initialize the inventory page after login.
    This fixture provides a pre-configured InventoryPage object.
    """
    return InventoryPage(logged_in_browser)


# ----------------------------
# Fixture: Test data manager
# ----------------------------
@pytest.fixture(scope="session")
def test_data():
    """Fixture to provide test data"""
    from test_data.test_data import DataManager
    return DataManager()