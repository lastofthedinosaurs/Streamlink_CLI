# Streamlink CLI
`Streamlink CLI` is a lightweight command-line utility that lets you watch and record live streams, VODs, and videos from Twitch and YouTube in a terminal.  

## Install

### Download the repository
``` bash
git clone https://github.com/lastofthedinosaurs/streamlink-cli.git
cd streamlink-cli
```

## Run

### Docker method

Build the image, then run a container using the image. 

#### Build image:
``` bash
docker build --tag lastofthedinosaurs/streamlink-cli:latest .
```

#### Run container:
``` bash
docker run --name streamlink-cli --interactive --tty lastofthedinosaurs/streamlink-cli:latest 
```

### Virtual Environment method

Create a new virtual environment, install the required Python packages, then run the script.

#### Create and activate a new virtual environment:

``` bash
python3 -m venv ./venv
source ./venv/bin/activate
```

#### Install the requirements:
``` bash
pip3 install --no-cache --upgrade pip setuptools
pip3 install --requirement requirements.txt
```

#### Run script:
``` bash
python3 streamlink-cli.py
```

## Remove

### Docker method

#### Remove container:
``` bash
docker rm streamlink-cli
```

#### Remove image:
``` bash
docker image rm lastofthedinosaurs/streamlink-cli:latest
```

### Virtual Environment method

#### Deactivate virtual environment:
``` bash
deactivate
```

#### Remove virtual environment:
``` bash
rm ./venv
```
