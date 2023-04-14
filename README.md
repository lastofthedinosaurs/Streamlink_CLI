# Streamlink CLI
**Streamlink CLI** is a lightweight command-line utility that lets you watch and record live streams, VODs, and videos from Twitch and YouTube in a terminal.  

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

### Run the script:
``` bash
python3 src/streamlink-cli.py
python3 src/twitch-cli.py
```

### Deactivate the virtual environment:
``` bash
deactivate
```
