
[![Pylint](https://github.com/lastofthedinosaurs/Streamlink_CLI/actions/workflows/pylint.yml/badge.svg)](https://github.com/lastofthedinosaurs/Streamlink_CLI/actions/workflows/pylint.yml) [![Scorecard supply-chain security](https://github.com/lastofthedinosaurs/Streamlink_CLI/actions/workflows/scorecard.yml/badge.svg)](https://github.com/lastofthedinosaurs/Streamlink_CLI/actions/workflows/scorecard.yml)

# Streamlink CLI
**Streamlink CLI** is a lightweight command-line utility that lets you watch and record live streams, VODs, and
videos from Twitch and YouTube in a terminal.  

## Usage

### Download the repository:
``` bash
git clone https://github.com/lastofthedinosaurs/streamlink-cli.git
cd streamlink-cli
git checkout -b dev
git pull origin dev
```

### Create and activate a new virtual environment:

``` bash
python3 -m venv ./venv
source ./venv/bin/activate
```

### Install the requirements:
``` bash
pip3 install --upgrade pip setuptools
pip3 install --requirement requirements.txt
```

### Edit the config file

Move `.env.example` to `.env` and open it with your favorite editor. 

``` bash
mv .env.example .env
vim .env
```

#### Authentication

Twitch APIs use two types of [OAuth 2.0](https://www.rfc-editor.org/rfc/rfc6749) access tokens to access
resources: [user access tokens](https://dev.twitch.tv/docs/authentication/#user-access-tokens) and
[app access tokens](https://dev.twitch.tv/docs/authentication/#app-access-tokens). Each API's
[reference content](https://dev.twitch.tv/docs/api/reference) identifies the type of access token you 
must use to access its resource. Some APIs require a user access token, others require a user access 
token or an app access token, and a few, like the EventSub APIs, require app access tokens.

**Streamlink_CLI** needs the `user:read:follows` scope to display a list of broadcasters that the user 
follows. This means our app requires a `user access token`. We can use the same token to call APIs that
don't require the user's permission because, in most cases, you can use the `user access token` to call 
APIs that accept `app access tokens`.

> **IMPORTANT**
>Treat access tokens, refresh tokens, and client secrets like passwords and safeguard them.

#### Getting OAuth Access Tokens

The first step to getting an access token is registering your application with Twitch (including
forks/clones of **Streamlink_CLI**). [Read more](https://dev.twitch.tv/docs/authentication/register-app/)

**Streamlink_CLI**  uses the Implicit grant flow for now but will switch to the Authorization code
grant flow after development. 

| Flow                                                                                                                            | Token Type        | Description                                                                                                                            |
|---------------------------------------------------------------------------------------------------------------------------------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| [Implicit grant flow](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#implicit-grant-flow)                      | user access token | Use this flow if your app does not use a server.                                                                                       |
| [Authorization code grant flow](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#authorization-code-grant-flow)  | user access token | Use this flow if your app uses a server, can securely store a client secret, and can make server-to-server requests to the Twitch API. |

> **NOTE**
> Third-party apps that call the Twitch APIs and maintain an OAuth session **must** call the `/validate`
> endpoint to verify that the access token is still valid. [Read more](https://dev.twitch.tv/docs/authentication/validate-tokens)

#### Configuration

After your have [registered](https://dev.twitch.tv/docs/authentication/register-app/) with Twitch,
paste the `Client ID` and `Secret` into `.env` under the `CLIENT_ID` and `CLIENT_SECRET` fields,
respectively. 

> **IMPORTANT**
> Ensure the `.env` file is only readable by your user

Run the following command if you're unsure how to do this:
``` bash
chmod 600 .env
```

### Run the script:

For now, the scripts don't accept any arguments, so just executing them as-is should work after
following the steps above.

`streamlink_cli.py` is pre-configured with recommended settings that, in general, will work for
most users.

On my system, mpv uses the `x11` vo driver, but I have sort of a unique setup. Most people will 
want to use `gpu`, which is the default in `streamlink_cli.py`.

If the list has a trailing ',', mpv will fall back on drivers not contained in the list:

``` Python
player["vo"] = "gpu,"
player["ao"] = "alsa,"
```

So, for me, mpv will produce a couple of warnings while it tries the gpu, opengpl, gpu-next, and
xv drivers before finally landing on x11. You should leave the `vo` and `ao` settings unless you 
have a good reason to change them. Playback should still work, even with the errors/warnings.

``` bash
last@laptop ~/streamlink_cli $ python3 src/twitch-cli.py
streamerName - [gameName] : streamTitle

last@laptop ~/streamlink_cli $ python3 src/streamlink_cli.py 
/home/last/streamlink_cli/venv/bin/python /home/last/streamlink_cli/src/streamlink_cli.py 

libEGL warning: DRI2: failed to authenticate
[warn] vo/gpu/opengl: Suspected software renderer or indirect context.

[error] vo/gpu: Can't open TTY for VT control: No such device or address

[warn] vo/gpu/opengl: Failed to set up VT switcher. Terminal switching will be unavailable.

[error] vo/gpu: Failed to create GBM surface.

[error] vo/gpu: Failed to setup GBM.

[warn] vo/gpu/opengl: Suspected software renderer or indirect context.

[error] vo/gpu: Can't open TTY for VT control: No such device or address

[warn] vo/gpu/opengl: Failed to set up VT switcher. Terminal switching will be unavailable.

[error] vo/gpu: Failed to create GBM surface.

[error] vo/gpu: Failed to setup GBM.

MESA-LOADER: failed to open iris: /usr/lib64/dri/iris_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib64/dri, suffix _dri)
failed to load driver: iris
MESA-LOADER: failed to open zink: /usr/lib64/dri/zink_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib64/dri, suffix _dri)
failed to load driver: zink
libEGL warning: DRI2: failed to authenticate
MESA-LOADER: failed to open iris: /usr/lib64/dri/iris_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib64/dri, suffix _dri)
failed to load driver: iris
MESA-LOADER: failed to open zink: /usr/lib64/dri/zink_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib64/dri, suffix _dri)
failed to load driver: zink
libEGL warning: DRI2: failed to authenticate
MESA-LOADER: failed to open iris: /usr/lib64/dri/iris_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib64/dri, suffix _dri)
failed to load driver: iris
MESA-LOADER: failed to open zink: /usr/lib64/dri/zink_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib64/dri, suffix _dri)
failed to load driver: zink
[warn] vo/gpu-next/opengl: Suspected software renderer or indirect context.

[error] vo/gpu-next: Can't open TTY for VT control: No such device or address

[warn] vo/gpu-next/opengl: Failed to set up VT switcher. Terminal switching will be unavailable.

[error] vo/gpu-next: Failed to create GBM surface.

[error] vo/gpu-next: Failed to setup GBM.

[error] vo/xv: No Xvideo support found.

[warn] vo/x11: Warning: this legacy VO has bad performance. Consider fixing your graphics drivers, or not forcing the x11 VO.

Now playing at 0.00s
Now playing at 0.03s
Now playing at 0.07s
Now playing at 0.10s
Now playing at 0.13s
Now playing at 0.17s
Now playing at 0.20s
Now playing at 0.23s
Now playing at 0.27s
Now playing at 0.30s
Now playing at 0.33s
Now playing at 0.37s
Now playing at 0.40s
Now playing at 0.43s
Now playing at 0.47s
Now playing at 0.50s
Now playing at 0.53s
Now playing at 0.57s
Now playing at 0.60s
Now playing at 0.63s
Now playing at 0.67s
Now playing at 0.70s
Now playing at 0.73s
Now playing at 0.77s
Now playing at 0.80s
Now playing at 0.83s
Now playing at 0.87s
Now playing at 0.90s
Now playing at 0.93s
Now playing at 0.97s
Now playing at 1.00s
Now playing at 1.03s
Now playing at 1.07s
Now playing at 1.10s

...

```

### Deactivate the virtual environment:
``` bash
deactivate
```
