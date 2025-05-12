def test_product_displayed(inventory_page):
    """
    Verify that a specific product is displayed on the inventory page.
    """
    product_name = "Sauce Labs Backpack"
    assert inventory_page.is_product_displayed(product_name), f"{product_name} is not displayed on the inventory page."
