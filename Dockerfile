FROM python:3.12-slim

WORKDIR /app

COPY setup.py ./setup.py
COPY ga4gh ./ga4gh
COPY unittests ./unittests
COPY README.md ./
COPY requirements.txt ./

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip samtools tabix bcftools
RUN python3 -m pip install --upgrade pip
RUN pip install crypt4gh && pip install .

CMD ["htsget-compliance", "https://htsget.ga4gh-demo.org/"]
