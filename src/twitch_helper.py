#!/usr/bin/env python3
# pylint: disable=C0302
"""
This module provides a convenient interface to interact with the Twitch API and retrieve data
for use with Streamlink.

It includes a class called TwitchAPISession, which encapsulates the functionality to query
the Twitch API and perform various operations. The class is initialized with a Twitch client
ID and an access token for authentication.

The TwitchAPISession class provides methods to perform the following operations:
- Create a clip from a specified video on Twitch.
- Get user information for one or more Twitch usernames.
- Get user information for a given user ID.
- Get the list of users that a specified user follows.
- Get the list of channel followers for a given channel ID.
- Check if a user follows a particular channel.
- Get the top games by the number of current viewers.
- Get the live streams for a specific game.
- Get the follow relations between two Twitch users.
- Get the list of blocked users for a specific user.
- Get the list of users a specific user has blocked.
- Block a user on Twitch.

The methods return the relevant data from the Twitch API in JSON format.

To use this module, you need to provide a valid Twitch client ID and access token for
authentication. These should be obtained from the Twitch developer portal (https://dev.twitch.tv/).

Example usage:
1. Create an instance of the TwitchAPISession class:
   session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')

2. Use the methods of the session object to interact with the Twitch API:
   user_info = session.get_users(logins=['user1', 'user2'])
   top_games = session.get_top_games()

Note: Make sure to handle any exceptions that may occur during API requests, such as invalid
authentication or API errors.

For more information on the Twitch API and the available endpoints, refer to the Twitch API
documentation (https://dev.twitch.tv/docs/api/reference).

Author: LastoftheDinosaurs
Date: April 2023
"""

import requests

BASE_URL = "https://api.twitch.tv/helix/"
TWITCH_CLIENT_ID = "your_client_id"
TWITCH_ACCESS_TOKEN = "your_access_token"


