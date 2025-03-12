# tests/ui_tests/test_product_filtering.py

import pytest
from selenium.webdriver.common.by import By
from page_objects.inventory_page import InventoryPage

class TestProductFiltering:
    """
    This class demonstrates equivalence partitioning and boundary value analysis 
    for product filtering functionality.
    """
    
    @pytest.fixture
    def inventory_page(self, setup):
        """Initialize the inventory page after login"""
        driver = setup
        driver.get("https://www.saucedemo.com/")
        # Log in with standard user
        from page_objects.login_page import LoginPage
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        return InventoryPage(driver)
    
    # Equivalence Partitioning for product filtering
    @pytest.mark.parametrize("sort_option,expected_first_product", [
        # Partition 1: Alphabetical sorting (A to Z)
        ("az", "Sauce Labs Backpack"),
        # Partition 2: Alphabetical sorting (Z to A)
        ("za", "Test.allTheThings() T-Shirt (Red)"),
        # Partition 3: Price sorting (low to high)
        ("lohi", "Sauce Labs Onesie"),
        # Partition 4: Price sorting (high to low)
        ("hilo", "Sauce Labs Fleece Jacket")
    ])
    def test_product_sorting_equivalence_partitioning(self, inventory_page, sort_option, expected_first_product):
        """Test different equivalence classes for product sorting"""
        # Implement a method to select sort option by value
        inventory_page.sort_products(sort_option)
        
        # Get the name of the first product after sorting
        first_product_name = inventory_page.get_first_product_name()
        
        # Verify sorting worked correctly
        assert first_product_name == expected_first_product, \
            f"Expected first product to be {expected_first_product}, but got {first_product_name}"
    
    # Boundary Value Analysis for product prices
    @pytest.mark.parametrize("price_threshold,expected_count", [
        # Lower boundary: $0.00 (should include all products)
        (0.00, 0),
        # Just inside boundary: $7.99 (should include 1 product)
        (7.99, 1),
        # Middle value: $15.99 (should include 3 products)
        (15.99, 4),
        # Upper boundary: $49.99 (should include all products)
        (49.99, 6),
        # Outside upper boundary: $50.00 (should include all products)
        (50.00, 6)
    ])
    def test_product_price_boundary_analysis(self, inventory_page, price_threshold, expected_count):
        """
        Test boundary values for product prices.
        This checks how many products are below or equal to the given price threshold.
        """
        # Get all product prices
        product_prices = inventory_page.get_all_product_prices()
        
        # Count products below or equal to threshold
        products_within_threshold = [
            price for price in product_prices if price <= price_threshold
        ]
        
        # Verify count matches expectation
        assert len(products_within_threshold) == expected_count, \
            f"Expected {expected_count} products at or below ${price_threshold:.2f}, " \
            f"but found {len(products_within_threshold)}"