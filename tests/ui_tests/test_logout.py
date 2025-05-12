from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_logout_from_inventory(inventory_page):
    inventory_page.logout()

    # Assert the login page is shown again
    login_field = WebDriverWait(inventory_page.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    assert login_field.is_displayed()
