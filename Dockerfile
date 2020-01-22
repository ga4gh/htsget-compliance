FROM ubuntu:18.04

WORKDIR /app

COPY setup.py ./setup.py
COPY ga4gh ./ga4gh
COPY README.md ./

RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get install -y python3.7
RUN apt-get install -y python3-pip
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN python3.7 -m pip install --upgrade pip
RUN npm install dredd --global
RUN python3.7 setup.py install
