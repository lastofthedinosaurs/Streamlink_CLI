#!/usr/bin/env
"""
Receives input data from various APIs (Twitch, YouTube, etc.) before
piping it to mpv for video playback. Other streaming/video platforms
can easily be added through the use of Streamlink Plugins.
"""

import mpv
from streamlink import Streamlink

session = Streamlink()
session.set_option("twitch-api-header", "OAuth <REDACTED>")
session.set_option("stream-timeout", 30)
session.set_option("player", "mpv")
stream = session.streams("https://www.twitch.tv/<REDACTED>")


def player_log(loglevel, component, message):
    """ Streamlink logger """
    print(f"[{loglevel}] {component}: {message}")


player = mpv.MPV(
    log_handler=player_log,
    ytdl=False,
    input_default_bindings=True,
    input_vo_keyboard=True
)
player.fullscreen = False
player.loop_playlist = "inf"
player.sid = "auto"
player.hwaccel = "auto"
player["stop-screensaver"] = "yes"
player["vo"] = "gpu,"
player["ao"] = "alsa,"


def skip_silence():
    """
    Used to automatically skip muted segments in Twitch VODs
    """
    player.set_loglevel("warn")
    player.af = "lavfi=[silencedetect=n=-20dB:d=1]"
    player.speed = 100

    def check(evt):
        toks = evt["event"]["text"].split()
        if "silence_end:" in toks:
            return float(toks[2])
        return None

    try:
        player.time_pos = player.wait_for_event("log_message", cond=check)
    except TypeError:
        pass

    player.speed = 1
    player.af = ""


@player.python_stream("streamlink-cli")
def reader(quality="best"):
    """ Open stream URL as a file """
    with stream[quality].open() as f:
        while True:
            yield f.read(1024*1024)


# Property access, these can be changed at runtime
@player.property_observer("time-pos")
def time_observer(_name, value):
    """
    Here, value is either None if nothing is playing or a float containing
    fractional seconds since the beginning of the file.
    """
    try:
        print(f"Now playing at {value:.2f}s")
    except TypeError:
        pass


@player.on_key_press("q")
def q_binding():
    """ MPV keyboard binding """
    print("THERE IS NO ESCAPE")


@player.on_key_press("s")
def s_binding():
    """ MPV keyboard binding """
    i = player.screenshot_raw()
    i.save("screenshot.png")


if __name__ == "__main__":
    player.play("python://streamlink-cli")
    skip_silence()
    player.wait_for_playback()

    del player
