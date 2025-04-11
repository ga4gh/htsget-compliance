[![Build Status][actions-badge]][actions-url]
[![Coverage Status](https://img.shields.io/coveralls/github/ga4gh/htsget-compliance.svg?style=flat-square)](https://coveralls.io/github/ga4gh/htsget-compliance)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg?style=flat-square)](https://www.python.org)

[actions-badge]: https://github.com/ga4gh/htsget-compliance/actions/workflows/test_build_release.yml/badge.svg
[actions-url]: https://github.com/ga4gh/htsget-compliance/actions?query=workflow%3Ahtsget-compliance+branch%3Amaster

# htsget Compliance
The htsget Compliance Suite determines a web service's compliance with the 
[htsget API specification](http://samtools.github.io/hts-specs/htsget.html) for serving large alignment and variant datasets. The
specification, developed by the
[Global Alliance for Genomics and Health](https://ga4gh.org), serves
to provide a standardized, interoperable API framework across different
institutions.

## Installation

First, required pre-requisites are [`samtools`, `bcftools`, `htsfile`](https://www.htslib.org/) and [`crypt4gh`](https://pypi.org/project/crypt4gh/) are assumed to be pre-installed in the system, i.e:

```shell
apt-get install samtools bcftools tabix uv  (OSX: brew install samtools uv)
uv venv .
pip install crypt4gh
```
To install `htsget-compliance`, clone the Github repository, then install via setuptools in a new virtual environment.

Create a new virtual environment:

```sh
git clone https://github.com/ga4gh/htsget-compliance.git
cd htsget-compliance

python3 -m venv .venv
source .venv/bin/activate
```

Install the package:
```sh
pip install -e .
```

## Quickstart

Running the following:

```shell
htsget-compliance https://htsget.ga4gh-demo.org  | jq '.["summary"]'
```

Should ideally yield:

```json
{
  "run": 12,
  "passed": 12,
  "warned": 0,
  "failed": 0,
  "skipped": 0
}
```

## Usage

The compliance tests can be run via `htsget-compliance ${HTSGET_URL}`, where 
`HTSGET_URL` is the base url to an htsget service. For example:
```
htsget-compliance https://htsget.ga4gh-demo.org
```

Additional commandline options can be specified to:

* write JSON report to file (`-f`)
* change the url path to alignment objects from the default /reads/{id} (`-r`)
* change the url path to variant objects from the default /variants/{id} (`-v`)
* etc.

A full list of options can be displayed via `htsget-compliance --help`

## Submitting Reports

The report can optionally be submitted to a local or hosted GA4GH Testbed Service with additional commandline options. While running the [GA4GH Testbed API](https://github.com/ga4gh/ga4gh-testbed-api), you can submit reports to your local instance with the following: 
```
htsget-compliance https://htsget.ga4gh-demo.org/  -s --submit-id 1edb5213-52a2-434f-a7b8-b101fea8fb30 --submit-token K5pLbwScVu8rEoLLj8pRy5Wv7EXTVahn --testbed-url http://localhost:4500/reports
```

If the [GA4GH Testbed UI](https://github.com/ga4gh/ga4gh-testbed-ui) is also running you can then see the report displayed on a web UI (ex. http://localhost:4500/).

## License

See the [LICENSE](https://github.com/ga4gh/htsget-compliance/blob/master/LICENSE)

## Issues

Please raise any issues on [Github](https://github.com/ga4gh/htsget-compliance/issues)
