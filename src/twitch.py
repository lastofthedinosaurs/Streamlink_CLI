#!/usr/bin/env python3
"""
Used to query the Twitch API for data to feed to Streamlink
"""

import os

import requests
from dotenv import load_dotenv


class APIhelper:
    """
    Used to build API queries.

    You can pass each method a query or use the methods' built-in
    settings to construct new queries. Some methods return results when
    no query is provided. See docs/ or the official Twitch API
    documentation for more details.
    """
    id = ""
    name = ""
    login = ""
    user_id = ""
    user_login = ""
    game_id = ""
    broadcaster_id = ""
    type = "live"
    lang = "en"
    first = 10
    started_at = ""
    ended_at = ""
    igdb_id = ""
    period = ""

    def get_channel_stream_schedule(self, keys, query=""):
        """
        Gets the broadcaster's streaming schedule.

        You can get the entire schedule or specific segments of
        the schedule.
        """
        url = "https://api.twitch.tv/helix/schedule"
        if not query:
            if self.broadcaster_id:
                query = f"broadcaster_id={self.broadcaster_id}"
            elif self.id:
                query = f"id={self.id}"
        return api_request(keys, url, f"{query}")

    def get_clips(self, keys, query=""):
        """
        Gets one or more video clips that were captured from streams.
        """
        url = "https://api.twitch.tv/helix/clips"
        if not query:
            if self.broadcaster_id:
                query = f"broadcaster_id={self.broadcaster_id}"
            elif self.game_id:
                query = f"game_id={self.game_id}"
            elif self.id:
                query = f"id={self.id}"
        return api_request(keys, url, f"{query}")

    def get_followed_channels(self, keys, query=""):
        """
        Gets a list of broadcasters that the specified user follows.

        You can also use this endpoint to see whether a user
        follows a specific broadcaster.
        """
        url = "https://api.twitch.tv/helix/followed"
        if not query:
            if self.user_id:
                query = f"user_id={self.user_id}"
            elif self.broadcaster_id:
                query = f"broadcaster_id={self.broadcaster_id}"
        return api_request(keys, url, f"{query}")

    def get_games(self, keys, query=""):
        """
        Gets information about specified categories or games.

        You may get up to 100 categories or games by specifying their
        ID or name. You may specify all IDs, all names, or a
        combination of IDs and names. If you specify a combination of
        IDs and names, the total number of IDs and names must not
        exceed 100.
        """
        url = "https://api.twitch.tv/helix/games"
        if not query:
            if self.id:
                query = f"id={self.id}"
            elif self.name:
                query = f"name={self.name}"
            elif self.igdb_id:
                query = f"igdb_id={self.igdb_id}"
        return api_request(keys, url, f"{query}")

    def get_streams(self, keys, query=""):
        """
        Gets a list of all streams.

        The list is in descending order by the number of viewers
        watching the stream. Because viewers come and go during a
        stream, finding duplicate or missing streams in the list as
        you page through the results is possible.
        """
        url = "https://api.twitch.tv/helix/streams"
        if not query:
            if self.user_id:
                query = f"user_id={self.user_id}"
            elif self.user_login:
                query = f"user_login={self.user_login}"
            elif self.game_id:
                query = f"game_id={self.game_id}"
        # Append options to query
        query = f"{query}&type={self.type}"
        query = f"{query}&language={self.lang}"
        query = f"{query}&first={self.first}"
        return api_request(keys, url, f"{query}")

    def get_top_games(self, keys, query=""):
        """
        Gets information about all broadcasts on Twitch.
        """
        url = "https://api.twitch.tv/helix/games/top"
        if not query:
            if self.first:
                query = f"first={self.first}"
        return api_request(keys, url, f"{query}")

    def get_users(self, keys, query=""):
        """
        Gets information about one or more users.

        If you don't specify IDs or login names, the request returns
        information about the user in the access token if you specify
        a user access token.
        """
        url = "https://api.twitch.tv/helix/users"
        if not query:
            if self.id:
                query = f"id={self.id}"
            elif self.login:
                query = f"login={self.login}"
        return api_request(keys, url, query)

    def get_videos(self, keys, query=""):
        """
        Gets information about one or more published videos.

        You may get videos by ID, by user, or by game/category.

        You may apply several filters to get a subset of the videos.
        The filters are applied as an AND operation to each video.

        For example, if language is set to 'de' and game_id is set to
        21779, the response includes only videos that show playing
        League of Legends by users that stream in German. The filters
        apply only if you get videos by user ID or game ID.
        """
        url = "https://api.twitch.tv/helix/videos"
        if not query:
            if self.id:
                query = f"id={self.id}"
            elif self.user_id:
                query = f"user_id={self.user_id}"
            elif self.game_id:
                query = f"game_id={self.game_id}"
        # Append options to query
        query = f"{query}&type={self.type}"
        query = f"{query}&language={self.lang}"
        query = f"{query}&first={self.first}"
        if self.period:
            query = f"{query}&period={self.period}"
        return api_request(keys, url, f"{query}")


def get_access_token(client_id, client_secret):
    """
    Twitch APIs require OAuth 2.0 access tokens to access resources.
    """
    url = "https://id.twitch.tv/oauth2/token"
    with requests.Session() as session:
        body = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        response = session.post(url, body)
        response.raise_for_status()
        return response.json()


def api_request(keys, url, query=""):
    """
    Send a GET request to the Twitch API
    """
    with requests.Session() as session:
        headers = {
            "Client-ID": CONFIG.get('CLIENT_ID'),
            "Authorization": f"Bearer {keys['access_token']}"
        }
        response = session.get(f"{url}?{query}".strip(), headers=headers)
        response.raise_for_status()
        return response.json()


def print_now_playing(array):
    """
    Print information about the requested stream
    """
    if len(array["data"]) == 1:
        game = array["data"][0]["game_name"]
        title = array["data"][0]["title"]
        # started_at = array["data"][0]["started_at"]
        print(f"{CONFIG.get('STREAMER')} - [{game}] : {title}")
    else:
        print(f"{CONFIG.get('STREAMER')} is not live")


if __name__ == "__main__":
    load_dotenv()
    CONFIG = {
        "CLIENT_SECRET": f"{os.getenv('CLIENT_SECRET')}",
        "CLIENT_ID": f"{os.getenv('CLIENT_ID')}",
        "STREAMER": f"{os.getenv('STREAMER')}"
    }

    KEYS = get_access_token(
        CONFIG.get('CLIENT_ID'),
        CONFIG.get('CLIENT_SECRET')
    )

    API_HELPER = APIhelper()
    API_HELPER.user_login = CONFIG.get('STREAMER')

    print_now_playing(API_HELPER.get_streams(KEYS))
