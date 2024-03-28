FROM python:3.8.16-bullseye
LABEL project="lightning-pworker"
ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    wget \
    git \
    build-essential \
    libgl1 \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev 

RUN echo 'PS1="\[$(tput setaf 3)$(tput bold)[\]lightning-pworker:\\w]#\[$(tput sgr0) \]"' >> /root/.bashrc
WORKDIR /workspace/lightning
RUN pip3 install pika
RUN pip3 install dotmap
RUN pip3 install redis
RUN pip3 install docker
RUN pip3 install requests
RUN pip3 install urllib3
RUN pip3 install sentry-sdk
RUN pip3 install boto3
RUN pip3 install pysbd
RUN pip3 install psutil schedule
RUN pip3 install watchdog
RUN apt-get install -y inotify-tools
RUN pip3 install grpcio grpcio-tools googleapis-common-protos mypy-protobuf
RUN pip3 install py7zr