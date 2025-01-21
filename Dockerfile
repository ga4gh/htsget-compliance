FROM python:3.13-slim

WORKDIR /app

COPY setup.py ./setup.py
COPY ga4gh ./ga4gh
COPY README.md ./

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip npm
RUN python3 -m pip install --upgrade pip
RUN pip install uv
RUN uv venv && uv pip install .