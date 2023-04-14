#!/usr/bin/env python3

import requests

CLIENT_SECRET = "<REDACTED>"
CLIENT_ID = "<REDACTED>"
STREAMER = "<REDACTED>"


def get_access_token():
    with requests.Session() as s:
        body = {
            "CLIENT_ID": CLIENT_ID,
            "CLIENT_SECRET": CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        r = s.post('https://id.twitch.tv/oauth2/token', body)
        r.raise_for_status()
        return r.json()


def get_stream_data(k):
    with requests.Session() as s:
        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {k['access_token']}"
        }
        r = s.get(f'https://api.twitch.tv/helix/streams?user_login={STREAMER}', headers=headers)
        r.raise_for_status()
        return r.json()


def print_now_playing(d):
    if len(d['data']) == 1:
        title = d['data'][0]['title']
        game = d['data'][0]['game_name']
        # started_at = d['data'][0]['started_at']
        print(f"{STREAMER} - [{game}] : {title}")
    else:
        print(f"{STREAMER} is not live")


if __name__ == '__main__':
    keys = get_access_token()
    data = get_stream_data(keys)

    print_now_playing(data)
