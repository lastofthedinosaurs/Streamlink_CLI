#!/usr/bin/env python3

import mpv
from streamlink import Streamlink

session = Streamlink()
session.set_option("twitch-api-header", "OAuth <REDACTED>")
session.set_option("stream-timeout", 30)
session.set_option("player", "mpv")
stream = session.streams("https://www.twitch.tv/<REDACTED>")


def player_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))


player = mpv.MPV(log_handler=player_log, ytdl=False, input_default_bindings=True, input_vo_keyboard=True)
player.fullscreen = False
player.loop_playlist = 'inf'
player.sid = "auto"
player.hwaccel = "auto"

# Option access, in general these require the core to reinitialize
player["stop-screensaver"] = "yes"

# Specify a priority list of audio/video output drivers to be used.
# If the list has a trailing ',', mpv will fall back on drivers not contained in the list.
player['vo'] = 'gpu,'
player['ao'] = 'alsa,'


def skip_silence():
    player.set_loglevel('warn')
    player.af = 'lavfi=[silencedetect=n=-20dB:d=1]'
    player.speed = 100

    def check(evt):
        toks = evt['event']['text'].split()
        if 'silence_end:' in toks:
            return float(toks[2])

    try:
        player.time_pos = player.wait_for_event('log_message', cond=check)
    except TypeError as e:
        print(e)
        pass

    player.speed = 1
    player.af = ''


@player.python_stream("streamlink-cli")
def reader(quality="best"):
    with stream[quality].open() as f:
        while True:
            yield f.read(1024*1024)


# Property access, these can be changed at runtime
@player.property_observer('time-pos')
def time_observer(_name, value):
    # Here, _value is either None if nothing is playing or a float containing
    # fractional seconds since the beginning of the file.
    try:
        print('Now playing at {:.2f}s'.format(value))
    except TypeError:
        pass


@player.on_key_press('q')
def q_binding():
    print('THERE IS NO ESCAPE')


@player.on_key_press('s')
def s_binding():
    img = player.screenshot_raw()
    img.save('screenshot.png')


if __name__ == '__main__':
    player.play("python://streamlink-cli")
    player.wait_for_playback()

    del player
