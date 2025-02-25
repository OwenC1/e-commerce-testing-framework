# api_tests/test_reqres_api.py

import pytest
import requests
import json
from datetime import datetime

class TestReqResAPI:
    """
    This class contains API tests for the ReqRes API service.
    We're testing basic CRUD (Create, Read, Update, Delete) operations.
    """
    BASE_URL = "https://reqres.in/api"

    def test_get_user_list(self):
        """
        Test retrieving a list of users from the API.
        This verifies we can successfully get user data and it's in the correct format.
        """
        # First, let's print what we're about to do
        print("\n🚀 Testing GET request to fetch user list...")

        # Make the request to the API
        response = requests.get(f"{self.BASE_URL}/users")
        
        # Print detailed information about what we received
        print("\n📥 Response Status Code:", response.status_code)
        print("\n📋 Response Headers:", json.dumps(dict(response.headers), indent=2))
        print("\n📦 Response Body:", json.dumps(response.json(), indent=2))
        
        # Now let's verify everything is correct
        assert response.status_code == 200, "Expected 200 OK status code"
        
        data = response.json()
        # Check the structure of our response
        assert "data" in data, "Response should contain 'data' key"
        assert "page" in data, "Response should contain page information"
        
        # Verify each user has the required fields
        for user in data["data"]:
            assert "id" in user, f"User {user} missing ID field"
            assert "email" in user, f"User {user} missing email field"
            assert "first_name" in user, f"User {user} missing first_name field"
            assert "last_name" in user, f"User {user} missing last_name field"

    def test_create_user(self):
        """
        Test creating a new user through the API.
        We'll send user data and verify the response contains the correct information.
        """
        print("\n🚀 Testing POST request to create new user...")

        # Prepare test data
        user_data = {
            "name": "John Doe",
            "job": "QA Engineer",
            "created_at": datetime.now().isoformat()
        }
        
        print("\n📤 Sending user data:", json.dumps(user_data, indent=2))
        
        # Send POST request to create user
        response = requests.post(
            f"{self.BASE_URL}/users",
            json=user_data
        )
        
        print("\n📥 Received response:", json.dumps(response.json(), indent=2))
        
        # Verify the response
        assert response.status_code == 201, f"Expected 201 Created status, got {response.status_code}"
        
        created_user = response.json()
        # Check if all our sent data is in the response
        assert created_user["name"] == user_data["name"], \
            f"Expected name to be {user_data['name']} but got {created_user['name']}"
        assert created_user["job"] == user_data["job"], \
            f"Expected job to be {user_data['job']} but got {created_user['job']}"
        
        # Verify we got an ID and creation timestamp
        assert "id" in created_user, "Response should include an ID"
        assert "createdAt" in created_user, "Response should include creation timestamp"

    def test_update_user(self):
        """
        Test updating an existing user's information.
        We'll update a user's details and verify the changes were saved.
        """
        print("\n🚀 Testing PUT request to update user...")

        user_id = 2  # We'll update user 2 as an example
        update_data = {
            "name": "Jane Smith",
            "job": "Senior QA Engineer"
        }
        
        print(f"\n📤 Sending update data for user {user_id}:", 
              json.dumps(update_data, indent=2))
        
        response = requests.put(
            f"{self.BASE_URL}/users/{user_id}",
            json=update_data
        )
        
        print("\n📥 Received response:", json.dumps(response.json(), indent=2))
        
        assert response.status_code == 200, f"Expected 200 OK status, got {response.status_code}"
        
        updated_user = response.json()
        assert updated_user["name"] == update_data["name"], \
            "Name should be updated in response"
        assert updated_user["job"] == update_data["job"], \
            "Job should be updated in response"
        assert "updatedAt" in updated_user, "Response should include update timestamp"

    def test_delete_user(self):
        """
        Test deleting a user from the system.
        We'll delete a user and verify they were removed successfully.
        """
        print("\n🚀 Testing DELETE request...")

        user_id = 3  # We'll delete user 3 as an example
        
        print(f"\n📤 Attempting to delete user {user_id}")
        
        response = requests.delete(f"{self.BASE_URL}/users/{user_id}")
        
        print(f"\n📥 Received status code: {response.status_code}")
        
        # For delete operations, we expect a 204 No Content response
        assert response.status_code == 204, \
            f"Expected 204 No Content status, got {response.status_code}"
            
    def test_get_single_user(self):
        """
        Test retrieving a single user's details from the API.
        This verifies we can get detailed information about a specific user.
        """
        # Use user ID 2 for testing
        user_id = 2
        
        # Make request to get user details
        response = requests.get(f"{self.BASE_URL}/users/{user_id}")
        
        # Verify successful response
        assert response.status_code == 200, "Should return 200 OK status"
        
        # Extract user data from response
        user_data = response.json()["data"]
        
        # Verify user structure
        assert user_data["id"] == user_id, "User ID should match requested ID"
        assert "email" in user_data, "User should have email"
        assert "first_name" in user_data, "User should have first name"
        assert "last_name" in user_data, "User should have last name"
        assert "avatar" in user_data, "User should have avatar URL"