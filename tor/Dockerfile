FROM alpine:3.19

LABEL maintainer="Peter Dave Hello <hsu@peterdavehello.org>"
LABEL name="tor-socks-proxy"
LABEL version="latest"

# Install necessary packages, including Tor and nyx
RUN echo '@edge https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories && \
    echo '@edge https://dl-cdn.alpinelinux.org/alpine/edge/testing'   >> /etc/apk/repositories && \
    apk -U upgrade && \
    apk -v add tor@edge obfs4proxy@edge curl && \
    apk -v add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/community/ nyx && \
    chmod 700 /var/lib/tor && \
    rm -rf /var/cache/apk/* && \
    tor --version

# Copy the torrc configuration file
COPY --chown=tor:root torrc /etc/tor/

# Expose the necessary ports for Tor
EXPOSE 8853/udp 9150/tcp

# Set the user to 'tor'
USER tor

# Start Tor with your custom configuration file
CMD ["/usr/bin/tor", "-f", "/etc/tor/torrc"]
