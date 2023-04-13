FROM alpine:3.17.3

ARG command

LABEL maintainer="LastoftheDinosaurs"
LABEL org.label-schema.description="Containerization of Streamlink CLI"
LABEL org.label-schema.name="streamlink-cli"
LABEL org.label-schema.schema-version="0.1"
LABEL org.label-schema.vcs-url="https://github.com/lastofthedinosaurs/streamlink-cli"

RUN apk add --no-cache \
    ffmpeg \
    mesa-demos \
    mpv \
    mpv-dev \
    mpv-libs \
    pulseaudio \
    ttf-dejavu \
    python3 \
  && adduser -u 1000 -D streamlink-cli \
  && mkdir -p /home/streamlink-cli/.config/mpv \
  && mkdir -p /home/streamlink-cli/.config/pulse \
  && echo "default-server = unix:/run/user/1000/pulse/native" > /home/streamlink-cli/.config/pulse/client.conf \
  && echo "autospawn = no" >> /home/streamlink-cli/.config/pulse/client.conf \
  && echo "daemon-binary = /bin/true" >> /home/streamlink-cli/.config/pulse/client.conf \
  && echo "enable-shm = false" >> /home/streamlink-cli/.config/pulse/client.conf \
  && echo "UP add volume +2" > /home/streamlink-cli/.config/mpv/input.conf \
  && echo "DOWN add volume -2" >> /home/streamlink-cli/.config/mpv/input.conf \
  && chown -R streamlink-cli:streamlink-cli /home/streamlink-cli

USER streamlink-cli

WORKDIR /home/streamlink-cli/

COPY [ "streamlink-cli.py", "requirements.txt", "/home/streamlink-cli/" ]

RUN export PATH="${HOME}/.local/bin:${PATH}" \
    && python3 -m ensurepip \
    && pip3 install --no-cache --upgrade pip setuptools \
    && pip3 install --requirement requirements.txt

CMD [ "python3", "streamlink-cli.py", "${command}" ]
