#!/usr/bin/env python3
"""
Used to query the Twitch API for data to feed to Streamlink
"""

import os

import requests
from dotenv import load_dotenv


class Config:
    OAUTH_URL = os.getenv("OAUTH_URL")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    CLIENT_ID = os.getenv("CLIENT_ID")
    STREAMER = os.getenv("STREAMER")


class APIhelper:
    id = ""
    login = ""
    user_id = ""
    user_login = ""
    game_id = ""
    type = "live"
    lang = "en"
    first = 10

    def get_streams(self, keys, query=""):
        """
        Gets a list of all streams.

        The list is in descending order by the number of viewers
        watching the stream. Because viewers come and go during a
        stream, it’s possible to find duplicate or missing streams
        in the list as you page through the results.
        """
        url = "https://api.twitch.tv/helix/streams"
        if not query:
            if self.user_id:
                query = f"user_id={self.user_id}"
            elif self.user_login:
                query = f"user_login={self.user_login}"
            elif self.game_id:
                query = f"game_id={self.game_id}"
        return api_request(
            keys,
            url,
            f"{query}&language={self.lang}".strip()
        )

    def get_users(self, keys, query=""):
        """
        Gets information about one or more users.

        If you don’t specify IDs or login names, the request returns
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


def get_access_token():
    """
    Twitch APIs require OAuth 2.0 access tokens to access resources.
    """
    url = "https://id.twitch.tv/oauth2/token"
    with requests.Session() as session:
        body = {
            "client_id": CONFIG.CLIENT_ID,
            "client_secret": CONFIG.CLIENT_SECRET,
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
            "Client-ID": CONFIG.CLIENT_ID,
            "Authorization": f"Bearer {keys['access_token']}"
        }
        response = session.get(f"{url}?{query}", headers=headers)
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
        print(f"{CONFIG.STREAMER} - [{game}] : {title}")
    else:
        print(f"{CONFIG.STREAMER} is not live")


if __name__ == "__main__":
    load_dotenv()
    CONFIG = Config()

    KEYS = get_access_token()

    API_HELPER = APIhelper()
    API_HELPER.user_login = CONFIG.STREAMER

    print_now_playing(API_HELPER.get_streams(KEYS))
