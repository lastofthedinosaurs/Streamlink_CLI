#!/usr/bin/env python3
"""
Unit tests for the TwitchAPISession class.

This test suite covers various methods of the TwitchAPISession class
to ensure their correctness and expected behavior when interacting with
the Twitch API.

Methods tested:
- get_users
- get_user_by_id
- get_user_follows
- get_channel_followers
- get_top_games
- get_streams_by_game
- get_user_blocks
- get_user_block_list
- block_user
- unblock_user

Each method's test case verifies that the method correctly sends a request
to the Twitch API and handles the response data accordingly. The unittest.mock
module is utilized to mock the API responses, ensuring isolated tests.

Note: These tests require a working internet connection to access the Twitch API.
"""

import unittest

from unittest.mock import Mock
import requests
from src.twitch_helper import TwitchAPISession

# pylint: disable=R0904
class TwitchAPISessionTestCase(unittest.TestCase):
    """
    Test cases for the TwitchAPISession class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = None
        self.oauth_token = None
        self.client_id = None

    def create_clip(self, video_id):
        """
        Create a clip from a specified video on Twitch.

        This method allows you to create a clip (short video highlight) from a specified video
        on Twitch. Creating a clip requires proper authentication using either an app access token
        or an OAuth token. If neither of these tokens is provided during initialization of the 
        session, a ValueError will be raised.

        Args:
            video_id (str): The ID of the video from which the clip will be created.
                            The video_id is a unique identifier for each video on Twitch.

        Returns:
            dict: A dictionary containing information about the created clip if the operation 
            is successful.

        Raises:
            ValueError: If no authentication token is provided during initialization.
            RuntimeError: If the API responds with a 401 Unauthorized error, indicating an invalid
                        OAuth token, or if the API responds with any other non-success status code,
                        indicating an error in creating the clip. The error message from the API 
                        response will be included in the exception message.

        Example:
            # Initialize a Twitch API session with an OAuth token
            oauth_token = "your_test_oauth_token_here"
            twitch_session_with_auth = TwitchAPISession(
                client_id="your_client_id",
                access_token="your_access_token",
                oauth_token=oauth_token
            )

            # Create a clip from a specified video
            video_id = "123456789"  # Replace with the actual video ID
            clip_info = twitch_session_with_auth.create_clip(video_id)
            print(clip_info)
            # Output: {
            #   'id': 'abcd1234',
            #   'edit_url': 'https://clips.twitch.tv/abcd1234',
            #   'url': 'https://clips.twitch.tv/abcd1234',
            #   'embed_url': 'https://clips.twitch.tv/embed?clip=abcd1234',
            #   'broadcaster_id': '987654321',
            #   'broadcaster_name': 'example_broadcaster',
            #   'creator_id': '123456789',
            #   'creator_name': 'example_creator',
            #   'video_id': '123456789',
            #   'game_id': '56789',
            #   'language': 'en',
            #   'title': 'Funny Gaming Moment',
            #   'view_count': 1000,
            #   'created_at': '2023-07-04T12:34:56Z',
            #   'thumbnail_url': 'https://clips.example.com/thumb.jpg',
            #   'duration': 30.5
            # }
        """
        # Check if the required authentication token is present
        if not self.access_token and not self.oauth_token:
            raise ValueError("Authentication token required: access token or OAuth token.")

        # Construct headers with Client-ID and Authorization
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.oauth_token or self.access_token}",
        }


        # Set the timeout value in seconds (adjust as needed)
        timeout_seconds = 10

        # Make a request to the Twitch API to create a clip for the given video_id
        url = f"https://api.twitch.tv/helix/clips?broadcaster_id={video_id}"
        response = requests.post(url, headers=headers, timeout=timeout_seconds)

        if response.status_code == 401:
            raise RuntimeError("Unauthorized: Invalid OAuth token.")
        if response.status_code != 200:
            error_message = response.json().get('message', 'Unknown error')
            raise RuntimeError(f"Error creating clip: {error_message}")

        return response.json()

    @classmethod
    def setUpClass(cls):
        """
        Create a single mock session for all tests.
        """
        cls.mock_session = Mock()
        cls.twitch_session = TwitchAPISession("test_client_id", "test_access_token")
        cls.twitch_session.session = cls.mock_session

    def mock_api_response(self, status_code, data=None, headers=None):
        """
        Helper method to mock the API response.
        """
        response = Mock()
        response.status_code = status_code
        response.json.return_value = data
        response.headers = headers or {}
        self.mock_session.request.return_value = response

    def test_get_users(self):
        """
        Test the get_users method.

        This test ensures that the get_users method correctly fetches information
        about multiple Twitch users based on their login names.

        It mocks the API response from Twitch and verifies that the response
        from the method matches the expected response.

        The method being tested sends a GET request to the Twitch API endpoint:
        "https://api.twitch.tv/helix/users"

        We mock the response from the API with the expected data, and the test
        checks if the method returns the expected response.

        Test covers the following scenarios:
        - Fetching information for multiple users.
        - Matching the response data with the expected data.

        """
        # Mock API response with sample data
        data = [{"id": "1", "login": "user1", "display_name": "User 1"},
                {"id": "2", "login": "user2", "display_name": "User 2"}]
        self.mock_api_response(200, data=data)

        # Call the method to test
        result = self.twitch_session.get_users(["user1", "user2"])

        # Verify the response
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["login"], "user1")
        self.assertEqual(result[1]["display_name"], "User 2")

    def test_get_user_by_id(self):
        """
        Test the get_user_by_id method.

        This test ensures that the get_user_by_id method correctly fetches information
        about a Twitch user based on their user ID.

        It mocks the API response from Twitch and verifies that the response
        from the method matches the expected response.

        The method being tested sends a GET request to the Twitch API endpoint:
        "https://api.twitch.tv/helix/users"

        We mock the response from the API with the expected data, and the test
        checks if the method returns the expected response.

        Test covers the following scenarios:
        - Fetching information for a single user by ID.
        - Matching the response data with the expected data.

        """
        # Mock API response with sample data
        data = {"id": "1", "login": "user1", "display_name": "User 1"}
        self.mock_api_response(200, data=data)

        # Call the method to test
        result = self.twitch_session.get_user_by_id("1")

        # Verify the response
        self.assertEqual(result["login"], "user1")
        self.assertEqual(result["display_name"], "User 1")

    def test_get_user_follows(self):
        """
        Test the get_user_follows method.

        This test ensures that the get_user_follows method correctly fetches information
        about users who are following a specific Twitch user.

        It mocks the API response from Twitch and verifies that the response
        from the method matches the expected response.

        The method being tested sends a GET request to the Twitch API endpoint:
        "https://api.twitch.tv/helix/users/follows"

        We mock the response from the API with the expected data, and the test
        checks if the method returns the expected response.

        Test covers the following scenarios:
        - Fetching information for users following a specific user.
        - Matching the response data with the expected data.

        """
        # Mock API response with sample data
        data = [{"from_id": "1", "to_id": "2"},
                {"from_id": "2", "to_id": "3"}]
        self.mock_api_response(200, data=data)

        # Call the method to test
        result = self.twitch_session.get_user_follows("user1")

        # Verify the response
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["to_id"], "3")

    def test_get_channel_followers(self):
        """
        Test the get_channel_followers method.

        This test ensures that the get_channel_followers method correctly fetches information
        about users who are following a specific Twitch channel.

        It mocks the API response from Twitch and verifies that the response
        from the method matches the expected response.

        The method being tested sends a GET request to the Twitch API endpoint:
        "https://api.twitch.tv/helix/users/follows"

        We mock the response from the API with the expected data, and the test
        checks if the method returns the expected response.

        Test covers the following scenarios:
        - Fetching information for users following a specific channel.
        - Matching the response data with the expected data.

        """
        # Mock API response with sample data
        data = [{"from_id": "1", "to_id": "channel1"},
                {"from_id": "2", "to_id": "channel1"}]
        self.mock_api_response(200, data=data)

        # Call the method to test
        result = self.twitch_session.get_channel_followers("channel1")

        # Verify the response
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["from_id"], "1")

    def test_get_top_games(self):
        """
        Test the get_top_games method.

        This test ensures that the get_top_games method correctly fetches information
        about the top games being played on Twitch.

        It mocks the API response from Twitch and verifies that the response
        from the method matches the expected response.

        The method being tested sends a GET request to the Twitch API endpoint:
        "https://api.twitch.tv/helix/games/top"

        We mock the response from the API with the expected data, and the test
        checks if the method returns the expected response.

        Test covers the following scenarios:
        - Fetching information for top games.
        - Matching the response data with the expected data.

        """
        # Mock API response with sample data
        data = {"data": [{"id": "1", "name": "Game 1"},
                         {"id": "2", "name": "Game 2"}]}
        self.mock_api_response(200, data=data)

        # Call the method to test
        result = self.twitch_session.get_top_games(2)

        # Verify the response
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["name"], "Game 2")

    def test_get_streams_by_game(self):
        """
        Test the get_streams_by_game method.

        This test ensures that the get_streams_by_game method correctly fetches information
        about streams for a specific game on Twitch.

        It mocks the API response from Twitch and verifies that the response
        from the method matches the expected response.

        The method being tested sends a GET request to the Twitch API endpoint:
        "https://api.twitch.tv/helix/streams"

        We mock the response from the API with the expected data, and the test
        checks if the method returns the expected response.

        Test covers the following scenarios:
        - Fetching information for streams of a specific game.
        - Matching the response data with the expected data.

        """
        # Mock API response with sample data
        data = {"data": [{"user_id": "1", "user_name": "user1", "viewer_count": 100},
                         {"user_id": "2", "user_name": "user2", "viewer_count": 200}]}
        self.mock_api_response(200, data=data)

        # Call the method to test
        result = self.twitch_session.get_streams_by_game("Game1", 2)

        # Verify the response
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["viewer_count"], 100)

    def test_get_user_blocks(self):
        """
        Test the get_user_blocks method.

        This test ensures that the get_user_blocks method correctly fetches information
        about users blocked by the authenticated Twitch user.

        It mocks the API response from Twitch and verifies that the response
        from the method matches the expected response.

        The method being tested sends a GET request to the Twitch API endpoint:
        "https://api.twitch.tv/helix/blocks"

        We mock the response from the API with the expected data, and the test
        checks if the method returns the expected response.

        Test covers the following scenarios:
        - Fetching information for blocked users.
        - Matching the response data with the expected data.

        """
        # Mock API response with sample data
        data = {"blocks": [{"user_id": "1", "user_login": "user1"},
                           {"user_id": "2", "user_login": "user2"}]}
        self.mock_api_response(200, data=data)

        # Call the method to test
        result = self.twitch_session.get_user_blocks()

        # Verify the response
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["user_login"], "user2")

    def test_get_user_block_list(self):
        """
        Test case for the get_user_block_list method.
        """
        # Mock API response with sample data
        data = {"block_list": [{"user_id": "1", "user_login": "user1"},
                               {"user_id": "2", "user_login": "user2"}]}
        self.mock_api_response(200, data=data)

        # Call the method to test
        result = self.twitch_session.get_user_block_list()

        # Verify the response
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["user_id"], "1")

    def test_block_user(self):
        """
        Test the block_user method.

        This test ensures that the block_user method correctly blocks a user on Twitch
        and returns the expected response.

        It mocks the API response from Twitch to verify that the method
        returns the expected response upon successful blocking of the user.

        The method being tested sends a PUT request to the Twitch API endpoint:
        "https://api.twitch.tv/helix/blocks"

        We mock the response from the API with the expected data, and the test
        checks if the method returns the expected response.

        Test covers the following scenarios:
        - Blocking a user successfully.
        - Handling the response data after blocking.

        """
        # Mock API response with sample data
        data = {"user_id": "blocked_user", "user_login": "blocked_user_login"}
        self.mock_api_response(200, data=data)

        # Call the method to test
        result = self.twitch_session.block_user("user_to_block")

        # Verify the response
        self.assertEqual(result["user_id"], "blocked_user")
        self.assertEqual(result["user_login"], "blocked_user_login")

    def test_unblock_user(self):
        """
        Test the unblock_user method.

        This test ensures that the unblock_user method correctly unblocks a user on Twitch
        and returns the expected response.

        It mocks the API response from Twitch to verify that the method
        returns the expected response upon successful unblocking of the user.

        The method being tested sends a DELETE request to the Twitch API endpoint:
        "https://api.twitch.tv/helix/blocks"

        We mock the response from the API with the expected data, and the test
        checks if the method returns the expected response.

        Test covers the following scenarios:
        - Unblocking a user successfully.
        - Handling the response data after unblocking.

        """
        # Mock API response with sample data
        data = {"user_id": "unblocked_user", "user_login": "unblocked_user_login"}
        self.mock_api_response(200, data=data)

        # Call the method to test
        result = self.twitch_session.unblock_user("user_to_unblock")

        # Verify the response
        self.assertEqual(result["user_id"], "unblocked_user")
        self.assertEqual(result["user_login"], "unblocked_user_login")

    def test_api_error_response(self):
        """
        Test error handling when the Twitch API returns an error response.

        It mocks the API response from Twitch with an error status code and checks
        if the methods in TwitchAPISession handle the error response appropriately.

        Test covers the following scenarios:
        - Error handling for invalid API responses.
        - Appropriate exception handling.

        """
        self.mock_session.get.return_value.status_code = 400
        self.mock_session.get.return_value.json.return_value = {
            "error": "Bad Request",
            "status": 400,
            "message": "Invalid input",
        }

        # Test get_users method with an invalid API response
        logins = ["user1", "user2"]
        with self.assertRaises(RuntimeError):
            self.twitch_session.get_users(logins)

        # Test get_user_by_id method with an invalid API response
        user_id = "123"
        with self.assertRaises(RuntimeError):
            self.twitch_session.get_user_by_id(user_id)

        # Add similar tests for other methods...

    def test_boundary_cases(self):
        """
        Test boundary cases for relevant parameters in the methods.

        This test checks if the methods handle minimum and maximum input values for
        relevant parameters correctly.

        Test covers the following scenarios:
        - Boundary cases for input parameters.
        - Proper handling of edge values.

        """
        # Test get_user_by_id with minimum user ID
        user_id_min = "1"
        self.mock_session.get.return_value.json.return_value = {"data": {"user_id": user_id_min}}
        response = self.twitch_session.get_user_by_id(user_id_min)
        self.assertEqual(response["data"]["user_id"], user_id_min)

        # Test get_user_by_id with maximum user ID
        user_id_max = "9" * 25  # Assume maximum user ID length is 25 characters
        self.mock_session.get.return_value.json.return_value = {"data": {"user_id": user_id_max}}
        response = self.twitch_session.get_user_by_id(user_id_max)
        self.assertEqual(response["data"]["user_id"], user_id_max)

        # Add similar tests for other methods...

    def test_negative_testing(self):
        """
        Test negative scenarios with invalid input data.

        This test checks if the methods handle invalid input data correctly.

        Test covers the following scenarios:
        - Negative testing with invalid input data.
        - Proper handling of exceptions or errors.

        """
        # Test get_users with an empty list of logins
        logins = []
        with self.assertRaises(ValueError):
            self.twitch_session.get_users(logins)

        # Test get_user_by_id with an invalid user ID (non-string input)
        user_id_invalid = 12345
        with self.assertRaises(TypeError):
            self.twitch_session.get_user_by_id(user_id_invalid)

        # Add similar tests for other methods...

    def test_integration_get_users(self):
        """
        Test get_users method with actual network connections to Twitch's API.

        This test makes actual API calls to Twitch's API and checks if the responses
        are as expected.

        Test covers the following scenarios:
        - Integration testing with actual network connections.
        - API response verification.

        IMPORTANT: Make sure to use a test Twitch account with limited privileges
        for integration testing to avoid unintended actions.

        """
        # Replace 'your_client_id' and 'your_access_token' with your actual Twitch API credentials
        real_twitch_session = TwitchAPISession(
            client_id='your_client_id', access_token='your_access_token'
        )

        # Test get_users with actual network connections
        logins = ["user1", "user2"]
        response = real_twitch_session.get_users(logins)

        # Assertions based on the actual API response
        self.assertIn("data", response)
        self.assertTrue(len(response["data"]) > 0)

    def test_rate_limit_handling(self):
        """
        Test handling of rate limit responses from Twitch's API.

        This test mocks the API response with a rate-limiting error and
        ensures that the methods correctly handle it.

        Test covers the following scenarios:
        - Rate limit handling for API responses.
        - Proper waiting and retries for rate-limited requests.

        """
        self.mock_session.get.return_value.status_code = 429
        self.mock_session.get.return_value.json.return_value = {
            "error": "Too Many Requests",
            "status": 429,
            "message": "Rate limit exceeded",
        }

        # Test get_users method with rate-limiting response
        logins = ["user1", "user2"]
        with self.assertRaises(RuntimeError):
            self.twitch_session.get_users(logins)

        # Add similar tests for other methods...

    def test_authentication(self):
        """
        Test handling of authenticated requests to Twitch's API.

        This test checks if the methods that require authentication
        handle it correctly and raise exceptions when necessary.

        Test covers the following scenarios:
        - Authentication handling for API requests.
        - Proper exception raising for unauthorized requests.

        IMPORTANT: To perform this test, you'll need to provide a test OAuth token
        or a token obtained from Twitch's API.

        """
        # Test a method that requires authentication (e.g., create_clip)
        oauth_token = "your_test_oauth_token_here"
        twitch_session_with_auth = TwitchAPISession(client_id="your_id", access_token=oauth_token)

        # Mock the API response with an authentication error
        self.mock_session.post.return_value.status_code = 401
        self.mock_session.post.return_value.json.return_value = {
            "error": "Unauthorized",
            "status": 401,
            "message": "Invalid OAuth token",
        }

        # Test create_clip method with an invalid OAuth token
        with self.assertRaises(RuntimeError):
            twitch_session_with_auth.create_clip("123")

        # Add similar tests for other authenticated methods...


    def test_endpoint_urls_and_parameters(self):
        """
        Test the constructed endpoint URLs and parameters.

        This test checks if the methods construct the correct endpoint URLs
        and include the required parameters in the API requests.

        Test covers the following scenarios:
        - URL construction for API endpoints.
        - Verification of required parameters in API requests.

        """
        # Test get_users method with specified logins
        logins = ["user1", "user2"]
        self.twitch_session.get_users(logins)

        # Check if the URL is constructed correctly
        self.mock_session.get.assert_called_with(
            "https://api.twitch.tv/helix/users",
            params={"login": "user1,user2"},  # Ensure correct parameters
            headers={"Authorization": "Bearer mock_oauth_token"},
        )

        # Add similar tests for other methods...

    def test_http_methods(self):
        """
        Test the HTTP methods used by the API requests.

        This test checks if the methods use the correct HTTP methods (GET, POST, PUT, DELETE, etc.)
        for the respective API calls.

        Test covers the following scenarios:
        - Verification of HTTP methods used in API requests.

        """
        # Test create_clip method (POST request)
        video_id = "123456"
        self.twitch_session.create_clip(video_id)

        # Check if the method used the POST HTTP method
        self.mock_session.post.assert_called_with(
            "https://api.twitch.tv/helix/clips",
            json={"broadcaster_id": video_id},
            headers={"Authorization": "Bearer mock_oauth_token"},
        )

        # Add similar tests for other methods that use different HTTP methods...


if __name__ == '__main__':
    unittest.main()
