"""
This is the setup file for managing the emit_sds_l0 package

Author: Winston Olson-Duvall, winston.olson-duvall@jpl.nasa.gov
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emit_sds_l0",
    version="1.4.0",
    author="Winston Olson-Duvall",
    author_email="winston.olson-duvall@jpl.nasa.gov",
    description="""
        L0 scripts and PGEs for EMIT data processing, including pcap->hosc, hosc->ccsds, and helper utilities.
        """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.jpl.nasa.gov/emit-sds/emit-sds-l0",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "ait-core==2.5.2"
    ],
    extras_require={
        "dev": [
            "pycodestyle>=2.6.0",
            "pytest>=6.2.1",
            "pytest-cov>=2.10.1"
        ]
    }
)
