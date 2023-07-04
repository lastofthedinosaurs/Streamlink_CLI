#!/usr/bin/env python3
"""
Used to query the Twitch API for data to feed to Streamlink
"""

import requests

BASE_URL = "https://api.twitch.tv/helix/"
TWITCH_CLIENT_ID = "your_client_id"
TWITCH_ACCESS_TOKEN = "your_access_token"


class TwitchAPISession:
    """
    A class to interact with the Twitch API using a session.

    Attributes:
        client_id (str): The Twitch client ID.
        access_token (str): The access token for authentication.
        session (requests.Session): The session object for API requests.
    """

    def __init__(self, client_id, access_token):
        """
        Initialize the TwitchAPISession.

        Args:
            client_id (str): The Twitch client ID.
            access_token (str): The access token for authentication.
        """
        self.client_id = client_id
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        })

    def get_users(self, logins):
        """
        Get user information for the given logins.

        Args:
            logins (str or list): The Twitch usernames.

        Returns:
            dict: The JSON response containing user information.
        """
        url = BASE_URL + "users"
        params = {"login": logins}
        response = self.session.get(url, params=params)
        return response.json()

    def get_user_by_id(self, user_id):
        """
        Get user information for the given user ID.

        Args:
            user_id (str): The Twitch user ID.

        Returns:
            dict: The JSON response containing user information.
        """
        url = BASE_URL + "users"
        params = {"id": user_id}
        response = self.session.get(url, params=params)
        return response.json()

    def get_user_follows(self, user_id, direction="to", first=20, after=None):
        """
        Get the list of users that the specified user follows.

        Args:
            user_id (str): The Twitch user ID of the user.
            direction (str, optional): The direction of the follow relationship. Valid values are "to" (users
                                       followed by the specified user) and "from" (users following the specified
                                       user). Default is "to".
            first (int, optional): The maximum number of results to return. Default is 20.
            after (str, optional): The cursor for pagination. Default is None.

        Returns:
            dict: The JSON response containing the list of followed users.
        """
        url = BASE_URL + "users/follows"
        params = {"from_id": user_id, "first": first, "after": after, "direction": direction}
        response = self.session.get(url, params=params)
        return response.json()

    def get_channel_followers(self, channel_id, first=20, after=None):
        """
        Get the list of channel followers for the given channel ID.

        Args:
            channel_id (str): The Twitch channel ID.
            first (int, optional): The maximum number of results to return. Default is 20.
            after (str, optional): The cursor for pagination. Default is None.

        Returns:
            dict: The JSON response containing the list of followers.
        """
        url = BASE_URL + "users/follows"
        params = {"to_id": channel_id, "first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def check_user_follows_channel(self, user_id, channel_id):
        """
        Check if the given user ID follows the given channel ID.

        Args:
            user_id (str): The Twitch user ID.
            channel_id (str): The Twitch channel ID.

        Returns:
            dict: The JSON response indicating if the user follows the channel.
        """
        url = BASE_URL + "users/follows"
        params = {"from_id": user_id, "to_id": channel_id}
        response = self.session.get(url, params=params)
        return response.json()

    def get_top_games(self, first=20, after=None):
        """
        Get the top games by number of current viewers.

        Args:
            first (int, optional): The maximum number of results to return. Default is 20.
            after (str, optional): The cursor for pagination. Default is None.

        Returns:
            dict: The JSON response containing the list of top games.
        """
        url = BASE_URL + "games/top"
        params = {"first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def get_streams_by_game(self, game_id, first=20, after=None):
        """
        Get the live streams for a specific game.

        Args:
            game_id (str): The Twitch game ID.
            first (int, optional): The maximum number of results to return. Default is 20.
            after (str, optional): The cursor for pagination. Default is None.

        Returns:
            dict: The JSON response containing the list of live streams for the game.
        """
        url = BASE_URL + "streams"
        params = {"game_id": game_id, "first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def get_users_follows(self, from_id, to_id, first=20, after=None):
        """
        Get the follow relations between two Twitch users.

        Args:
            from_id (str): The Twitch user ID of the follower.
            to_id (str): The Twitch user ID of the followee.
            first (int, optional): The maximum number of results to return. Default is 20.
            after (str, optional): The cursor for pagination. Default is None.

        Returns:
            dict: The JSON response containing the list of follow relations.
        """
        url = BASE_URL + "users/follows"
        params = {"from_id": from_id, "to_id": to_id, "first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def get_user_blocks(self, user_id=None, first=20, after=None):
        """
        Get the list of blocked users for a specific user.

        Args:
            user_id (str): The Twitch user ID.
            first (int, optional): The maximum number of results to return. Default is 20.
            after (str, optional): The cursor for pagination. Default is None.

        Returns:
            dict: The JSON response containing the list of blocked users.
        """
        url = BASE_URL + "users/blocks"
        params = {"broadcaster_id": user_id, "first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def get_user_block_list(self, user_id=None, first=20, after=None):
        """
        Get the list of users a specific user has blocked.

        Args:
            user_id (str): The Twitch user ID.
            first (int, optional): The maximum number of results to return. Default is 20.
            after (str, optional): The cursor for pagination. Default is None.

        Returns:
            dict: The JSON response containing the list of blocked users.
        """
        url = BASE_URL + "users/blocks"
        params = {"user_id": user_id, "first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def block_user(self, target_user_id):
        """
        Block a specific user.

        Args:
            target_user_id (str): The Twitch user ID of the user to block.

        Returns:
            dict: The JSON response indicating the success of the block action.
        """
        url = BASE_URL + "users/blocks"
        data = {"target_user_id": target_user_id}
        response = self.session.post(url, json=data)
        return response.json()

    def unblock_user(self, target_user_id):
        """
        Unblock a specific user.

        Args:
            target_user_id (str): The Twitch user ID of the user to unblock.

        Returns:
            dict: The JSON response indicating the success of the unblock action.
        """
        url = BASE_URL + "users/blocks"
        data = {"target_user_id": target_user_id}
        response = self.session.delete(url, json=data)
        return response.json()


if __name__ == "__main__":
    # Initialize the API session
    TWITCH_SESSION = TwitchAPISession(TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN)

    # Example 1 - Get users by usernames:
    USERNAMES = ["user1", "user2", "user3"]
    USERS_RESPONSE = TWITCH_SESSION.get_users(USERNAMES)
    print("Example 1 - Get users by usernames:")
    print(USERS_RESPONSE)

    # Example 2: Get user information by user ID
    USER_ID = "12345"
    USER_RESPONSE = TWITCH_SESSION.get_user_by_id(USER_ID)
    print("Example 2 - Get user by ID:")
    print(USER_RESPONSE)

    # Example 3: Get channel followers
    CHANNEL_ID = "54321"
    FOLLOWERS_RESPONSE = TWITCH_SESSION.get_channel_followers(CHANNEL_ID)
    print("Example 3 - Get channel followers:")
    print(FOLLOWERS_RESPONSE)

    # Example 4: Check if a user follows a channel
    USER_ID = "12345"
    CHANNEL_ID = "54321"
    FOLLOWS_RESPONSE = TWITCH_SESSION.check_user_follows_channel(USER_ID, CHANNEL_ID)
    print("Example 4 - Check if a user follows a channel:")
    print(FOLLOWS_RESPONSE)

    # Example 5: Get top games
    COUNT = 10
    TOP_GAMES_RESPONSE = TWITCH_SESSION.get_top_games(COUNT)
    print("Example 5 - Get top games:")
    print(TOP_GAMES_RESPONSE)

    # Example 6: Get streams by game
    GAME_ID = "123"
    STREAMS_RESPONSE = TWITCH_SESSION.get_streams_by_game(GAME_ID)
    print("Example 6 - Get streams by game:")
    print(STREAMS_RESPONSE)

    # Example 7 - Get users follows:
    FROM_USER_ID = "123"
    TO_USER_ID = "456"
    USER_FOLLOWS_RESPONSE = TWITCH_SESSION.get_users_follows(FROM_USER_ID, TO_USER_ID)
    print("Example 7 - Get users follows:")
    print(USER_FOLLOWS_RESPONSE)

    # Example 8 - Get user follows:
    USER_ID = "789"
    # Add direction parameter with value "to" to get users followed by the specified user
    USER_FOLLOWS_RESPONSE = TWITCH_SESSION.get_user_follows(USER_ID, direction="to", first=5)
    print("Example 8 - Get user follows:")
    print(USER_FOLLOWS_RESPONSE)

    # Example 9: Get user blocks
    USER_ID = "12345"  # Specify the user whose blocked users you want to retrieve
    USER_BLOCKS_RESPONSE = TWITCH_SESSION.get_user_blocks(USER_ID)
    print("Example 9 - Get user blocks:")
    print(USER_BLOCKS_RESPONSE)

    # Example 10: Get user block list
    TARGET_USER_ID = "999"
    USER_BLOCK_LIST_RESPONSE = TWITCH_SESSION.get_user_block_list(TARGET_USER_ID)
    print("Example 10 - Get user block list:")
    print(USER_BLOCK_LIST_RESPONSE)

    # Example 11: Block user
    TARGET_USER_ID = "111"
    BLOCK_USER_RESPONSE = TWITCH_SESSION.block_user(TARGET_USER_ID)
    print("Example 11 - Block user:")
    print(BLOCK_USER_RESPONSE)

    # Example 12: Unblock user
    TARGET_USER_ID = "111"
    UNBLOCK_USER_RESPONSE = TWITCH_SESSION.unblock_user(TARGET_USER_ID)
    print("Example 12 - Unblock user:")
    print(UNBLOCK_USER_RESPONSE)
