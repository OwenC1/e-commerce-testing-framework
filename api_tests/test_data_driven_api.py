# api_tests/test_data_driven_api.py
import pytest
import requests
from test_data.data_reader import DataReader

class TestDataDrivenAPI:
    @pytest.fixture
    def api_data(self):
        """Fixture to load API test data"""
        return DataReader.load_data("api/user_data.json")
    
    @pytest.fixture
    def base_url(self):
        """Fixture to provide the base URL"""
        return "https://reqres.in/api"
    
    @pytest.mark.parametrize("user_data_index", [0, 1, 2])
    def test_create_user(self, api_data, base_url, user_data_index):
        """
        Test creating users with different data sets.
        
        This demonstrates how to use parametrized indices to access different
        data entries from our test data.
        """
        # Get user data for this test iteration
        user_data = api_data["create_users"][user_data_index]
        
        # Make the request with data from our test data file
        response = requests.post(
            f"{base_url}/users",
            json={
                "name": user_data["name"],
                "job": user_data["job"]
            }
        )
        
        # Verify response
        assert response.status_code == user_data["expected_status"]
        assert response.json()["name"] == user_data["name"]
        assert response.json()["job"] == user_data["job"]
    
    # Fixed parametrization to use actual user IDs instead of string characters
    @pytest.mark.parametrize("user_id", [1, 2, 3, 12, 23])
    def test_get_user(self, base_url, user_id):
        """
        Test retrieving different users by ID.
        
        This shows how to test different scenarios with a range of user IDs,
        some that exist and some that don't.
        """
        # Make request to get user details for this ID
        response = requests.get(f"{base_url}/users/{user_id}")
        
        # For existing users (1-12 in reqres), we expect success
        if 1 <= user_id <= 12:
            assert response.status_code == 200
            assert response.json()["data"]["id"] == user_id
        else:
            # For non-existent users, we expect 404
            assert response.status_code == 404
            
    def test_update_user(self, api_data, base_url):
        """
        Test updating a user's information.
        
        This demonstrates using data from the JSON file for request payload.
        """
        # Get update data from test data file
        update_data = api_data["update_user"]
        user_id = 2  # Using a known user ID
        
        # Make the update request
        response = requests.put(
            f"{base_url}/users/{user_id}",
            json=update_data
        )
        
        # Verify response
        assert response.status_code == 200
        assert response.json()["name"] == update_data["name"]
        assert response.json()["job"] == update_data["job"]
        
    # Example of a more advanced data-driven test
    @pytest.mark.parametrize("method,expected_code", [
        ("GET", 200),
        ("POST", 201),
        ("PUT", 200),
        ("DELETE", 204)
    ])
    def test_request_methods(self, base_url, method, expected_code):
        """
        Test different HTTP methods with expected status codes.
        
        This shows how to parametrize multiple values at once.
        """
        # Prepare request details based on method
        endpoint = f"{base_url}/users"
        payload = None
        
        if method in ["POST", "PUT"]:
            endpoint = f"{endpoint}/2" if method == "PUT" else endpoint
            payload = {"name": "Test User", "job": "Tester"}
        
        if method == "DELETE":
            endpoint = f"{endpoint}/2"
            
        # Execute the request dynamically based on method
        response = requests.request(method, endpoint, json=payload)
        
        # Verify correct response code
        assert response.status_code == expected_code