#!/usr/bin/env
"""
Receives input data from various APIs (Twitch, YouTube, etc.) before
piping it to mpv for video playback. Other streaming/video platforms
may be added through the use of Streamlink Plugins.
"""

import os

import mpv
from dotenv import load_dotenv
from streamlink import Streamlink

from twitch import get_access_token

load_dotenv()


def player_log(loglevel, component, message):
    """ mpv logger """
    print(f"[{loglevel}] {component}: {message}")


PLAYER = mpv.MPV(
    log_handler=player_log,
    ytdl=False,
    input_default_bindings=True,
    input_vo_keyboard=True
)


def skip_silence():
    """
    Used to automatically skip muted segments in Twitch VODs
    """
    PLAYER.set_loglevel("error")
    PLAYER.af = "lavfi=[silencedetect=n=-20dB:d=1]"
    PLAYER.speed = 100

    def check(evt):
        toks = evt["event"]["text"].split()
        if "silence_end:" in toks:
            return float(toks[2])
        return None

    try:
        PLAYER.time_pos = PLAYER.wait_for_event("log_message", cond=check)
    except TypeError:
        pass

    PLAYER.speed = 1
    PLAYER.af = ""


@PLAYER.python_stream("streamlink-cli")
def reader(quality="best"):
    """ Open stream URL as a file """
    try:
        with STREAM[quality].open() as file:
            while True:
                yield file.read(1024*1024)
    except KeyError as e:
        print(f"{CONFIG.get('STREAMER')} is not live")
        raise e


# Property access, these can be changed at runtime
@PLAYER.property_observer("time-pos")
def time_observer(_name, value):
    """
    Here, value is either None if nothing is playing or a float containing
    fractional seconds since the beginning of the file.
    """
    try:
        print(f"Now playing at {value:.2f}s")
    except TypeError:
        pass


@PLAYER.on_key_press("q")
def q_binding():
    """ mpv keyboard binding """
    print("THERE IS NO ESCAPE")


@PLAYER.on_key_press("s")
def s_binding():
    """ mpv keyboard binding """
    img = PLAYER.screenshot_raw()
    img.save("screenshot.png")


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

    SESSION = Streamlink()
    SESSION.set_option("twitch-api-header", f"OAuth {KEYS['access_token']}")
    SESSION.set_option("stream-timeout", 30)
    SESSION.set_option("player", "mpv")
    STREAM = SESSION.streams(f"https://www.twitch.tv/{CONFIG.get('STREAMER')}")

    PLAYER.fullscreen = False
    PLAYER.loop_playlist = "inf"
    PLAYER.sid = "auto"
    PLAYER.hwaccel = "auto"
    PLAYER["stop-screensaver"] = "yes"
    PLAYER["vo"] = "gpu,"
    PLAYER["ao"] = "alsa,"
    PLAYER.play("python://streamlink-cli")
    skip_silence()
    PLAYER.wait_for_playback()

    del PLAYER
