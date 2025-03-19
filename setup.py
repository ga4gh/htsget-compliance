# -*- coding: utf-8 -*-
"""htsget-compliance setup script

Example:
    Install htsget-compliance::

        $ python setup.py install

Attributes:
    NAME (str): python package name
    VERSION (str): python package version number
    AUTHOR (str): python package author
    EMAIL (str): author's contact email
    install_requires (list): dependencies for this package

Todo:
    
"""

import codecs
import setuptools

NAME = "ga4gh-htsget-compliance"
VERSION = "1.0.0"
AUTHOR = "Jeremy Adams"
EMAIL = "jeremy.adams@ga4gh.org"

try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

with open("README.md", "r") as fh:
    long_description = fh.read()
install_requires = [
    'click',
    'jsonschema',
    'requests'
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description="Reports web service compliance to GA4GH htsget specification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ga4gh/htsget-compliance",
    package_data={
        '': [
            'web/*/*',
            'schemas/*',
            'data/reads/*',
            'data/variants/*'
        ]
    },
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        htsget-compliance=ga4gh.htsget.compliance.entrypoint:main
    ''',
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
)
