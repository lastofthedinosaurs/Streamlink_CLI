#!/usr/bin/env python3
"""
Used to query the Twitch API for data to feed to Streamlink
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()


class Config:
    OAUTH_URL = os.getenv("OAUTH_URL")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    CLIENT_ID = os.getenv("CLIENT_ID")
    STREAMER = os.getenv("STREAMER")


CONFIG = Config()


def get_access_token():
    """
    Twitch APIs require OAuth 2.0 access tokens to access resources.
    """
    with requests.Session() as session:
        body = {
            "client_id": CONFIG.CLIENT_ID,
            "client_secret": CONFIG.CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        response = session.post(CONFIG.OAUTH_URL, body)
        response.raise_for_status()
        return response.json()


def api_request(keys, url, query=''):
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
    KEYS = get_access_token()

    URL = "https://api.twitch.tv/helix/streams"
    QUERY = f"user_login={CONFIG.STREAMER}"

    DATA = api_request(KEYS, URL, QUERY)

    print_now_playing(DATA)
