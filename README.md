[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](https://opensource.org/licenses/Apache-2.0)
[![Coverage Status](https://img.shields.io/coveralls/github/ga4gh/htsget-compliance.svg?style=flat-square)](https://coveralls.io/github/ga4gh/htsget-compliance)
[![Python 3.6](https://img.shields.io/badge/python-3.6%20|%203.7-blue.svg?style=flat-square)](https://www.python.org)

# htsget Compliance
The htsget Compliance Suite determines a web service's compliance with the 
[htsget API specification](http://samtools.github.io/hts-specs/htsget.html) for serving large alignment and variant datasets. The
specification, developed by the
[Global Alliance for Genomics and Health](https://ga4gh.org), serves
to provide a standardized, interoperable API framework across different
institutions.

## Installation

To install, clone the Github repository, then install via setuptools:
```
git clone https://github.com/ga4gh/htsget-compliance.git
cd htsget-compliance
python setup.py install
```

## Usage

The compliance tests can be run via `htsget-compliance ${HTSGET_URL}`, where 
`HTSGET_URL` is the base url to an htsget service. For example:
```
htsget-compliance https://htsget.ga4gh.org
```

Additional commandline options can be specified to:

* write JSON report to file (`-f`)
* change the url path to alignment objects from the default /reads/{id} (`-r`)
* change the url path to variant objects from the default /variants/{id} (`-v`)
* etc.

A full list of options can be displayed via `htsget-compliance --help`

Requires [`Samtools` suite](http://www.htslib.org/) to be available in your path

## License

See the [LICENSE](https://github.com/ga4gh/htsget-compliance/blob/master/LICENSE)

## Issues

Please raise any issues on [Github](https://github.com/ga4gh/htsget-compliance/issues)
