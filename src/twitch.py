#!/usr/bin/env python3
"""
Used to query the Twitch API for data to feed to Streamlink
"""

import requests

CLIENT_SECRET = '<REDACTED>'
CLIENT_ID = '<REDACTED>'
STREAMER = '<REDACTED>'


def get_access_token():
    """
    Twitch APIs require OAuth 2.0 access tokens to access resources.
    """
    with requests.Session() as s:
        body = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        r = s.post('https://id.twitch.tv/oauth2/token', body)
        r.raise_for_status()
        return r.json()


def api_request(keys, url, query=''):
    """
    Send a GET request to the Twitch API
    """
    with requests.Session() as s:
        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {keys['access_token']}"
        }
        r = s.get(f"{url}?{query}", headers=headers)
        r.raise_for_status()
        return r.json()


def print_now_playing(data):
    """
    Print information about the requested stream
    """
    if len(data['data']) == 1:
        title = data['data'][0]['title']
        game = data['data'][0]['game_name']
        # started_at = data['data'][0]['started_at']
        print(f"{STREAMER} - [{game}] : {title}")
    else:
        print(f"{STREAMER} is not live")


if __name__ == '__main__':
    KEYS = get_access_token()

    URL = "https://api.twitch.tv/helix/streams"
    QUERY = f"user_login={STREAMER}"

    DATA = api_request(KEYS, URL, QUERY)

    print_now_playing(DATA)
