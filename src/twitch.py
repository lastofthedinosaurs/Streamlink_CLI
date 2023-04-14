#!/usr/bin/env python3

import requests

client_secret = "<REDACTED>"
client_id = "<REDACTED>"
streamer = "<REDACTED>"


def get_access_token():
    with requests.Session() as s:
        body = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        r = s.post('https://id.twitch.tv/oauth2/token', body)
        r.raise_for_status()
        return r.json()


def get_stream_data(k):
    with requests.Session() as s:
        headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {k['access_token']}"
        }
        r = s.get(f'https://api.twitch.tv/helix/streams?user_login={streamer}', headers=headers)
        r.raise_for_status()
        return r.json()


def print_now_playing(d):
    if len(d['data']) == 1:
        title = d['data'][0]['title']
        game = d['data'][0]['game_name']
        started_at = d['data'][0]['started_at']
        print(f"{streamer} - [{game}] : {title}")
    else:
        print(f"{streamer} is not live")


if __name__ == '__main__':
    keys = get_access_token()
    data = get_stream_data(keys)

    print_now_playing(data)
