import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
                     help="Run in headless mode (used in CI or Docker)")

# ----------------------------
# Hook to capture test status
# Used to take screenshot on test failure
# ----------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

# ----------------------------
# Fixture: Return environment config
# Loads things like base URL, timeout, credentials
# ----------------------------
@pytest.fixture(scope="function")
def env():
    return Environment()

# ----------------------------
# Main fixture: Launch WebDriver
# Uses either local Chrome or BrowserStack depending on flag
# ----------------------------
@pytest.fixture(scope="function")
def browser(request, env):
    use_browserstack = request.config.getoption("--use_browserstack")
    headless = request.config.getoption("--headless")

    # --- BrowserStack mode ---
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

        url = f"https://{browserstack_username}:{browserstack_access_key}@hub-cloud.browserstack.com/wd/hub"
        driver = webdriver.Remote(command_executor=url, desired_capabilities=capabilities)

    # --- Local Chrome mode ---
    else:
        options = Options()

        # Docker/CI-safe Chrome options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--remote-debugging-port=9222")  # Required for Docker headless Chrome
        options.add_argument("--window-size=1920,1080")

        # Enable headless if passed as CLI arg
        if headless:
            options.add_argument("--headless=new")  # Modern headless mode

        # Try using WebDriver Manager to download correct chromedriver
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"[WebDriverManager FAILED]: {e}")
            driver = webdriver.Chrome(options=options)  # Fallback

    # Maximize window and set implicit wait
    driver.maximize_window()
    driver.implicitly_wait(env.timeout)

    # Yield the browser for the test
    yield driver

    # --- Teardown: Take screenshot if test failed ---
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_dir = env.get_screenshot_dir()
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{request.node.name}.png")
        try:
            driver.save_screenshot(screenshot_path)
            print(f"[Screenshot saved]: {screenshot_path}")
        except Exception as e:
            print(f"[Screenshot failed]: {e}")

    # Quit browser after test
    driver.quit()

# ----------------------------
# Base fixture: Open home page
# Opens the base URL defined in env config
# ----------------------------
@pytest.fixture
def setup(browser, env):
    browser.get(env.base_url)
    return browser

# ----------------------------
# Fixture: Login and return browser
# Use this when your test requires login first
# ----------------------------
@pytest.fixture
def logged_in_browser(browser, env):
    browser.get(env.base_url)
    login_page = LoginPage(browser)
    
    # Fetch username and password
    user_creds = env.get_credentials('standard_user')
    username = user_creds.get('username', 'standard_user')
    password = user_creds.get('password', 'secret_sauce')
    
    login_page.login(username, password)

    # Wait until redirected to inventory page
    WebDriverWait(browser, env.timeout).until(
        EC.url_contains("inventory.html")
    )
    return browser

# ----------------------------
# Fixture: Return InventoryPage object
# This allows tests to start from the logged-in inventory page
# ----------------------------
@pytest.fixture
def inventory_page(logged_in_browser):
    return InventoryPage(logged_in_browser)

# ----------------------------
# Fixture: Load shared test data
# Used for data-driven test cases
# ----------------------------
@pytest.fixture(scope="session")
def test_data():
    from test_data.test_data import DataManager
    return DataManager()