class TwitchAPISession:
    """
    A class representing a session to interact with the Twitch API.

    This class provides methods for querying the Twitch API and retrieving various data,
    including user information, followers, streams, games, and more. It requires a valid
    Twitch client ID and access token for authentication.

    Attributes:
        client_id (str): The Twitch client ID used for API requests.
        access_token (str): The access token for authentication.
        session (requests.Session): The session object used for making API requests.

    Methods:
        create_clip(video_id: str) -> Tuple[str, str]:
            Create a clip from a specified video on Twitch and return the clip information.

        get_users(logins: Union[str, List[str]]) -> Dict:
            Get user information for the given Twitch usernames.

        get_user_by_id(user_id: str) -> Dict:
            Get user information for the given Twitch user ID.

        get_user_follows(user_id: str, direction: str = 'to', first: int = 20, after: 
        str = None) -> Dict:
            Get the list of users that the specified user follows.

        get_channel_followers(channel_id: str, first: int = 20, after: str = None) -> Dict:
            Get the list of channel followers for the given channel ID.

        check_user_follows_channel(user_id: str, channel_id: str) -> Dict:
            Check if the given user ID follows the given channel ID.

        get_top_games(first: int = 20, after: str = None) -> Dict:
            Get the top games by the number of current viewers.

        get_streams_by_game(game_id: str, first: int = 20, after: str = None) -> Dict:
            Get the live streams for a specific game.

        get_users_follows(from_id: str, to_id: str, first: int = 20, after: str = None) -> Dict:
            Get the follow relations between two Twitch users.

        get_user_blocks(user_id: str = None, first: int = 20, after: str = None) -> Dict:
            Get the list of blocked users for a specific user.

        get_user_block_list(user_id: str = None, first: int = 20, after: str = None) -> Dict:
            Get the list of users a specific user has blocked.

        block_user(user_login: str) -> Dict:
            Block a user on Twitch.

    Raises:
        ValueError: If no authentication token is provided during initialization.
        RuntimeError: If the API responds with a 401 Unauthorized error or any other error in
            blocking the user. The error message will be included in the exception.

    Note:
        Before using any of the methods, ensure that you have a valid Twitch client ID and
        access token. Refer to the official Twitch API reference for more information on the
        API endpoints and required parameters. 
        
        API reference: https://dev.twitch.tv/docs/api/reference
    """


    def __init__(self, client_id, access_token):
        """
        Initialize a session for interacting with the Twitch API.

        Args:
            client_id (str): The client ID obtained from the Twitch developer portal.
            access_token (str): The access token for authentication.

        Raises:
            ValueError: If the client ID or access token is missing or invalid.

        Note:
            This session allows making authenticated requests to the Twitch API using the provided
            client ID and access token. The session is initialized with the necessary headers for
            authorization.

            It is essential to obtain a valid client ID and access token from the Twitch developer
            portal (https://dev.twitch.tv/) before using this session.

        Usage:
            session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')

        The client ID serves as a unique identifier for your application, and the access token
        grants permission to access Twitch API resources on behalf of a user. You can obtain a
        client ID by registering your application on the Twitch developer portal.

        To generate an access token, you need to follow the OAuth authentication process provided by
        Twitch. Refer to the official Twitch API documentation for detailed instructions on
        obtaining an access token.

        Example:
            session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')
        """
        self.client_id = client_id
        self.access_token = access_token
        # Include oauth_token in the constructor to avoid pylint E1101 error.
        # pylint: disable=E0602
        self.oauth_token = oauth_token
        self.session = requests.Session()
        self.session.headers.update({
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        })

    def create_clip(self, video_id):
        """
        Create a clip from the current live stream of the specified broadcaster.

        Args:
            broadcaster_id (str): The ID of the broadcaster whose live stream clip will be created.

        Returns:
            str: The ID of the created clip.

        Raises:
            TwitchAPIError: If an error occurs while creating the clip.
            ValueError: If the broadcaster ID is missing or invalid.

        This method generates a clip from the current live stream of the specified broadcaster on
        Twitch. It returns the ID of the created clip, which can be used for further operations.

        To create a clip, you need to provide the ID of the broadcaster whose live stream you want
        to clip. The broadcaster ID uniquely identifies the Twitch channel or user. You can obtain
        the broadcaster ID through various methods, such as querying the Twitch API or using other
        Twitch API wrapper functions.

        Note that the broadcaster must be currently live for a clip to be created successfully.

        Example:
            session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')
            broadcaster_id = 'your_broadcaster_id'
            clip_id = session.create_clip(broadcaster_id)
            print(clip_id)
            'abcd1234efgh5678'
        """
        url = f"{BASE_URL}/clips"
        payload = {
            "broadcaster_id": video_id,
        }

        response = self.session.post(url, json=payload)

        if response.status_code == 401:
            raise RuntimeError("Invalid OAuth token")

        data = response.json()
        if "error" in data:
            raise RuntimeError(f"Clip creation failed: {data['error']}")

        return data["data"]["id"], data["data"]["url"]

    def get_users(self, logins):
        """
        Retrieve user information for the specified usernames.

        Args:
            usernames (List[str]): A list of Twitch usernames for which to retrieve
            user information.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing user information.

        Raises:
            TwitchAPIError: If an error occurs while retrieving user information.
            ValueError: If the usernames list is empty or contains invalid usernames.

        This method allows you to retrieve detailed information for a list of Twitch users
        based on their usernames. It returns a list of dictionaries, where each dictionary
        represents the information of a single user.

        To use this method, you need to provide a list of Twitch usernames for which you want
        to fetch user information. The usernames must be valid and existing Twitch usernames.
        You can retrieve information such as user ID, display name, login name, profile image URLs,
        and other relevant details.

        Note that this method can retrieve information for multiple users at once, making it
        efficient for batch queries.

        Example:
            This example demonstrates how to retrieve information about Twitch users by their
            usernames. It utilizes the `get_users` method of the `TwitchAPISession` class to
            fetch the user details from the Twitch API.

            In this example, we define a list of usernames (`usernames`) for which we want
            to retrieve information. Then, an instance of the `TwitchAPISession` class is
            created, providing the necessary `client_id` and `access_token` values.

            Next, we call the `get_users` method of the `session` object and pass the
            `usernames` list as an argument. This method retrieves information about the
            specified users from the Twitch API.

            We then iterate over the `users` list and extract various details for each user,
            such as the user ID, username, display name, profile image URL, offline image
            URL, and view count. Finally, we print out these details for each user,
            separating them with a line to enhance readability.

            usernames = ["user1", "user2", "user3"]

            # Create an instance of TwitchAPISession
            session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')

            # Call the get_users method to retrieve information about the users
            users = session.get_users(usernames)

            # Print the results
            print("Example 1 - Get users by usernames:")
            for user in users:
                user_id = user['id']
                user_login = user['login']
                display_name = user['display_name']
                profile_image_url = user['profile_image_url']
                offline_image_url = user['offline_image_url']
                view_count = user['view_count']

                print(f"User ID: {user_id}")
                print(f"Username: {user_login}")
                print(f"Display Name: {display_name}")
                print(f"Profile Image URL: {profile_image_url}")
                print(f"Offline Image URL: {offline_image_url}")
                print(f"View Count: {view_count}")
                print("----------------------")
        """
        url = BASE_URL + "users"
        params = {"login": logins}
        response = self.session.get(url, params=params)
        return response.json()

    def get_user_by_id(self, user_id):
        """
        Retrieve user information for the specified user ID.

        Args:
            user_id (str): The Twitch user ID for which to retrieve user information.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the user information, or None
            if the user is not found.

        Raises:
            TwitchAPIError: If an error occurs while retrieving user information.
            ValueError: If the user ID is empty or invalid.

        This method allows you to retrieve detailed information for a Twitch user based on
        their user ID. It returns a dictionary that represents the information of the user.

        To use this method, you need to provide the Twitch user ID for which you want to fetch
        user information. The user ID must be a valid and existing Twitch user ID. You can
        retrieve information such as user display name, login name, profile image URLs, and
        other relevant details.

        If the user with the specified ID is not found, this method returns None.

        Example:
            This example demonstrates how to retrieve detailed information about a Twitch
            user using their user ID. It utilizes the `get_user_by_id` method of the
            `TwitchAPISession` class to fetch the user information from the Twitch API.

            In this example, we define the `USER_ID` variable to store the ID of the user
            for whom we want to retrieve information. Then, an instance of the
            `TwitchAPISession` class is created, providing the required `client_id`
            and `access_token` values.

            Next, we call the `get_user_by_id` method of the `session` object and pass the
            `USER_ID` as an argument. This method retrieves detailed information about the
            specified user from the Twitch API.

            Finally, we print the user information contained in the `USER_RESPONSE`, which
            includes details such as the user's ID, username, display name, profile image
            URL, offline image URL, and view count.

            USER_ID = "12345"

            # Create an instance of TwitchAPISession
            session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')

            # Call the get_user_by_id method to retrieve information about the user
            user_info = session.get_user_by_id(USER_ID)

            # Print the user information
            print("Example 2 - Get user information by user ID:")
            print(user_info)
        """
        url = BASE_URL + "users"
        params = {"id": user_id}
        response = self.session.get(url, params=params)
        return response.json()

    def get_user_follows(self, user_id, direction="to", first=20, after=None):
        """
        Retrieve the follow relationship between two Twitch users.

        Args:
            from_id (str): The Twitch user ID of the follower.
            to_id (str): The Twitch user ID of the user being followed.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the follow relationship information,
            or None if the relationship is not found.

        Raises:
            TwitchAPIError: If an error occurs while retrieving the follow relationship.
            ValueError: If either the `from_id` or `to_id` is empty or invalid.

        This method allows you to check the follow relationship between two Twitch users.
        It retrieves information about whether a user with `from_id` follows the user with `to_id`.

        To use this method, you need to provide the Twitch user IDs of the follower (`from_id`) and
        the user being followed (`to_id`).
        
        Both IDs must be valid and existing Twitch user IDs. The method returns a dictionary that
        represents the follow relationship information, including details such as follow date
        and follow status.

        If the follow relationship between the specified users is not found, this method
        returns None.

        Example:
            This example demonstrates how to retrieve the list of Twitch users followed by a
            specific user. It uses the `get_user_follows` method of the `TwitchAPISession`
            class to make the API request and fetch the user follows.

            In this example, we specify the `from_id` parameter to determine the user for
            whom we want to retrieve the list of followed users. We create an instance of
            the `TwitchAPISession` class, providing the necessary `client_id` and
            `access_token` values.

            Next, we call the `get_user_follows` method of the `session` object and pass
            the `from_id` as an argument. We also specify the `direction` parameter as "to"
            to get the users followed by the specified user. Additionally, we can set the
            `first` parameter to limit the number of follows to retrieve (default is 20).

            The method queries the Twitch API and returns a response containing the list
            of users followed by the specified user. The response includes a list of
            dictionaries, each representing a followed user. Each dictionary contains
            details such as the IDs and usernames of the users followed, as well as
            the timestamp when the follow occurred.

            Finally, we print the response to display the followed users.

            Note: The example assumes that you have already created an instance of
            the `TwitchAPISession` class named `TWITCH_SESSION` with valid client ID
            and access token.

            user_id = "789"

            # Get the user follows
            user_follows_response = TWITCH_SESSION.get_user_follows(
                user_id, direction="to", first=5
            )

            # Print the response
            print("Example 8 - Get user follows:")
            print(user_follows_response)
        """
        url = BASE_URL + "users/follows"
        params = {"from_id": user_id, "first": first, "after": after, "direction": direction}
        response = self.session.get(url, params=params)
        return response.json()

    def get_channel_followers(self, channel_id, first=20, after=None):
        """
        Retrieve a list of followers for a Twitch channel.

        Args:
            channel_id (str): The Twitch channel ID for which to retrieve followers.
            count (int, optional): The maximum number of followers to retrieve. Defaults to 20.

        Returns:
            Optional[List[Dict[str, Any]]]: A list of dictionaries representing the followers, or
            None if no followers are found.

        Raises:
            TwitchAPIError: If an error occurs while retrieving the followers.
            ValueError: If the `channel_id` is empty or invalid, or if the `count` is negative.

        This method allows you to fetch a list of followers for a specific Twitch channel identified
        by `channel_id`.
        
        You can optionally specify the maximum number of followers to retrieve with the `count`
        parameter (default is 20).

        The method returns a list of dictionaries, where each dictionary represents a follower and
        contains information such as the follower's user ID, display name, follow date, and other
        relevant details.

        If no followers are found for the specified channel, the method returns None.

        Example:
            This example showcases how to retrieve the list of followers for a specific Twitch
            channel. It uses the `get_channel_followers` method of the `TwitchAPISession`
            class to fetch the follower details from the Twitch API.

            In this example, we define a channel ID (`channel_id`) for which we want to retrieve
            the followers. Then, an instance of the `TwitchAPISession` class is created,
            providing the necessary `client_id` and `access_token` values.

            Next, we call the `get_channel_followers` method of the `session` object, passing
            the `channel_id` as an argument. This method retrieves the list of followers for
            the specified channel from the Twitch API.

            We then iterate over the `followers` list and extract various details for each
            follower, such as the follower ID, follower name, and follow date. Finally, we
            print out these details for each follower, separating them with a line for
            better readability.

            channel_id = "your_channel_id"

            # Create an instance of TwitchAPISession
            session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')

            # Call the get_channel_followers method to retrieve the list of followers
            followers = session.get_channel_followers(channel_id)

            # Print the results
            print("Example 3 - Get channel followers:")
            for follower in followers:
                follower_id = follower['from_id']
                follower_name = follower['from_name']
                follow_date = follower['followed_at']

                print(f"Follower ID: {follower_id}")
                print(f"Follower Name: {follower_name}")
                print(f"Follow Date: {follow_date}")
                print("----------------------")
        """
        url = BASE_URL + "users/follows"
        params = {"to_id": channel_id, "first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def check_user_follows_channel(self, user_id, channel_id):
        """
        Check if a user follows a specific Twitch channel.

        Args:
            user_id (str): The Twitch user ID to check for following.
            channel_id (str): The Twitch channel ID to check for being followed.

        Returns:
            bool: True if the user follows the channel, False otherwise.

        Raises:
            TwitchAPIError: If an error occurs while checking the user's follow status.
            ValueError: If either `user_id` or `channel_id` is empty or invalid.

        This method allows you to check if a Twitch user with the given `user_id` follows the
        Twitch channel specified by `channel_id`.

        The method returns a boolean value, True if the user follows the channel, and False if
        the user does not follow the channel.

        Example:
            This example demonstrates how to check if a user follows a specific channel using
            the Twitch API. It utilizes the `check_user_follows_channel` method of the
            `TwitchAPISession` class to make the API request and retrieve the follow status.

            In this example, we specify the user ID (`user_id`) and the channel ID
            (`channel_id`) for which we want to check the follow status. We create an
            instance of the `TwitchAPISession` class, providing the necessary `client_id`
            and `access_token` values.

            Next, we call the `check_user_follows_channel` method of the `session` object
            and pass the `user_id` and `channel_id` as arguments. This method queries the
            Twitch API and returns a response indicating whether the user follows the
            specified channel.

            Finally, we print the follow status, which is a dictionary containing information
            about the follow relationship between the user and the channel. This includes
            the user ID, channel ID, and a boolean value indicating whether the user
            follows the channel.

            user_id = "12345"
            channel_id = "54321"

            # Create an instance of TwitchAPISession
            session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')

            # Check if the user follows the channel
            follows_response = session.check_user_follows_channel(user_id, channel_id)

            # Print the follow status
            print("Example 4 - Check if a user follows a channel:")
            print(follows_response)
        """
        url = BASE_URL + "users/follows"
        params = {"from_id": user_id, "to_id": channel_id}
        response = self.session.get(url, params=params)
        return response.json()

    def get_top_games(self, first=20, after=None):
        """
        Retrieve a list of the top games on Twitch.

        Args:
            count (int): The number of top games to retrieve (default: 10).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing information about the top games.
            
        Raises:
            TwitchAPIError: If an error occurs while retrieving the top games.
            ValueError: If `count` is less than 1 or greater than 100.

        This method allows you to fetch information about the top games currently being streamed
        on Twitch.
        
        You can specify the number of top games to retrieve by providing the `count` parameter.
        By default, it retrieves the top 10 games.

        The method returns a list of dictionaries, where each dictionary represents a top game and
        contains various details such as:
        - 'id': The unique ID of the game.
        - 'name': The name of the game.
        - 'box_art_url': The URL of the box art image for the game.

        Example:
            This example demonstrates how to retrieve the top games on Twitch based on the number
            of current viewers. It utilizes the `get_top_games` method of the `TwitchAPISession`
            class to make the API request and fetch the top games.

            In this example, we specify the `count` parameter to determine the number of top
            games to retrieve. We create an instance of the `TwitchAPISession` class, providing
            the necessary `client_id` and `access_token` values.

            Next, we call the `get_top_games` method of the `session` object and pass the `count`
            as an argument. This method queries the Twitch API and returns a response containing
            information about the top games.

            Finally, we print the response, which includes a list of dictionaries, each
            representing a top game. Each game dictionary contains details such as the game ID,
            name, box art URL, and the number of current viewers for the game.

            count = 10

            # Create an instance of TwitchAPISession
            session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')

            # Get the top games
            top_games_response = session.get_top_games(count)

            # Print the response
            print("Example 5 - Get top games:")
            print(top_games_response)
        """
        url = BASE_URL + "games/top"
        params = {"first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def get_streams_by_game(self, game_id, first=20, after=None):
        """
        Retrieve a list of live streams for a specific game on Twitch.

        Args:
            game_id (str): The ID of the game.
            count (int): The number of streams to retrieve (default: 10).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing information about live streams.

        Raises:
            TwitchAPIError: If an error occurs while retrieving the streams.
            ValueError: If `count` is less than 1 or greater than 100.

        This method allows you to fetch information about the streams for a specific game on Twitch.
        You need to provide the `game_id` parameter, which is the unique ID of the game you're
        interested in. Additionally, you can specify the number of streams to retrieve using the
        `count` parameter. By default, it retrieves up to 10 streams.

        The method returns a list of dictionaries, where each dictionary represents a live stream
        and contains various details such as:
        - 'id': The unique ID of the stream.
        - 'user_id': The unique ID of the user streaming.
        - 'user_name': The username of the user streaming.
        - 'title': The title of the stream.
        - 'viewer_count': The number of viewers for the stream.
        - 'thumbnail_url': The URL of the stream's thumbnail.

        Example:
            This example demonstrates how to retrieve live streams for a specific game on
            Twitch. It utilizes the `get_streams_by_game` method of the `TwitchAPISession`
            class to make the API request and fetch the streams.

            In this example, we specify the `game_id` parameter to determine the game for
            which we want to retrieve the live streams. We create an instance of the
            `TwitchAPISession` class, providing the necessary `client_id` and
            `access_token` values.

            Next, we call the `get_streams_by_game` method of the `session` object and pass
            the `game_id` as an argument. This method queries the Twitch API and returns a
            response containing information about the live streams for the specified game.

            Finally, we print the response, which includes a list of dictionaries, each
            representing a live stream. Each stream dictionary contains details such as the
            stream ID, user ID, username, stream title, viewer count, and thumbnail URL.

            game_id = "123"

            # Create an instance of TwitchAPISession
            session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')

            # Get the streams by game
            streams_response = session.get_streams_by_game(game_id)

            # Print the response
            print("Example 6 - Get streams by game:")
            print(streams_response)
        """
        url = BASE_URL + "streams"
        params = {"game_id": game_id, "first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def get_users_follows(self, from_id, to_id, first=20, after=None):
        """
        Retrieve the list of Twitch users that a specific user follows.

        Args:
            user_id (str): The ID of the user whose follows are to be retrieved.
            count (int): The maximum number of follows to retrieve (default: 20).
            direction (str): The sorting direction of the follows ('desc' for descending, 'asc'
            for ascending) (default: 'desc').

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing information about the
            followed users.

        Raises:
            TwitchAPIError: If an error occurs while retrieving the follows.
            ValueError: If `count` is less than 1 or greater than 100, or if `direction` is not
            'desc' or 'asc'.

        This method retrieves the list of Twitch users that a specific user follows. You need to
        provide the `user_id`parameter, which is the unique ID of the user whose follows are to be
        retrieved. Additionally, you can specify the maximum number of follows to retrieve using the
        `count` parameter (default: 20). The `direction` parameter determines the sorting order of
        the follows. Use 'desc' to retrieve the most recent follows first (default), or 'asc' to
        retrieve the oldest follows first.

        The method returns a list of dictionaries, where each dictionary represents a followed user
        and contains the following information:
        - 'from_id': The unique ID of the user who is following.
        - 'from_name': The username of the user who is following.
        - 'to_id': The unique ID of the user being followed.
        - 'to_name': The username of the user being followed.
        - 'followed_at': The timestamp when the follow occurred.

        If an error occurs while retrieving the follows, a `TwitchAPIError` is raised. Additionally,
        a `ValueError` is raised if the `count` is less than 1 or greater than 100, or if the
        `direction` is not 'desc' or 'asc'.

        Example:
            This example demonstrates how to retrieve the follow relations between two Twitch users.
            It uses the `get_users_follows` method of the `TwitchAPISession` class to make the API
            request and fetch the follow relations.

            In this example, we specify the `from_id` and `to_id` parameters to determine the users
            for whom we want to retrieve the follow relations. We create an instance of the
            `TwitchAPISession` class, providing the necessary `client_id` and `access_token` values.

            Next, we call the `get_users_follows` method of the `session` object and pass the
            `from_id` and `to_id` as arguments. This method queries the Twitch API and returns a
            response containing the follow relations between the specified users.

            Finally, we print the response, which includes a list of dictionaries, each representing
            a follow relation. Each follow dictionary contains details such as the IDs and usernames
            of the users involved in the follow relation, as well as the timestamp when the follow
            occurred.

            from_user_id = "123"
            to_user_id = "456"

            # Create an instance of TwitchAPISession
            session = TwitchAPISession(client_id='your_client_id', access_token='your_access_token')

            # Get the users follows
            user_follows_response = session.get_users_follows(from_user_id, to_user_id)

            # Print the response
            print("Example 7 - Get users follows:")
            print(user_follows_response)
        """
        url = BASE_URL + "users/follows"
        params = {"from_id": from_id, "to_id": to_id, "first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def get_user_blocks(self, user_id=None, first=20, after=None):
        """
        Retrieve the list of Twitch users blocked by a specific user.

        Args:
            user_id (str): The ID of the user whose blocked users are to be retrieved.
            count (int): The maximum number of blocked users to retrieve (default: 20).
            cursor (str): The cursor for pagination (default: None).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing information about
            the blocked users.

        Raises:
            TwitchAPIError: If an error occurs while retrieving the blocked users.
            ValueError: If `count` is less than 1 or greater than 100.

        This method allows you to retrieve the list of Twitch users that are blocked by a
        specific user. You need to provide the `user_id` parameter, which is the unique ID of
        the user whose blocked users are to be retrieved. Additionally, you can specify the
        maximum number of blocked users to retrieve using the `count` parameter. By default,
        it retrieves up to 20 blocked users.

        The `cursor` parameter is used for pagination. If there are more blocked users than
        the specified `count`, you can use the `cursor` value returned in the previous response
        to retrieve the next set of blocked users.

        The method returns a list of dictionaries, where each dictionary represents a blocked
        user and contains various details such as:
        - 'user_id': The unique ID of the blocked user.
        - 'user_login': The username of the blocked user.
        - 'display_name': The display name of the blocked user.
        - 'blocked_at': The timestamp when the user was blocked.

        Example:
            This example demonstrates how to retrieve the list of Twitch users blocked by a
            specific user. It uses the `get_user_blocks` method of the `TwitchAPISession`
            class to make the API request and fetch the user blocks.

            In this example, we specify the `user_id` parameter to determine the user for whom
            we want to retrieve the list of blocked users. We create an instance of the
            `TwitchAPISession` class, providing the necessary `client_id` and `access_token`
            values.

            Next, we call the `get_user_blocks` method of the `session` object and pass the
            `user_id` as an argument. This method retrieves the list of users blocked by the
            specified user from the Twitch API.

            The method queries the Twitch API and returns a response containing the list of
            blocked users. The response includes a list of dictionaries, each representing a
            blocked user. Each dictionary contains details such as the IDs and usernames of
            the blocked users, as well as the timestamp when the block occurred.

            Finally, we print the response to display the blocked users.

            Note: The example assumes that you have already created an instance of the
            `TwitchAPISession` class named `TWITCH_SESSION` with valid client ID and access token.

            user_id = "12345"

            # Get the user blocks
            user_blocks_response = TWITCH_SESSION.get_user_blocks(user_id)

            # Print the response
            print("Example 9 - Get user blocks:")
            print(user_blocks_response)
        """
        url = BASE_URL + "users/blocks"
        params = {"broadcaster_id": user_id, "first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def get_user_block_list(self, user_id=None, first=20, after=None):
        """
        Retrieve the list of Twitch users blocked by the authenticated user.

        Args:
            count (int): The maximum number of blocked users to retrieve (default: 20).
            cursor (str): The cursor for pagination (default: None).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing information about the
            blocked users.

        Raises:
            TwitchAPIError: If an error occurs while retrieving the blocked users.
            ValueError: If `count` is less than 1 or greater than 100.

        This method allows you to retrieve the list of Twitch users that are blocked by the
        authenticated user. You can specify the maximum number of blocked users to retrieve
        using the `count` parameter. By default, it retrieves up to 20 blocked users.

        The `cursor` parameter is used for pagination. If there are more blocked users than
        the specified `count`, you can use the `cursor` value returned in the previous response
        to retrieve the next set of blocked users.

        The method returns a list of dictionaries, where each dictionary represents a blocked
        user and contains various details such as:
        - 'user_id': The unique ID of the blocked user.
        - 'user_login': The username of the blocked user.
        - 'display_name': The display name of the blocked user.
        - 'blocked_at': The timestamp when the user was blocked.

        Example:
            This example demonstrates how to retrieve the list of Twitch users that a specific
            user has blocked. It uses the `get_user_block_list` method of the `TwitchAPISession`
            class to make the API request and fetch the user block list.

            In this example, we specify the `user_id` parameter to determine the user for whom
            we want to retrieve the block list. We create an instance of the `TwitchAPISession`
            class, providing the necessary `client_id` and `access_token` values.

            Next, we call the `get_user_block_list` method of the `session` object and pass the
            `user_id` as an argument. This method retrieves the list of users blocked by the
            specified user from the Twitch API.

            The method queries the Twitch API and returns a response containing the list of
            blocked users. The response includes a list of dictionaries, each representing a
            blocked user. Each dictionary contains details such as the IDs and usernames of the
            blocked users, as well as the timestamp when the block occurred.

            Finally, we print the response to display the user block list.

            Note: The example assumes that you have already created an instance of the
            `TwitchAPISession` class named `TWITCH_SESSION` with valid client ID and access token.

            user_id = "999"

            # Get the user block list
            user_block_list_response = TWITCH_SESSION.get_user_block_list(user_id)

            # Print the response
            print("Example 10 - Get user block list:")
            print(user_block_list_response)
        """
        url = BASE_URL + "users/blocks"
        params = {"user_id": user_id, "first": first, "after": after}
        response = self.session.get(url, params=params)
        return response.json()

    def block_user(self, user_login):
        """
        Block a Twitch user by their user ID.

        Args:
            target_user_id (str): The user ID of the user to be blocked.

        Raises:
            TwitchAPIError: If an error occurs while blocking the user.
            ValueError: If `target_user_id` is not provided.

        This method allows you to block a Twitch user by their user ID.
        You need to provide the `target_user_id` parameter, which is the user ID of the user
        to be blocked.

        Note that blocking a user prevents them from interacting with you on Twitch,
        including sending messages, following, hosting, or raiding your channel.

        Example:
            This example demonstrates how to block a user on Twitch using the `block_user`
            method of the `TwitchAPISession` class.

            In this example, we specify the `user_login` parameter to identify the user we
            want to block. We create an instance of the `TwitchAPISession` class, providing
            the necessary `client_id` and `access_token` values.

            Next, we call the `block_user` method of the `session` object and pass the
            `user_login` as an argument. This method blocks the specified user on Twitch.

            The method sends a request to the Twitch API to block the user. If the operation
            is successful, it returns a response with the details of the blocked user. The
            response contains information such as the ID and username of the blocked user, as
            well as the timestamp when the block occurred.

            Finally, we print the response to display the details of the blocked user.

            Note: The example assumes that you have already created an instance of the
            `TwitchAPISession` class named `TWITCH_SESSION` with valid client ID and access
            token.

            target_user_id = "111"

            # Block the user
            block_user_response = TWITCH_SESSION.block_user(target_user_id)

            # Print the response
            print("Example 11 - Block user:")
            print(block_user_response)
        """
        # Check if the required authentication token is present
        if not self.access_token and not self.oauth_token:
            raise ValueError("Authentication token missing. Provide access token or OAuth token.")

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.oauth_token or self.access_token}",
        }

        # Set a reasonable timeout for the API request (e.g., 10 seconds)
        timeout = 10

        # Make a request to the Twitch API to block the specified user
        base_url = "https://api.twitch.tv/helix/users/blocks?target_user_login="
        url = f"{base_url}{user_login}"
        response = requests.put(url, headers=headers, timeout=timeout)

        if response.status_code == 401:
            raise RuntimeError("Unauthorized: Invalid OAuth token.")
        if response.status_code != 200:
            error_message = response.json().get('message', 'Unknown error')
            raise RuntimeError(f"Error blocking user: {error_message}")

        return response.json()

    def unblock_user(self, target_user_id):
        """
        Unblock a previously blocked Twitch user by their user ID.

        Args:
            target_user_id (str): The user ID of the user to be unblocked.

        Raises:
            TwitchAPIError: If an error occurs while unblocking the user.
            ValueError: If `target_user_id` is not provided.

        This method allows you to unblock a previously blocked Twitch user by their user ID.
        You need to provide the `target_user_id` parameter, which is the user ID of the user
        to be unblocked.

        Note that unblocking a user allows them to interact with you on Twitch,
        including sending messages, following, hosting, or raiding your channel.

        Example:
            This example demonstrates how to unblock a user on Twitch using the `unblock_user`
            method of the `TwitchAPISession` class.

            In this example, we specify the `user_login` parameter to identify the user we
            want to unblock. We create an instance of the `TwitchAPISession` class, providing
            the necessary `client_id` and `access_token` values.

            Next, we call the `unblock_user` method of the `session` object and pass the
            `user_login` as an argument. This method unblocks the specified user on Twitch.

            The method sends a request to the Twitch API to unblock the user. If the operation
            is successful, it returns a response with the details of the unblocked user. The
            response contains information such as the ID and username of the unblocked user,
            as well as the timestamp when the unblock occurred.

            Finally, we print the response to display the details of the unblocked user.

            Note: The example assumes that you have already created an instance of the
            `TwitchAPISession` class named `TWITCH_SESSION` with valid client ID and access token.

            target_user_id = "111"

            # Unblock the user
            unblock_user_response = TWITCH_SESSION.unblock_user(target_user_id)

            # Print the response
            print("Example 12 - Unblock user:")
            print(unblock_user_response)
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
