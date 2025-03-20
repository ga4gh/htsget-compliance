FROM python:3.12-slim

WORKDIR /app

COPY setup.py ./setup.py
COPY ga4gh ./ga4gh
COPY README.md ./

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
RUN python3 -m pip install --upgrade pip
RUN pip install uv
RUN uv venv && source .venv/bin/activate && uv pip install -r requirements.txt

RUN htsget-compliance https://htsget.ga4gh-demo.org/
