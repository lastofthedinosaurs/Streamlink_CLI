#!/usr/bin/env python3
"""
Receives input data from various APIs (Twitch, YouTube, etc.)
before piping it to mpv for video playback. Other streaming/video
platforms may be added through the use of Streamlink Plugins.
"""

import os
from mpv import MPV
import streamlink
from dotenv import load_dotenv
from twitch_helper import TwitchAPISession

load_dotenv()


def player_log(loglevel, component, message):
    """ mpv logger """
    print(f"[{loglevel}] {component}: {message}")


def print_now_playing(array, config_data):
    """
    Print information about the requested stream
    """
    if len(array["data"]) == 1:
        game = array["data"][0]["game_name"]
        title = array["data"][0]["title"]
        print(f"{config_data['STREAMER']} - [{game}]: {title}")
    else:
        print(f"{config_data['STREAMER']} is not live")


class TwitchPlayer:
    """
    A class for playing Twitch streams using mpv media player.

    Attributes:
        mpv (MPV): The mpv media player instance.
        stream (streamlink.Stream): Object representing the stream to be played.
        config (dict): Twitch API credentials and streamer settings.
        audio_filter (str): Audio filter setting for skipping silenced segments in Twitch VODs.
        speed (int): Playback speed for skipped silenced segments.
        time_pos (float): Position of the playback time in seconds.
        fullscreen (bool): Flag indicating whether the media player is in fullscreen mode.

    Methods:
        skip_silence(): Automatically skip muted segments in Twitch VODs.
        reader(quality="best"): Open the stream URL as a file and yield its content.
        q_binding(): mpv keyboard binding for the 'q' key press.
        s_binding(): mpv keyboard binding for the 's' key press (screenshot).
        time_observer(_name, value): Observer method to track the playback time position.

    Note:
        Requires 'mpv', 'streamlink', and 'dotenv' libraries to be installed.

    Example usage:
        player = TwitchPlayer()
        player.config = {...}  # Dict with Twitch API credentials and streamer info.
        player.stream = streamlink.streams("https://www.twitch.tv/example_stream")['best']
        player.mpv.fullscreen = False
        player.reader()
        player.skip_silence()
        player.mpv.wait_for_playback()
        del player
    """
    def __init__(self):
        self.mpv = MPV(log_handler=player_log, ytdl=False)
        self.stream = None
        self.config = None
        self.audio_filter = None
        self.speed = None
        self.time_pos = None
        self.fullscreen = False

    def skip_silence(self):
        """
        Used to automatically skip muted segments in Twitch VODs
        """
        self.mpv.set_loglevel("error")
        self.audio_filter = "lavfi=[silencedetect=n=-20dB:d=1]"
        self.speed = 100

        def check(evt):
            toks = evt["event"]["text"].split()
            if "silence_end:" in toks:
                return float(toks[2])
            return None

        try:
            self.time_pos = self.mpv.wait_for_event("log-message", cond=check)
        except TypeError:
            pass

        self.speed = 1
        self.audio_filter = ""

    def reader(self, quality="best"):
        """ Open stream URL as a file """
        try:
            with self.stream[quality].open() as file:
                while True:
                    yield file.read(1024 * 1024)
        except KeyError as error:
            print(f"{self.config.get('STREAMER')} is not live")
            raise error

    # pylint: disable=E1120
    @MPV.on_key_press("q")
    def q_binding(self):
        """ mpv keyboard binding """
        print("THERE IS NO ESCAPE")

    # pylint: disable=E1120
    @MPV.on_key_press("s")
    def s_binding(self):
        """ mpv keyboard binding """
        img = self.mpv.screenshot_raw()
        img.save("screenshot.png")

    # pylint: disable=E1120
    @MPV.property_observer("time-pos")
    def time_observer(self, _name, value):
        """
        Here, value is either None if nothing is playing or a float containing
        fractional seconds since the beginning of the file.
        """
        try:
            print(f"Now playing at {value:.2f}s")
        except TypeError:
            pass


if __name__ == "__main__":
    load_dotenv()
    config = {
        "CLIENT_SECRET": os.getenv('CLIENT_SECRET'),
        "CLIENT_ID": os.getenv('CLIENT_ID'),
        "STREAMER": os.getenv('STREAMER')
    }

    twitch_api = TwitchAPISession(config["CLIENT_ID"], config["CLIENT_SECRET"])

    # Example usage of the class methods:
    channel_schedule = twitch_api.get_channel_stream_schedule()
    print_now_playing(channel_schedule, config)

    clips = twitch_api.get_clips(broadcaster_id="example_broadcaster_id")
    print(clips)

    # Instantiate the stream object here using streamlink.streams
    STREAM_URL = "https://www.twitch.tv/example_stream"  # For example

    streams = streamlink.streams(STREAM_URL)
    your_stream_object = streams['best']  # Choose the quality: 'best', 'worst', '720p', etc.

    player = TwitchPlayer()
    player.config = config
    player.stream = your_stream_object
    player.mpv.fullscreen = False
    player.mpv.loop_playlist = "inf"
    player.mpv.sid = "auto"
    player.mpv.hwaccel = "auto"
    player.mpv["stop-screensaver"] = "yes"
    player.mpv["vo"] = "gpu,opengl"
    player.mpv["ao"] = "alsa"
    player.reader()
    player.skip_silence()
    player.mpv.wait_for_playback()

    del player
