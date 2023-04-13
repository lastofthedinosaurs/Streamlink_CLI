#!/usr/bin/env python3

import mpv
from streamlink import Streamlink

session = Streamlink()
session.set_option("twitch-api-header", "OAuth <REDACTED>")
session.set_option("stream-timeout", 30)
session.set_option("player", "mpv")
stream = session.streams("https://www.twitch.tv/<REDACTED>")


def my_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))


p = mpv.MPV(log_handler=my_log, ytdl=True, input_default_bindings=True, input_vo_keyboard=True)
p.fullscreen = True
p.loop_playlist = 'inf'
p.fullscreen = "no"
p.sid = "auto"
p.hwaccel = "auto"

# Option access, in general these require the core to reinitialize
p["stop-screensaver"] = "yes"

# Specify a priority list of audio/video output drivers to be used.
# If the list has a trailing ',', mpv will fall back on drivers not contained in the list.
p['vo'] = 'gpu,'
p['ao'] = 'pulse,'


def skip_silence():
    p.set_loglevel('debug')
    p.af = 'lavfi=[silencedetect=n=-20dB:d=1]'
    p.speed = 100

    def check(evt):
        toks = evt['event']['text'].split()
        if 'silence_end:' in toks:
            return float(toks[2])

    try:
        p.time_pos = p.wait_for_event('log_message', cond=check)
    except TypeError as e:
        print(e)
        pass

    p.speed = 1
    p.af = ''


@p.python_stream("streamlink-cli")
def reader(quality="best"):
    with stream[quality].open() as f:
        while True:
            yield f.read(1024*1024)


# Property access, these can be changed at runtime
@p.property_observer('time-pos')
def time_observer(_name, value):
    # Here, _value is either None if nothing is playing or a float containing
    # fractional seconds since the beginning of the file.
    try:
        print('Now playing at {:.2f}s'.format(value))
    except TypeError as e:
        print(e)
        pass


@p.on_key_press('q')
def my_q_binding():
    print('THERE IS NO ESCAPE')


@p.on_key_press('s')
def my_s_binding():
    pillow_img = p.screenshot_raw()
    pillow_img.save('screenshot.png')


if __name__ == '__main__':
    p.play("python://streamlink-cli")
    skip_silence()
    p.wait_for_playback()

    del p
